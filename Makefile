.PHONY: help
.PHONY: infra-install infra-dev-install infra-lint infra-format infra-test scripts-test security-check public-check infra-check infra-serve infra-smoke infra-evidence infra-release release-brief course-catalog workshop-packet assessment-pack roadmap-pack infra-clean docs-build docs-quality docs-inventory
.PHONY: \
	inference-install inference-serve inference-health inference-test \
	gateway-install gateway-serve gateway-health gateway-test \
	eval-install eval-run-mmlu eval-run-gsm8k eval-compare eval-test \
	finetune-install finetune-train finetune-save finetune-export finetune-test \
	all-serve all-stop

ROOT_DIR := $(abspath $(dir $(lastword $(MAKEFILE_LIST))))
MODEL ?= Qwen/Qwen2.5-0.5B-Instruct
PYTHON ?= python3
PYTHON_FOR_SUBMAKE := $(if $(findstring /,$(PYTHON)),$(abspath $(PYTHON)),$(PYTHON))
INFERENCE_PORT ?= 8000
GATEWAY_PORT ?= 8080
INFERENCE_BASE_URL ?= http://localhost:$(INFERENCE_PORT)/v1
EVAL_OUTPUT ?= ./results/mmlu_eval_result.json
EVAL_BASELINE ?= $(EVAL_OUTPUT)
EVAL_CANDIDATE ?= $(EVAL_OUTPUT)
EVAL_COMPARE_OUTPUT ?= ./results/mmlu_compare.json
FINETUNE_OUTPUT ?= ./outputs/demo-run
FINETUNE_CHECKPOINT ?= $(FINETUNE_OUTPUT)/checkpoint-0001
FINETUNE_EXPORT_OUTPUT ?= ./outputs/demo-export
EVIDENCE_SMOKE_DIR ?= ./.tmp/smoke
EVIDENCE_OUTPUT ?= ./.tmp/evidence/evidence_packet.json
EVIDENCE_MARKDOWN ?= ./.tmp/evidence/evidence_packet.md
LEARNING_INVENTORY_OUTPUT ?= ./.tmp/docs-inventory/learning_inventory.json
LEARNING_INVENTORY_MARKDOWN ?= ./.tmp/docs-inventory/learning_inventory.md
COURSE_CATALOG_INVENTORY ?= $(LEARNING_INVENTORY_OUTPUT)
COURSE_CATALOG_OUTPUT ?= ./.tmp/course-catalog/course_catalog.json
COURSE_CATALOG_MARKDOWN ?= ./.tmp/course-catalog/course_catalog.md
RELEASE_BRIEF_INVENTORY ?= $(LEARNING_INVENTORY_OUTPUT)
RELEASE_BRIEF_EVIDENCE ?= $(EVIDENCE_OUTPUT)
RELEASE_BRIEF_OUTPUT ?= ./.tmp/release/release_brief.json
RELEASE_BRIEF_MARKDOWN ?= ./.tmp/release/release_brief.md
WORKSHOP_PACKET_CATALOG ?= $(COURSE_CATALOG_OUTPUT)
WORKSHOP_PACKET_RELEASE ?= $(RELEASE_BRIEF_OUTPUT)
WORKSHOP_PACKET_OUTPUT ?= ./.tmp/workshop/workshop_packet.json
WORKSHOP_PACKET_MARKDOWN ?= ./.tmp/workshop/workshop_packet.md
ASSESSMENT_PACK_CATALOG ?= $(COURSE_CATALOG_OUTPUT)
ASSESSMENT_PACK_WORKSHOP ?= $(WORKSHOP_PACKET_OUTPUT)
ASSESSMENT_PACK_OUTPUT ?= ./.tmp/assessment/assessment_pack.json
ASSESSMENT_PACK_MARKDOWN ?= ./.tmp/assessment/assessment_pack.md
ROADMAP_PACK_RELEASE ?= $(RELEASE_BRIEF_OUTPUT)
ROADMAP_PACK_ASSESSMENT ?= $(ASSESSMENT_PACK_OUTPUT)
ROADMAP_PACK_OUTPUT ?= ./.tmp/roadmap/roadmap_pack.json
ROADMAP_PACK_MARKDOWN ?= ./.tmp/roadmap/roadmap_pack.md

