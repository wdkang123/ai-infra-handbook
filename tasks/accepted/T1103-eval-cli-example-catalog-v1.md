# eval-module CLI Example Catalog v1

## Task ID: T1103
## Title: eval-module Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module CLI Example Catalog

本文档定义 eval-module CLI 命令行接口的用法示例，对应真实文件 `eval-module/src/eval_module/main.py`（待实现）。

## CLI 入口

```bash
python -m eval_module.main --help
```

```
usage: eval_module.main [-h] {run,compare,list-tasks} ...

eval-module: evaluation CLI for ai-infra

optional arguments:
  -h, --help  show this help message

commands:
  {run,compare,list-tasks}
```

---

## 1. run — 运行评测

```bash
python -m eval_module.main run \
  --task <task_id> \
  --model <model_name> \
  --backend-url <url> \
  --output <path>
```

### 示例 1: MMLU

```bash
python -m eval_module.main run \
  --task mmlu \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1
```

### 示例 2: GSM8K

```bash
python -m eval_module.main run \
  --task gsm8k \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1
```

### 示例 3: HumanEval

```bash
python -m eval_module.main run \
  --task humaneval \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1
```

### run 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--task` | 必填 | 任务 ID（mmlu / gsm8k / humaneval / truthfulqa） |
| `--model` | 必填 | HuggingFace 模型名或路径 |
| `--backend-url` | `http://localhost:8000/v1` | 推理后端 |
| `--num-fewshot` | `5` | few-shot 样本数 |
| `--limit` | `None` | 限制样本数（快速测试） |
| `--output` | `./results/eval_result.json` | 输出 JSON 文件 |

---

## 2. compare — 对比评测

```bash
python -m eval_module.main compare \
  --baseline <result.json> \
  --candidate <result.json> \
  --output <path>
```

### 示例：对比 baseline 和 finetuned 模型

```bash
python -m eval_module.main compare \
  --baseline ./results/baseline.json \
  --candidate ./results/candidate.json
```

### compare 参数说明

| 参数 | 默认值 | 说明 |
|---|---|---|
| `--baseline` | 必填 | baseline 结果 JSON 文件路径 |
| `--candidate` | 必填 | candidate 结果 JSON 文件路径 |
| `--output` | `None` | 输出文件（可选） |

---

## 3. list-tasks — 列出可用任务

```bash
python -m eval_module.main list-tasks
```

输出：
```
Available benchmark tasks:
  mmlu       — Massively Multitask Language Understanding
  gsm8k      — Grade School Math 8K
  humaneval  — HumanEval Code Completion
  truthfulqa — TruthfulQA
```

---

## 完整工作流示例

```bash
# 1. 启动 inference-service（来自 T1005 local_dev_sequence.sh）
bash scripts/local_dev_sequence.sh start

# 2. 运行 MMLU 评测
python -m eval_module.main run \
  --task mmlu \
  --model Qwen2.5-0.5B-Instruct \
  --backend-url http://localhost:8000/v1

# 3. 停止服务
bash scripts/local_dev_sequence.sh stop

# 4. 对比报告（如 T1103-eval-compare-report-samples-v1.md）
python -m eval_module.main compare \
  --baseline ./results/baseline.json \
  --candidate ./results/candidate.json \
  --output results/compare/gsm8k.json
```

---

## 与 Starter Blueprint 对齐（T1003 eval-module）

| Blueprint 命令 | CLI 对应 |
|---|---|
| `make run-mmlu` | `python -m eval_module.main run --task mmlu` |
| `make run-gsm8k` | `python -m eval_module.main run --task gsm8k` |
| `eval-module compare` | `python -m eval_module.main compare --baseline ... --candidate ...` |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — lm-eval CLI interface
2. https://github.com/opencompass/opencompass — OpenCompass CLI

Risk of Staleness:
- CLI interface is project-internal; defined per T303 eval-module MVP design
