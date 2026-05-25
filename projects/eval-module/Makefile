.PHONY: help install run-mmlu run-gsm8k compare test clean

PYTHON ?= python3

help:
	@printf "install\nrun-mmlu\nrun-gsm8k\ncompare\ntest\nclean\n"

install:
	@$(PYTHON) -m pip install -e ".[test]"

run-mmlu:
	@PYTHONPATH=src $(PYTHON) -m eval_module.main run \
		--task mmlu \
		--model $${MODEL:-Qwen/Qwen2.5-0.5B-Instruct} \
		--backend-url $${BACKEND_URL:-http://localhost:8000/v1} \
		--output $${OUTPUT:-./results/mmlu_eval_result.json}

run-gsm8k:
	@PYTHONPATH=src $(PYTHON) -m eval_module.main run \
		--task gsm8k \
		--model $${MODEL:-Qwen/Qwen2.5-0.5B-Instruct} \
		--backend-url $${BACKEND_URL:-http://localhost:8000/v1} \
		--output $${OUTPUT:-./results/gsm8k_eval_result.json}

compare:
	@PYTHONPATH=src $(PYTHON) -m eval_module.main compare \
		--baseline "$${BASELINE:?BASELINE is required}" \
		--candidate "$${CANDIDATE:?CANDIDATE is required}" \
		--output "$${OUTPUT:-./results/compare_report.json}"

test:
	@if [ -d tests ]; then PYTHONPATH=src $(PYTHON) -m pytest tests -v; else echo "tests/ not implemented yet"; fi

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