help:
	@grep -E '^[a-zA-Z_-]+:' Makefile | \
		grep -v '.PHONY' | \
		sed 's/:.*//' | \
		sort | uniq

infra-install: inference-install gateway-install eval-install finetune-install

infra-dev-install: infra-install
	@$(PYTHON_FOR_SUBMAKE) -m pip install -r requirements-dev.txt

infra-lint:
	@$(PYTHON_FOR_SUBMAKE) -m ruff check projects scripts

infra-format:
	@$(PYTHON_FOR_SUBMAKE) -m ruff format projects scripts
	@$(PYTHON_FOR_SUBMAKE) -m ruff check --fix projects scripts

infra-test: inference-test gateway-test eval-test finetune-test scripts-test

docs-build:
	@npm run docs:build

docs-quality:
	@$(PYTHON_FOR_SUBMAKE) scripts/docs_quality_check.py

docs-inventory:
	@$(PYTHON_FOR_SUBMAKE) scripts/build_learning_inventory.py \
		--docs-dir docs \
		--root-dir . \
		--output $(LEARNING_INVENTORY_OUTPUT) \
		--markdown-output $(LEARNING_INVENTORY_MARKDOWN) \
		--strict

course-catalog: docs-inventory
	@$(PYTHON_FOR_SUBMAKE) scripts/build_course_catalog.py \
		--inventory $(COURSE_CATALOG_INVENTORY) \
		--output $(COURSE_CATALOG_OUTPUT) \
		--markdown-output $(COURSE_CATALOG_MARKDOWN) \
		--strict

scripts-test:
	@$(PYTHON_FOR_SUBMAKE) -m pytest scripts/tests -v

security-check:
	@$(PYTHON_FOR_SUBMAKE) scripts/security_scan.py

public-check: security-check infra-check

infra-check: infra-lint infra-test docs-quality docs-build

infra-serve: inference-serve gateway-serve

infra-smoke:
	@if [ -f scripts/integration_smoke_test.sh ]; then \
		PYTHON=$(PYTHON_FOR_SUBMAKE) MODEL=$(MODEL) INFERENCE_PORT=$(INFERENCE_PORT) GATEWAY_PORT=$(GATEWAY_PORT) bash scripts/integration_smoke_test.sh; \
	else \
		echo "scripts/integration_smoke_test.sh not implemented yet"; \
		exit 1; \
	fi

infra-evidence:
	@$(PYTHON_FOR_SUBMAKE) scripts/build_evidence_packet.py \
		--smoke-dir $(EVIDENCE_SMOKE_DIR) \
		--output $(EVIDENCE_OUTPUT) \
		--markdown-output $(EVIDENCE_MARKDOWN)

release-brief: docs-inventory infra-evidence
	@$(PYTHON_FOR_SUBMAKE) scripts/build_release_brief.py \
		--inventory $(RELEASE_BRIEF_INVENTORY) \
		--evidence $(RELEASE_BRIEF_EVIDENCE) \
		--output $(RELEASE_BRIEF_OUTPUT) \
		--markdown-output $(RELEASE_BRIEF_MARKDOWN) \
		--strict

workshop-packet: course-catalog release-brief
	@$(PYTHON_FOR_SUBMAKE) scripts/build_workshop_packet.py \
		--course-catalog $(WORKSHOP_PACKET_CATALOG) \
		--release-brief $(WORKSHOP_PACKET_RELEASE) \
		--output $(WORKSHOP_PACKET_OUTPUT) \
		--markdown-output $(WORKSHOP_PACKET_MARKDOWN) \
		--strict

