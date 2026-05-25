.PHONY: help install serve health test clean

PYTHON ?= python3

help:
	@printf "install\nserve\nhealth\ntest\nclean\n"

install:
	@$(PYTHON) -m pip install -e ".[test]"

serve:
	@PYTHONPATH=src $(PYTHON) -m ai_gateway.main serve \
		--port $${PORT:-8080} \
		--host $${HOST:-0.0.0.0}

health:
	@curl -s http://localhost:$${PORT:-8080}/health | $(PYTHON) -m json.tool

test:
	@if [ -d tests ]; then PYTHONPATH=src $(PYTHON) -m pytest tests -v; else echo "tests/ not implemented yet"; fi

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
