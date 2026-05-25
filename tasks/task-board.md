# Task Board

## Rules

- 只有带完整任务卡的任务才允许进入 `READY`
- MiniMax 只处理 `owner: MINIMAX` 的 `READY` 任务
- 白天微任务模式每轮控制在 3 到 6 个任务
- 夜间/长跑模式优先使用 `PACK-长跑专题包`
- 0 接管长跑模式优先使用 `PACK-0接管链式专题包`
- 更长时段优先使用 `PACK-深研究0接管专题包`
- 轻量专题包允许包含 3 到 6 个交付物
- 0 接管链式专题包允许包含 6 到 8 个交付物
- 深研究 0 接管专题包优先包含 8 个交付物
- `REVIEW_PENDING` 中的内容必须先经 Codex 审阅，不能直接入库

## Status Snapshot

- [x] 最初目标里的“学习手册主线”已完成到可正式开始学习的阶段
- [x] 文档站已可通过 `npm run docs:dev` 启动，并已验证 `npm run docs:build`
- [x] 四个项目的最小可运行闭环已打通
- [x] 文档、代码、运行手册、第一次实操入口已基本对齐
- [ ] 后续工作以抛光、按学习卡点细化、逐步替换更真实实现为主

## ACCEPTED

- [x] T000 建立 v1.1 方案主文档
- [x] T001 建立最小仓库骨架
- [x] T002 建立 README 初版
- [x] T003 建立 MiniMax/Codex 协议初版
- [x] T201 CODEX 编写“什么是 AI Infra”第一章
- [x] T111 vLLM 资料包修订版
- [x] T122 SGLang 资料包收紧版
- [x] T113 Triton IS 资料包重做版
- [x] T124 Glossary Router 术语收紧版
- [x] T134 vLLM 章节模板化初稿
- [x] T142 推理服务 comparison-index v1 收紧版
- [x] T145 SGLang 章节修订版
- [x] T147 inference stack sources-index v1
- [x] T151 TensorRT-LLM 资料包补官方文档入口
- [x] T153 Glossary 第二批术语收紧
- [x] T156 Triton IS 章节再修
- [x] T162 Observability/Evaluation 官方资料
- [x] T173 LoRA/QLoRA/PEFT 官方资料
- [x] T174 Unsloth 官方资料
- [x] T175 Benchmark 官方资料
- [x] T176 Night Sources Digest v1
- [x] T181 AI Gateway 资料包收紧版
- [x] T182 Cache 资料包收紧版
- [x] T183 Router 资料包收紧版
- [x] T163 inference stack comparison-index v2
- [x] T191 TensorRT-LLM 章节初稿
- [x] T301 inference-service MVP 设计
- [x] T302 ai-gateway MVP 设计
- [x] T303 eval-module MVP 设计
- [x] T304 finetune-demo MVP 设计
- [x] T164 gateway / cache / router sources-index v1
- [x] T165 finetuning sources-index v1
- [x] T198 Unsloth 章节初稿
- [x] T193 AI Gateway 章节初稿 → 已修订为 T203，并已通过
- [x] T194 Observability 章节初稿 → 已修订为 T204，并已通过
- [x] T203 AI Gateway 章节修订
- [x] T204 Observability 章节修订
- [x] T195 Evaluation 章节初稿 → 已修订为 T205，并已通过
- [x] T197 LoRA / PEFT 章节初稿 → 已修订为 T207，并已通过
- [x] T205 Evaluation 章节修订
- [x] T207 LoRA / PEFT 章节修订
- [x] T306 benchmark / evaluation sources-index v1
- [x] T196 Cache / Prefix Caching 章节初稿 → 已修订为 T206，再修订为 T208
- [x] T208 Cache 章节修订 round 2
- [x] T209 finetuning comparison-index 收紧
- [x] T307 observability sources-index v1
- [x] T308 evaluation / benchmark comparison-index v1 → 已收紧为 T309，并已通过
- [x] T309 evaluation / benchmark comparison-index 收紧
- [x] T310 observability comparison-index v1
- [x] T311 Benchmark / Leaderboard 章节初稿 → 已修订为 T312，并已通过
- [x] T312 Benchmark / Leaderboard 章节修订
- [x] T313 observability / evaluation glossary batch 03
- [x] T314 finetuning glossary batch 04 → 已收紧为 T315，并已通过
- [x] T315 finetuning glossary batch 04 收紧
- [x] T316 observability / evaluation comparison-index v2
- [x] T317 benchmark / leaderboard glossary batch 05
- [x] T401 Observability Long-Run Pack v1 → 已完成并通过
- [x] T402 Evaluation / Benchmark Long-Run Pack v1 → 已完成，已收紧为 T404
- [x] T403 Finetuning Long-Run Pack v1 → 已完成并通过
- [x] T404 Evaluation / Benchmark Long-Run Pack v1 收紧修订 → 已完成
- [x] T501 Observability Long-Run Pack v2 → 已完成
- [x] T502 Evaluation / Benchmark Long-Run Pack v2 → 已完成
- [x] T503 Finetuning Long-Run Pack v2 → 已完成
- [x] T601 Inference Core Zero-Touch Pack → 已完成
- [x] T602 Observability / Evaluation Zero-Touch Pack → 已完成
- [x] T603 Finetuning / Training Zero-Touch Pack → 已完成
- [x] T604 Cross-Project Systemization Pack → 已完成
- [x] T701 Inference Engines Deep-Research Pack → 已完成并通过
- [x] T702 Observability / Evaluation Deep-Research Pack → 已完成并通过
- [x] T703 Finetuning / Training Deep-Research Pack → 已完成，已收紧为 T713
- [x] T704 Cross-Project Deep-Research Pack → 已完成，已收紧为 T714
- [x] T705 Execution Decomposition Pack → 已完成，已收紧为 T715
- [x] T713 Finetuning Decision Memo Tighten → 已完成并通过
- [x] T714 Project Dependency Matrix Tighten → 已完成并通过
- [x] T715 Project Task Breakdown Tighten → 已完成并通过
- [x] T801 inference-service Execution Prep Pack → 已完成，已收紧为 T811
- [x] T802 ai-gateway Execution Prep Pack → 已完成，已收紧为 T812
- [x] T803 eval-module Execution Prep Pack → 已完成，已收紧为 T813
- [x] T804 finetune-demo Execution Prep Pack → 已完成并通过
- [x] T805 Cross-Project Integration Prep Pack → 已完成，已收紧为 T815
- [x] T811 inference-service API Contract Tighten → 已完成并通过
- [x] T812 ai-gateway API Contract Tighten → 已完成并通过
- [x] T813 eval-module Validation Checklist Tighten → 已完成并通过
- [x] T815 Codex Implementation Order Tighten → 已完成并通过
- [x] T901 inference-service Scaffold Pack → 已完成，已收紧为 T921
- [x] T902 ai-gateway Scaffold Pack → 已完成，已收紧为 T922
- [x] T903 eval-module Scaffold Pack → 已完成，已收紧为 T923
- [x] T904 finetune-demo Scaffold Pack → 已完成，已收紧为 T924
- [x] T905 Developer Workflow Scaffold Pack → 已完成，已收紧为 T925
- [x] T921 inference-service Scaffold Install Tighten → 已就地修订并通过
- [x] T922 ai-gateway Scaffold Install Tighten → 已就地修订并通过
- [x] T923 eval-module Scaffold Install Tighten → 已就地修订并通过
- [x] T924 finetune-demo Scaffold Install Tighten → 已就地修订并通过
- [x] T925 Developer Workflow Scaffold Tighten → 已就地修订并通过
- [x] T1003 eval-module Starter File Pack → 已完成并通过
- [x] T1004 finetune-demo Starter File Pack → 已完成并通过
- [x] T1012 ai-gateway Starter File Pack Revision → 已完成并通过
- [x] T1001 inference-service Starter File Pack → 已完成并通过
- [x] T1005 Root / Dev Workflow Starter File Pack → 已完成并通过
- [x] T1021 inference-service Stream Syntax Fix → 已完成并通过
- [x] T1025 Root Smoke MODEL Pass-through Fix → 已完成并通过
- [x] T1104 finetune-demo Fixture Pack → 已完成并通过
- [x] T1112 ai-gateway Fixture Pack Revision → 已完成并通过
- [x] T1115 Root Integration Fixture Pack Revision → 已完成并通过
- [x] T1101 inference-service Fixture Pack → 已完成并通过
- [x] T1103 eval-module Fixture Pack → 已完成并通过
- [x] T1131 inference Request Fixture Rename Fix → 已完成并通过
- [x] T1133 eval Backend And CLI Fix → 已完成并通过
- [x] T1212 ai-gateway Implementation Map Revision → 已完成并通过
- [x] T1225 Root Integration Implementation Map Tighten Round 2 → 已完成并通过
- [x] T1231 inference-service Implementation Map Tighten Round 3 → 已完成并通过
- [x] T1233 eval-module Implementation Map Tighten Round 3 → 已完成并通过
- [x] T1234 finetune-demo Implementation Map Tighten Round 3 → 已完成并通过
- [x] T1301 inference-service Execution Slice Pack → 已完成并通过
- [x] T1302 ai-gateway Execution Slice Pack → 已完成并通过
- [x] T1313 eval-module Execution Slice Pack Revision → 已完成并通过
- [x] T1314 finetune-demo Execution Slice Pack Revision → 已完成并通过
- [x] T1315 Root Integration Execution Slice Pack Revision → 已完成并通过
- [x] T1401 inference-service Codex Task Pack → 已完成并通过
- [x] T1402 ai-gateway Codex Task Pack → 已完成并通过
- [x] T1403 eval-module Codex Task Pack → 已完成并通过
- [x] T1404 finetune-demo Codex Task Pack → 已完成并通过
- [x] T1405 Root Integration Codex Task Pack → 已完成并通过