assessment-pack: course-catalog workshop-packet
	@$(PYTHON_FOR_SUBMAKE) scripts/build_assessment_pack.py \
		--course-catalog $(ASSESSMENT_PACK_CATALOG) \
		--workshop-packet $(ASSESSMENT_PACK_WORKSHOP) \
		--output $(ASSESSMENT_PACK_OUTPUT) \
		--markdown-output $(ASSESSMENT_PACK_MARKDOWN) \
		--strict

roadmap-pack: release-brief assessment-pack
	@$(PYTHON_FOR_SUBMAKE) scripts/build_roadmap_pack.py \
		--release-brief $(ROADMAP_PACK_RELEASE) \
		--assessment-pack $(ROADMAP_PACK_ASSESSMENT) \
		--output $(ROADMAP_PACK_OUTPUT) \
		--markdown-output $(ROADMAP_PACK_MARKDOWN) \
		--strict

infra-release: infra-format docs-inventory course-catalog public-check infra-smoke infra-evidence release-brief workshop-packet assessment-pack roadmap-pack
	@echo "Release checks completed. See $(RELEASE_BRIEF_MARKDOWN)"

infra-clean:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) -C projects/inference-service clean || true
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) -C projects/ai-gateway clean || true
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) -C projects/eval-module clean || true
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) -C projects/finetune-demo clean || true

inference-install:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) install -C projects/inference-service

inference-serve:
	@cd projects/inference-service && nohup env PYTHON=$(PYTHON_FOR_SUBMAKE) MODEL=$(MODEL) PORT=$(INFERENCE_PORT) bash scripts/serve.sh >/tmp/ai-infra-inference.log 2>&1 &

inference-health:
	@curl -s http://localhost:$(INFERENCE_PORT)/health | $(PYTHON) -m json.tool

inference-test:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) test -C projects/inference-service

gateway-install:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) install -C projects/ai-gateway

gateway-serve:
	@cd projects/ai-gateway && nohup env PYTHON=$(PYTHON_FOR_SUBMAKE) PORT=$(GATEWAY_PORT) bash scripts/serve.sh >/tmp/ai-infra-gateway.log 2>&1 &

gateway-health:
	@curl -s http://localhost:$(GATEWAY_PORT)/health | $(PYTHON) -m json.tool

gateway-test:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) test -C projects/ai-gateway

eval-install:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) install -C projects/eval-module

eval-run-mmlu:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) run-mmlu MODEL=$(MODEL) BACKEND_URL=$(INFERENCE_BASE_URL) OUTPUT=$(EVAL_OUTPUT) -C projects/eval-module

eval-run-gsm8k:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) run-gsm8k MODEL=$(MODEL) BACKEND_URL=$(INFERENCE_BASE_URL) -C projects/eval-module

eval-test:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) test -C projects/eval-module

eval-compare:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) compare BASELINE=$(EVAL_BASELINE) CANDIDATE=$(EVAL_CANDIDATE) OUTPUT=$(EVAL_COMPARE_OUTPUT) -C projects/eval-module

finetune-install:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) install -C projects/finetune-demo

finetune-train:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) train MODEL=$(MODEL) OUTPUT=$(FINETUNE_OUTPUT) -C projects/finetune-demo

finetune-save:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) save CHECKPOINT=$(FINETUNE_CHECKPOINT) OUTPUT=$(FINETUNE_EXPORT_OUTPUT) -C projects/finetune-demo

finetune-export:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) export CHECKPOINT=$(FINETUNE_CHECKPOINT) OUTPUT=$(FINETUNE_EXPORT_OUTPUT) -C projects/finetune-demo

finetune-test:
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) test -C projects/finetune-demo

all-serve: inference-serve
	@sleep 3
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) INFERENCE_PORT=$(INFERENCE_PORT) inference-health
	@$(MAKE) PYTHON=$(PYTHON_FOR_SUBMAKE) GATEWAY_PORT=$(GATEWAY_PORT) gateway-serve

all-stop:
	@pkill -f "inference_service.main" 2>/dev/null || true
	@pkill -f "ai_gateway.main" 2>/dev/null || true
