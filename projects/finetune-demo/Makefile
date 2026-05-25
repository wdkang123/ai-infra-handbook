.PHONY: help install train save export test clean

PYTHON ?= python3

help:
	@printf "install\ntrain\nsave\nexport\ntest\nclean\n"

install:
	@$(PYTHON) -m pip install -e ".[test]"

train:
	@PYTHONPATH=src $(PYTHON) -m finetune_demo.main train \
		--method $${METHOD:-lora} \
		--model $${MODEL:-Qwen/Qwen2.5-0.5B-Instruct} \
		--dataset $${DATASET:-./data/train.jsonl} \
		--output $${OUTPUT:-./outputs}

save:
	@PYTHONPATH=src $(PYTHON) -m finetune_demo.main save \
		--checkpoint "$${CHECKPOINT:?CHECKPOINT is required}" \
		--output "$${OUTPUT:?OUTPUT is required}"

export:
	@PYTHONPATH=src $(PYTHON) -m finetune_demo.main export \
		--checkpoint "$${CHECKPOINT:?CHECKPOINT is required}" \
		--output "$${OUTPUT:?OUTPUT is required}"

test:
	@if [ -d tests ]; then PYTHONPATH=src $(PYTHON) -m pytest tests -v; else echo "tests/ not implemented yet"; fi

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
