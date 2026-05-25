#!/usr/bin/env bash
set -euo pipefail

MODEL="${MODEL:-Qwen/Qwen2.5-0.5B-Instruct}"
INFERENCE_PORT="${INFERENCE_PORT:-8000}"
GATEWAY_PORT="${GATEWAY_PORT:-8080}"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON_BIN="${PYTHON:-$ROOT_DIR/.venv/bin/python}"
TMP_DIR="${TMP_DIR:-$ROOT_DIR/.tmp/smoke}"
FAILURES=0
STARTED_INFERENCE=0
STARTED_GATEWAY=0
INFERENCE_PID=""
GATEWAY_PID=""

if [[ "$PYTHON_BIN" == */* && "$PYTHON_BIN" != /* ]]; then
  PYTHON_BIN="$ROOT_DIR/$PYTHON_BIN"
fi

wait_for_url() {
  local url="$1"
  local retries=30
  while [ "$retries" -gt 0 ]; do
    if curl -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    retries=$((retries - 1))
    sleep 1
  done
  return 1
}

service_is_up() {
  local url="$1"
  curl -fsS "$url" >/dev/null 2>&1
}

start_inference_if_needed() {
  if service_is_up "http://localhost:${INFERENCE_PORT}/health"; then
    return 0
  fi
  (
    cd "$ROOT_DIR/projects/inference-service"
    env PYTHON="$PYTHON_BIN" MODEL="$MODEL" PORT="$INFERENCE_PORT" bash scripts/serve.sh
  ) >/tmp/ai-infra-smoke-inference.log 2>&1 &
  INFERENCE_PID=$!
  STARTED_INFERENCE=1
  wait_for_url "http://localhost:${INFERENCE_PORT}/health"
}

start_gateway_if_needed() {
  if service_is_up "http://localhost:${GATEWAY_PORT}/health"; then
    return 0
  fi
  (
    cd "$ROOT_DIR/projects/ai-gateway"
    env PYTHON="$PYTHON_BIN" PORT="$GATEWAY_PORT" bash scripts/serve.sh
  ) >/tmp/ai-infra-smoke-gateway.log 2>&1 &
  GATEWAY_PID=$!
  STARTED_GATEWAY=1
  wait_for_url "http://localhost:${GATEWAY_PORT}/health"
}

cleanup() {
  if [ "$STARTED_GATEWAY" -eq 1 ] && [ -n "$GATEWAY_PID" ]; then
    kill "$GATEWAY_PID" 2>/dev/null || true
    wait "$GATEWAY_PID" 2>/dev/null || true
  fi
  if [ "$STARTED_INFERENCE" -eq 1 ] && [ -n "$INFERENCE_PID" ]; then
    kill "$INFERENCE_PID" 2>/dev/null || true
    wait "$INFERENCE_PID" 2>/dev/null || true
  fi
}

trap cleanup EXIT

mkdir -p "$TMP_DIR"
rm -rf "$TMP_DIR/eval" "$TMP_DIR/finetune" "$TMP_DIR/serving" "$TMP_DIR/evidence"

check_code() {
  local name="$1"
  local expected="$2"
  local cmd="$3"
  local code
  code="$(eval "$cmd")"
  if [ "$code" = "$expected" ]; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name (expected $expected got $code)"
    FAILURES=$((FAILURES + 1))
  fi
}

check_body_contains() {
  local name="$1"
  local needle="$2"
  local cmd="$3"
  local body
  body="$(eval "$cmd")"
  if grep -q "$needle" <<<"$body"; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name (missing '$needle')"
    FAILURES=$((FAILURES + 1))
  fi
}

check_path_exists() {
  local name="$1"
  local path="$2"
  if [ -e "$path" ]; then
    echo "[PASS] $name"
  else
    echo "[FAIL] $name (missing '$path')"
    FAILURES=$((FAILURES + 1))
  fi
}

save_snapshot() {
  local url="$1"
  local path="$2"
  mkdir -p "$(dirname "$path")"
  curl -fsS "$url" >"$path"
}

save_serving_evidence() {
  local serving_tmp="$TMP_DIR/serving"
  mkdir -p "$serving_tmp"

  save_snapshot "http://localhost:${INFERENCE_PORT}/health" "$serving_tmp/inference_health.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/health" "$serving_tmp/gateway_health.json"
  save_snapshot "http://localhost:${INFERENCE_PORT}/v1/models" "$serving_tmp/inference_models.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/v1/models" "$serving_tmp/gateway_models.json"
  save_snapshot "http://localhost:${INFERENCE_PORT}/metrics" "$serving_tmp/inference_metrics.prom"
  save_snapshot "http://localhost:${GATEWAY_PORT}/metrics" "$serving_tmp/gateway_metrics.prom"
  save_snapshot "http://localhost:${INFERENCE_PORT}/events/summary?event_type=request_success&requested_model=${MODEL}" "$serving_tmp/inference_events_summary.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/events/summary?event_type=request_success&upstream_model=vllm-local" "$serving_tmp/gateway_events_summary.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/events/failures" "$serving_tmp/gateway_failure_summary.json"
  save_snapshot "http://localhost:${INFERENCE_PORT}/events/requests?requested_model=${MODEL}" "$serving_tmp/inference_request_index.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/events/requests?requested_model=vllm-local&upstream_model=vllm-local" "$serving_tmp/gateway_request_index.json"
  save_snapshot "http://localhost:${INFERENCE_PORT}/events/requests/req_smoke_inference_1" "$serving_tmp/inference_request_timeline.json"
  save_snapshot "http://localhost:${GATEWAY_PORT}/events/requests/req_smoke_gateway_1" "$serving_tmp/gateway_request_timeline.json"
}

build_evidence_packet() {
  local evidence_tmp="$TMP_DIR/evidence"
  mkdir -p "$evidence_tmp"
  "$PYTHON_BIN" "$ROOT_DIR/scripts/build_evidence_packet.py" \
    --smoke-dir "$TMP_DIR" \
    --output "$evidence_tmp/evidence_packet.json" \
    --markdown-output "$evidence_tmp/evidence_packet.md" \
    --strict >/tmp/ai-infra-evidence-packet.log 2>&1
}

run_eval_smoke() {
  local eval_dir="$ROOT_DIR/projects/eval-module"
  local eval_tmp="$TMP_DIR/eval"
  mkdir -p "$eval_tmp"

  (
    cd "$eval_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m eval_module.main run \
      --task mmlu \
      --model "$MODEL" \
      --backend-url "http://localhost:${INFERENCE_PORT}/v1" \
      --output "$eval_tmp/baseline.json" >/tmp/ai-infra-eval-run.log 2>&1
  )
  (
    cd "$eval_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m eval_module.main compare \
      --baseline "$eval_tmp/baseline.json" \
      --candidate "$eval_tmp/baseline.json" \
      --output "$eval_tmp/compare.json" >/tmp/ai-infra-eval-compare.log 2>&1
  )
  (
    cd "$eval_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m eval_module.main list-comparisons \
      --results-dir "$eval_tmp" \
      --output "$eval_tmp/comparison_index.json" >/tmp/ai-infra-eval-comparison-index.log 2>&1
  )
  (
    cd "$eval_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m eval_module.main leaderboard \
      --results-dir "$eval_tmp" \
      --backend vllm \
      --num-fewshot 5 \
      --output "$eval_tmp/leaderboard.json" >/tmp/ai-infra-eval-leaderboard.log 2>&1
  )
  (
    cd "$eval_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m eval_module.main list-runs \
      --results-dir "$eval_tmp" \
      --model "$MODEL" \
      --backend vllm \
      --num-fewshot 5 \
      --output "$eval_tmp/run_index.json" >/tmp/ai-infra-eval-run-index.log 2>&1
  )

  check_path_exists "IT-08 eval baseline json" "$eval_tmp/baseline.json"
  check_path_exists "IT-08b eval sample outputs json" "$eval_tmp/baseline/sample_outputs.json"
  check_path_exists "IT-08c eval sample summary json" "$eval_tmp/baseline/sample_summary.json"
  check_path_exists "IT-08c2 eval sample analysis json" "$eval_tmp/baseline/sample_analysis.json"
  check_path_exists "IT-08d eval leaderboard json" "$eval_tmp/leaderboard.json"
  check_path_exists "IT-08e eval leaderboard markdown" "$eval_tmp/leaderboard.md"
  check_path_exists "IT-08f eval run index json" "$eval_tmp/run_index.json"
  check_path_exists "IT-08g eval run index markdown" "$eval_tmp/run_index.md"
  check_path_exists "IT-09 eval compare json" "$eval_tmp/compare.json"
  check_path_exists "IT-10 eval compare markdown" "$eval_tmp/compare.md"
  check_path_exists "IT-10a eval comparison index json" "$eval_tmp/comparison_index.json"
  check_path_exists "IT-10a2 eval comparison index markdown" "$eval_tmp/comparison_index.md"
  check_body_contains "IT-10b eval release recommendation" "release_recommendation" "cat '$eval_tmp/compare.json'"
  check_body_contains "IT-10b2 eval sample analysis score buckets" "score_buckets" "cat '$eval_tmp/baseline/sample_analysis.json'"
  check_body_contains "IT-10c eval leaderboard report type" "eval_leaderboard" "cat '$eval_tmp/leaderboard.json'"
  check_body_contains "IT-10d eval leaderboard best result file" "best_result_file" "cat '$eval_tmp/leaderboard.json'"
  check_body_contains "IT-10d2 eval leaderboard backend filter" "\"backend_filter\":\"vllm\"" "cat '$eval_tmp/leaderboard.json' | tr -d '[:space:]'"
  check_body_contains "IT-10d3 eval leaderboard fewshot filter" "\"num_fewshot_filter\":5" "cat '$eval_tmp/leaderboard.json' | tr -d '[:space:]'"
  check_body_contains "IT-10d4 eval leaderboard backend groups" "backend_groups" "cat '$eval_tmp/leaderboard.json'"
  check_body_contains "IT-10e eval run index report type" "eval_run_index" "cat '$eval_tmp/run_index.json'"
  check_body_contains "IT-10f eval run index result file" "result_file" "cat '$eval_tmp/run_index.json'"
  check_body_contains "IT-10f2 eval run index backend filter" "\"backend_filter\":\"vllm\"" "cat '$eval_tmp/run_index.json' | tr -d '[:space:]'"
  check_body_contains "IT-10f3 eval run index task summaries" "task_summaries" "cat '$eval_tmp/run_index.json'"
  check_body_contains "IT-10g eval comparison index report type" "eval_comparison_index" "cat '$eval_tmp/comparison_index.json'"
  check_body_contains "IT-10h eval comparison index release" "release_recommendation" "cat '$eval_tmp/comparison_index.json'"
  check_body_contains "IT-10i eval comparison verdict counts" "verdict_counts" "cat '$eval_tmp/comparison_index.json'"
  check_body_contains "IT-10j eval comparison recommendation counts" "recommendation_counts" "cat '$eval_tmp/comparison_index.json'"
  check_body_contains "IT-10k eval comparison task summaries" "task_summaries" "cat '$eval_tmp/comparison_index.json'"
}

run_finetune_smoke() {
  local finetune_dir="$ROOT_DIR/projects/finetune-demo"
  local finetune_tmp="$TMP_DIR/finetune"
  mkdir -p "$finetune_tmp"

  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main train \
      --method lora \
      --model "$MODEL" \
      --dataset "$finetune_dir/data/train.jsonl" \
      --output "$finetune_tmp/run" \
      --epochs 1 >/tmp/ai-infra-finetune-train.log 2>&1
  )
  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main export \
      --checkpoint "$finetune_tmp/run/checkpoint-0001" \
      --output "$finetune_tmp/exported" >/tmp/ai-infra-finetune-export.log 2>&1
  )
  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main list-datasets \
      --registry "$finetune_tmp/dataset_registry.jsonl" \
      --method lora \
      --model "$MODEL" \
      --output "$finetune_tmp/dataset_registry_report.json" \
      --markdown-output "$finetune_tmp/dataset_registry_report.md" >/tmp/ai-infra-finetune-datasets.log 2>&1
  )
  local dataset_id
  dataset_id="$("$PYTHON_BIN" -c 'import json, sys; print(json.loads(open(sys.argv[1]).readline())["dataset_id"])' "$finetune_tmp/dataset_registry.jsonl")"
  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main list-runs \
      --history "$finetune_tmp/run_history.jsonl" \
      --dataset-id "$dataset_id" \
      --model "$MODEL" \
      --method lora \
      --output "$finetune_tmp/run_index.json" \
      --markdown-output "$finetune_tmp/run_index.md" >/tmp/ai-infra-finetune-run-index.log 2>&1
  )
  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main diff-datasets \
      --registry "$finetune_tmp/dataset_registry.jsonl" \
      --left "$dataset_id" \
      --right "$dataset_id" \
      --output "$finetune_tmp/dataset_registry_diff.json" \
      --markdown-output "$finetune_tmp/dataset_registry_diff.md" >/tmp/ai-infra-finetune-dataset-diff.log 2>&1
  )
  (
    cd "$finetune_dir"
    env PYTHON="$PYTHON_BIN" PYTHONPATH=src \
      "$PYTHON_BIN" -m finetune_demo.main list-exports \
      --history "$finetune_tmp/export_history.jsonl" \
      --dataset-id "$dataset_id" \
      --model "$MODEL" \
      --output "$finetune_tmp/export_index.json" \
      --markdown-output "$finetune_tmp/export_index.md" >/tmp/ai-infra-finetune-export-index.log 2>&1
  )

  check_path_exists "IT-11 finetune run manifest" "$finetune_tmp/run/run_manifest.json"
  check_path_exists "IT-12 finetune checkpoint" "$finetune_tmp/run/checkpoint-0001/adapter_model.safetensors"
  check_path_exists "IT-12b finetune checkpoint index" "$finetune_tmp/run/checkpoints/checkpoint_index.json"
  check_body_contains "IT-12c finetune checkpoint index type" "finetune_checkpoint_index" "cat '$finetune_tmp/run/checkpoints/checkpoint_index.json'"
  check_path_exists "IT-13 finetune export manifest" "$finetune_tmp/exported/export_manifest.json"
  check_body_contains "IT-13b finetune dataset role stats" "role_counts" "cat '$finetune_tmp/run/data/dataset_summary.json'"
  check_body_contains "IT-13d finetune dataset version" "dataset_version" "cat '$finetune_tmp/run/data/dataset_summary.json'"
  check_body_contains "IT-13c finetune export lineage" "lineage" "cat '$finetune_tmp/exported/export_manifest.json'"
  check_body_contains "IT-13e finetune export history dataset version" "dataset_version" "cat '$finetune_tmp/export_history.jsonl'"
  check_body_contains "IT-13e2 finetune export history duration" "duration_seconds" "cat '$finetune_tmp/export_history.jsonl'"
  check_body_contains "IT-13e3 finetune export status" "\"status\":\"success\"" "cat '$finetune_tmp/export_history.jsonl' | tr -d '[:space:]'"
  check_body_contains "IT-13e4 finetune export manifest pointer" "export_manifest_file" "cat '$finetune_tmp/export_history.jsonl'"
  check_path_exists "IT-13f finetune dataset registry entry" "$finetune_tmp/run/data/dataset_registry_entry.json"
  check_body_contains "IT-13g finetune dataset registry history" "dataset_id" "cat '$finetune_tmp/dataset_registry.jsonl'"
  check_path_exists "IT-13h finetune dataset registry report" "$finetune_tmp/dataset_registry_report.json"
  check_path_exists "IT-13h2 finetune run index" "$finetune_tmp/run_index.json"
  check_body_contains "IT-13h3 finetune run index type" "finetune_run_index" "cat '$finetune_tmp/run_index.json'"
  check_body_contains "IT-13h4 finetune run index manifest pointer" "run_manifest_file" "cat '$finetune_tmp/run_index.json'"
  check_body_contains "IT-13h5 finetune run index checkpoint pointer" "checkpoint_index_file" "cat '$finetune_tmp/run_index.json'"
  check_body_contains "IT-13i finetune dataset registry report type" "finetune_dataset_registry" "cat '$finetune_tmp/dataset_registry_report.json'"
  check_body_contains "IT-13j finetune dataset registry duplicate count" "duplicate_entry_count" "cat '$finetune_tmp/dataset_registry_report.json'"
  check_body_contains "IT-13k finetune dataset registry method filter" "\"method_filter\":\"lora\"" "cat '$finetune_tmp/dataset_registry_report.json' | tr -d '[:space:]'"
  check_body_contains "IT-13l finetune dataset registry model filter" "\"model_filter\":\"$MODEL\"" "cat '$finetune_tmp/dataset_registry_report.json' | tr -d '[:space:]'"
  check_path_exists "IT-13m finetune dataset registry diff" "$finetune_tmp/dataset_registry_diff.json"
  check_body_contains "IT-13n finetune dataset registry diff type" "finetune_dataset_diff" "cat '$finetune_tmp/dataset_registry_diff.json'"
  check_body_contains "IT-13o finetune dataset registry diff identical sha" "\"identical_dataset_sha256\":true" "cat '$finetune_tmp/dataset_registry_diff.json' | tr -d '[:space:]'"
  check_path_exists "IT-13p finetune export index" "$finetune_tmp/export_index.json"
  check_body_contains "IT-13q finetune export index type" "finetune_export_index" "cat '$finetune_tmp/export_index.json'"
  check_body_contains "IT-13r finetune export index adapter hash" "adapter_model_sha256" "cat '$finetune_tmp/export_index.json'"
  check_body_contains "IT-13s finetune export index duration" "average_duration_seconds" "cat '$finetune_tmp/export_index.json'"
  check_body_contains "IT-13t finetune export model summaries" "model_summaries" "cat '$finetune_tmp/export_index.json'"
  check_body_contains "IT-13u finetune export dataset summaries" "dataset_summaries" "cat '$finetune_tmp/export_index.json'"
}

start_inference_if_needed
start_gateway_if_needed

check_body_contains "IT-00 gateway upstream health" "\"vllm-local\":\"healthy\"" "curl -s http://localhost:${GATEWAY_PORT}/health | tr -d '[:space:]'"
check_body_contains "IT-00b gateway fallback upstream health" "\"vllm-backup\":\"healthy\"" "curl -s http://localhost:${GATEWAY_PORT}/health | tr -d '[:space:]'"
check_body_contains "IT-00c inference model list" "\"id\":\"${MODEL}\"" "curl -s http://localhost:${INFERENCE_PORT}/v1/models | tr -d '[:space:]'"
check_body_contains "IT-00d gateway model list" "\"id\":\"vllm-local\"" "curl -s http://localhost:${GATEWAY_PORT}/v1/models | tr -d '[:space:]'"
check_body_contains "IT-00e gateway model fallback metadata" "\"fallback_count\":1" "curl -s http://localhost:${GATEWAY_PORT}/v1/models | tr -d '[:space:]'"
check_code "IT-01b direct inference" "200" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${INFERENCE_PORT}/v1/chat/completions -H 'Content-Type: application/json' -d '{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'"
check_code "IT-01b4 direct inference request timeline seed" "200" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${INFERENCE_PORT}/v1/chat/completions -H 'X-Request-ID: req_smoke_inference_1' -H 'Content-Type: application/json' -d '{\"model\":\"${MODEL}\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi timeline\"}]}'"
check_code "IT-01b2 direct inference unknown model" "404" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${INFERENCE_PORT}/v1/chat/completions -H 'Content-Type: application/json' -d '{\"model\":\"unknown-model\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'"
check_code "IT-01b3 direct inference empty messages" "422" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${INFERENCE_PORT}/v1/chat/completions -H 'Content-Type: application/json' -d '{\"model\":\"${MODEL}\",\"messages\":[]}'"
check_code "IT-01 gateway proxy" "200" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'"
check_body_contains "IT-01c gateway stream proxy" "data: \\[DONE\\]" "curl -sN -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi stream\"}],\"stream\":true}'"
check_body_contains "IT-01d gateway request id" "x-request-id: req_smoke_gateway_1" "curl -sD - -o /dev/null -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'X-Request-ID: req_smoke_gateway_1' -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi request id\"}]}' | tr '[:upper:]' '[:lower:]'"
check_body_contains "IT-01e gateway cache bypass header" "x-cache: bypass" "curl -sD - -o /dev/null -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi cache header\"}]}' | tr '[:upper:]' '[:lower:]'"
check_body_contains "IT-01f gateway upstream model header" "x-upstream-model: vllm-local" "curl -sD - -o /dev/null -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi upstream header\"}]}' | tr '[:upper:]' '[:lower:]'"
check_code "IT-04 no auth" "401" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Content-Type: application/json' -d '{\"model\":\"vllm-local\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'"
check_code "IT-06 unknown model" "404" "curl -s -o /dev/null -w '%{http_code}' -X POST http://localhost:${GATEWAY_PORT}/v1/chat/completions -H 'Authorization: Bearer dev-gateway-key-1' -H 'Content-Type: application/json' -d '{\"model\":\"unknown-model\",\"messages\":[{\"role\":\"user\",\"content\":\"Hi\"}]}'"
check_body_contains "IT-07 gateway metrics" "ai_gateway_" "curl -s http://localhost:${GATEWAY_PORT}/metrics"
check_body_contains "IT-07b inference metrics requests" "vllm_num_requests_total" "curl -s http://localhost:${INFERENCE_PORT}/metrics"
check_body_contains "IT-07c inference prompt token metric" "vllm_prompt_tokens_total" "curl -s http://localhost:${INFERENCE_PORT}/metrics"
check_body_contains "IT-07d inference completion token metric" "vllm_completion_tokens_total" "curl -s http://localhost:${INFERENCE_PORT}/metrics"
check_body_contains "IT-07d2 inference structured events" "request_success" "curl -s http://localhost:${INFERENCE_PORT}/events"
check_body_contains "IT-07d3 inference event filters" "req_" "curl -s 'http://localhost:${INFERENCE_PORT}/events?event_type=request_success&requested_model=${MODEL}'"
check_body_contains "IT-07d4 inference event summary" "event_type_counts" "curl -s 'http://localhost:${INFERENCE_PORT}/events/summary?event_type=request_success&requested_model=${MODEL}'"
check_body_contains "IT-07d5 inference request timeline" "request_success" "curl -s 'http://localhost:${INFERENCE_PORT}/events/requests/req_smoke_inference_1'"
check_body_contains "IT-07d6 inference request index" "matched_request_count" "curl -s 'http://localhost:${INFERENCE_PORT}/events/requests?requested_model=${MODEL}'"
check_body_contains "IT-07e gateway fallback metrics" "ai_gateway_fallback_attempts_total" "curl -s http://localhost:${GATEWAY_PORT}/metrics"
check_body_contains "IT-07f gateway structured events" "request_success" "curl -s http://localhost:${GATEWAY_PORT}/events"
check_body_contains "IT-07g gateway event filters" "request_success" "curl -s 'http://localhost:${GATEWAY_PORT}/events?event_type=request_success&upstream_model=vllm-local'"
check_body_contains "IT-07h gateway event summary" "upstream_model_counts" "curl -s 'http://localhost:${GATEWAY_PORT}/events/summary?event_type=request_success&upstream_model=vllm-local'"
check_body_contains "IT-07h2 gateway failure summary" "status_code_counts" "curl -s 'http://localhost:${GATEWAY_PORT}/events/failures'"
check_body_contains "IT-07i gateway request timeline" "upstream_attempt" "curl -s 'http://localhost:${GATEWAY_PORT}/events/requests/req_smoke_gateway_1'"
check_body_contains "IT-07j gateway request index" "matched_request_count" "curl -s 'http://localhost:${GATEWAY_PORT}/events/requests?requested_model=vllm-local&upstream_model=vllm-local'"
save_serving_evidence
run_eval_smoke
run_finetune_smoke
build_evidence_packet
check_path_exists "IT-14 evidence packet json" "$TMP_DIR/evidence/evidence_packet.json"
check_path_exists "IT-14b evidence packet markdown" "$TMP_DIR/evidence/evidence_packet.md"
check_body_contains "IT-14c evidence packet type" "ai_infra_evidence_packet" "cat '$TMP_DIR/evidence/evidence_packet.json'"
check_body_contains "IT-14d evidence packet sections" "serving_gateway" "cat '$TMP_DIR/evidence/evidence_packet.json'"

if [ "$FAILURES" -ne 0 ]; then
  exit 1
fi