## READY
- [ ] （无新增 MiniMax 任务；下一阶段建议由 Codex 直接开始实现）

## CODE_STATUS

- [x] inference-service 已实现最小服务骨架、动态 `health/metrics`、`/v1/chat/completions`、最小 `stream=true` SSE 返回、`x-request-id` 和项目级测试
- [x] ai-gateway 已实现鉴权、模型路由、代理转发、最小 streaming 透传、`x-request-id` 贯穿、最小 upstream 健康探测、限流、动态 metrics、`401/404/429/502` 错误路径和项目级测试
- [x] eval-module 已实现 `run / compare / list-tasks` CLI、result store、run/comparison bundle、JSON + Markdown 报告和项目级测试
- [x] finetune-demo 已实现 `train / save / export` CLI、mock trainer、checkpoint/metrics/logs/adapters/run/export manifest/artifacts manifest 产物和项目级测试
- [x] 根级 `Makefile`、`scripts/local_dev_sequence.sh`、`scripts/integration_smoke_test.sh` 已打通最小联调链路
- [x] `make infra-test` 当前已覆盖 inference-service、ai-gateway、eval-module、finetune-demo 四个项目测试
- [x] `make infra-smoke` 当前已覆盖 direct inference、gateway proxy、401、404、gateway metrics、inference dynamic metrics、eval result/compare 落盘、finetune train/export 落盘主链路
- [x] VitePress 学习站已可通过 `npm run docs:dev` 启动，并已验证 `docs:build` 与本地 `http://localhost:5173` 可访问

