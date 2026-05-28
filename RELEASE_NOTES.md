# Release Notes

## v0.1.0 - Public Learning Launch

AI Infra Handbook v0.1.0 is the first public learning release. It is a learning project, not a production platform.

This release helps backend, platform, and AI application developers understand AI Infra through runnable code, structured documentation, hands-on labs, and evidence-driven review.

Highlights:

- Four runnable learning projects: `inference-service`, `ai-gateway`, `eval-module`, `finetune-demo`.
- A 15-minute quickstart path through `make quickstart`.
- OpenAI-compatible learning endpoints for chat completions and model listing.
- Request evidence through `x-request-id`, events, request timelines, metrics, and failure summaries.
- Eval reports with run, compare, leaderboard, sample analysis, and release recommendation.
- Finetune asset lineage through dataset registry, run manifest, checkpoint index, export manifest, and history.
- Public learning materials: labs, case studies, output gallery, workshop kit, assessments, publication checklist, starter issues, and migration design notes.

Validation before publishing:

```bash
PYTHON=.venv/bin/python make docs-quality
PYTHON=.venv/bin/python make infra-check
PYTHON=.venv/bin/python make infra-smoke
PYTHON=.venv/bin/python make public-check
```

Known boundaries:

- This is not a production serving platform.
- The default backend is still a learning/mock path.
- Real vLLM, SGLang, OpenTelemetry, Prometheus, and richer eval release gates are staged as migration work.
- External secrets, local machine paths, model weights, caches, logs, and real `.env` files should not be committed.

Next stage:

- Add a real vLLM adapter path while preserving the current API contract.
- Add versioned OpenTelemetry GenAI tracing mapping.
- Align current and real backend metrics with Prometheus-style dashboards.
- Expand eval regression gates and failure case labs.
- Convert starter issue seeds into GitHub issues after the first public release.