## REVIEW_PENDING

- [ ] T601 Inference Core Zero-Touch Pack 已完成，待 Codex 批量验收
- [ ] T602 Observability / Evaluation Zero-Touch Pack 已完成，待 Codex 批量验收
- [ ] T603 Finetuning / Training Zero-Touch Pack 已完成，待 Codex 批量验收
- [ ] T604 Cross-Project Systemization Pack 已完成，待 Codex 批量验收
- [ ] （无新增）

## REVISE_REQUIRED

- [ ] T101 vLLM 资料包初稿待修订 → `tasks/review/T101-review.md` → 已完成并通过
- [ ] T102 SGLang 资料包初稿待修订 → `tasks/review/T102-review.md` → 已完成 T112 修订，再经 T122 收紧，已完成
- [ ] T103 Triton 资料包初稿待重做 → `tasks/review/T103-review.md` → 已完成重做
- [ ] T104 glossary 第一批术语初稿待修订 → `tasks/review/T104-review.md` → 已完成 T114 修订，再经 T124 收紧，已完成
- [ ] T161 AI Gateway 资料包待修订 → `tasks/review/T161-review.md` → 已完成 T181 修订并通过
- [ ] T171 Cache 资料包待修订 → `tasks/review/T171-review.md` → 已完成 T182 修订并通过
- [ ] T172 Router 资料包待修订 → `tasks/review/T172-review.md` → 已完成 T183 修订并通过
- [ ] T193 AI Gateway 章节初稿待收紧 → `tasks/review/T193-review.md` → 已完成 T203 修订并通过
- [ ] T194 Observability 章节初稿待收紧 → `tasks/review/T194-review.md` → 已完成 T204 修订并通过
- [ ] T195 Evaluation 章节初稿待收紧 → `tasks/review/T195-review.md` → 已完成 T205 修订并通过
- [ ] T196 Cache / Prefix Caching 章节初稿待收紧 → `tasks/review/T196-review.md` → 已完成 T208 修订（最终收口）
- [ ] T197 LoRA / PEFT 章节初稿待收紧 → `tasks/review/T197-review.md` → 已完成 T207 修订并通过
- [ ] T199 finetuning comparison-index v1 待收紧 → `tasks/review/T199-review.md` → 已完成 T209 收紧并通过
- [ ] T308 evaluation / benchmark comparison-index v1 待收紧 → `tasks/review/T308-review.md` → 已完成 T309 收紧并通过
- [ ] T311 Benchmark / Leaderboard 章节初稿待收紧 → `tasks/review/T311-review.md` → 已完成 T312 修订并通过
- [ ] T314 finetuning glossary batch 04 待收紧 → `tasks/review/T314-review.md` → 已完成 T315 收紧并通过
- [ ] T402 Evaluation / Benchmark Long-Run Pack v1 待收紧 → `tasks/review/T402-review.md`
- [ ] T703 Finetuning / Training Deep-Research Pack 待收紧 → `tasks/review/T703-review.md`
- [ ] T704 Cross-Project Deep-Research Pack 待收紧 → `tasks/review/T704-review.md`
- [ ] T705 Execution Decomposition Pack 待收紧 → `tasks/review/T705-review.md`
- [ ] T801 inference-service Execution Prep Pack 待收紧 → `tasks/review/T801-review.md`
- [ ] T802 ai-gateway Execution Prep Pack 待收紧 → `tasks/review/T802-review.md`
- [ ] T803 eval-module Execution Prep Pack 待收紧 → `tasks/review/T803-review.md`
- [ ] T805 Cross-Project Integration Prep Pack 待收紧 → `tasks/review/T805-review.md`
- [ ] T901 inference-service Scaffold Pack 待收紧 → `tasks/review/T901-review.md`
- [ ] T902 ai-gateway Scaffold Pack 待收紧 → `tasks/review/T902-review.md`
- [ ] T903 eval-module Scaffold Pack 待收紧 → `tasks/review/T903-review.md`
- [ ] T904 finetune-demo Scaffold Pack 待收紧 → `tasks/review/T904-review-round-2.md`
- [ ] T905 Developer Workflow Scaffold Pack 待收紧 → `tasks/review/T905-review.md`
- [ ] T1001 inference-service Starter File Pack 待收紧 → `tasks/review/T1001-review.md` → 已完成 T1011/T1021 修订并通过
- [ ] T1002 ai-gateway Starter File Pack 待收紧 → `tasks/review/T1002-review.md` → 已完成 T1012 修订并通过
- [ ] T1005 Root / Dev Workflow Starter File Pack 待收紧 → `tasks/review/T1005-review.md` → 已完成 T1015/T1025 修订并通过
- [ ] T1011 inference-service Starter File Pack Revision 待再修订 → `tasks/review/T1011-review-round-2.md` → 已完成 T1021 修订并通过
- [ ] T1015 Root / Dev Workflow Starter File Pack Revision 待再修订 → `tasks/review/T1015-review-round-2.md` → 已完成 T1025 修订并通过
- [ ] T1101 inference-service Fixture Pack 待修订 → `tasks/review/T1101-review.md`
- [ ] T1102 ai-gateway Fixture Pack 待修订 → `tasks/review/T1102-review.md`
- [ ] T1103 eval-module Fixture Pack 待修订 → `tasks/review/T1103-review.md`
- [ ] T1105 Root Integration Fixture Pack 待修订 → `tasks/review/T1105-review.md`
- [ ] T1111 inference-service Fixture Pack Revision 待再修订 → `tasks/review/T1111-review-round-2.md`
- [ ] T1113 eval-module Fixture Pack Revision 待再修订 → `tasks/review/T1113-review-round-2.md`
- [ ] T1121 inference-service Fixture Naming Tighten 待再修订 → `tasks/review/T1121-review-round-3.md`
- [ ] T1123 eval-module Fixture Contract Tighten 待再修订 → `tasks/review/T1123-review-round-3.md`
- [ ] T1201 inference-service Implementation Map Pack 待修订 → `tasks/review/T1201-review.md`
- [ ] T1202 ai-gateway Implementation Map Pack 待修订 → `tasks/review/T1202-review.md`
- [ ] T1203 eval-module Implementation Map Pack 待修订 → `tasks/review/T1203-review.md`
- [ ] T1204 finetune-demo Implementation Map Pack 待修订 → `tasks/review/T1204-review.md`
- [ ] T1205 Root Integration Implementation Map Pack 待修订 → `tasks/review/T1205-review.md`
- [ ] T1211 inference-service Implementation Map Revision 待再收紧 → `tasks/review/T1211-review-round-2.md`
- [ ] T1213 eval-module Implementation Map Revision 待再收紧 → `tasks/review/T1213-review-round-2.md`
- [ ] T1214 finetune-demo Implementation Map Revision 待再收紧 → `tasks/review/T1214-review-round-2.md`
- [ ] T1215 Root Integration Implementation Map Revision 待再收紧 → `tasks/review/T1215-review-round-2.md`
- [ ] T1221 inference-service Implementation Map Tighten Round 2 待再收紧 → `tasks/review/T1221-review-round-3.md`
- [ ] T1223 eval-module Implementation Map Tighten Round 2 待再收紧 → `tasks/review/T1223-review-round-3.md`
- [ ] T1224 finetune-demo Implementation Map Tighten Round 2 待再收紧 → `tasks/review/T1224-review-round-3.md`
- [ ] T1303 eval-module Execution Slice Pack 待修订 → `tasks/review/T1303-review.md`
- [ ] T1304 finetune-demo Execution Slice Pack 待修订 → `tasks/review/T1304-review.md`
- [ ] T1305 Root Integration Execution Slice Pack 待修订 → `tasks/review/T1305-review.md`

## IN_PROGRESS_CODEX

- [ ] 继续做少量一致性抛光和入口优化
- [ ] 根据真实学习过程中的卡点补文档和说明
- [ ] 再按需把部分学习型实现逐步替换成更真实实现

## BACKLOG

- [ ] T305 comparison-index 模板页

## BLOCKED

- [ ] None

## ARCHIVED

- [x] T-INIT 初始方案讨论
