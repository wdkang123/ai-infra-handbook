Task ID: T176
Task Title: 产出 night sources digest v1
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 Night Run 01 当晚完成的 10 个资料包/修订任务，产出汇总索引。

Result:

## Night Run 01 资料包汇总

### 当晚新增组件清单

| # | 组件 | 类型 | 定位 |
|---|------|------|------|
| 1 | **TensorRT-LLM** | 推理优化后端 | NVIDIA 提供的 LLM 推理优化库，基于 TensorRT 的算子层优化 |
| 2 | **AI Gateway** | 网关层 | 统一接入多模型供应商的 API 代理层（Portkey、APIPark、LiteLLM 等） |
| 3 | **Observability 工具链** | 可观测性 | LLM 请求 tracing、metrics、feedback 采集（Langfuse、TensorZero、Agenta） |
| 4 | **Evaluation 工具链** | 评测 | 模型能力评测（Benchmark）和输出质量评测（LM-Eval Harness、Stanford HELM） |
| 5 | **Caching / Prefix Cache** | 缓存 | KV cache 复用和 semantic cache（vLLM PagedAttention、SGLang RadixAttention、LMCache） |
| 6 | **Model Router** | 路由层 | 动态请求分发（NVIDIA llm-router、LiteLLM、Portkey） |
| 7 | **LoRA / QLoRA / PEFT** | 微调方法 | 参数高效微调方法及 Hugging Face PEFT 框架 |
| 8 | **Unsloth** | 微调加速 | LoRA/QLoRA 训练加速，2x 速度 + 50% 显存占用 |
| 9 | **Benchmark / Serving Eval** | 评测工具 | 推理性能评测工具（vLLM/SGLang benchmarks、LM-Eval Harness、LMSYS Arena） |
| 10 | **Glossary 术语收紧** | 术语修订 | Canary Routing、Tracing、Replay 来源精确化 |

### 每个组件优先阅读（每个组件 2 个链接）

| 组件 | 优先阅读 1 | 优先阅读 2 |
|------|-----------|-----------|
| TensorRT-LLM | https://github.com/NVIDIA/TensorRT-LLM | https://github.com/NVIDIA/TensorRT-LLM/tree/main/triton_backend |
| AI Gateway | https://github.com/Portkey-AI/gateway | https://github.com/BerriAI/litellm |
| Observability | https://langfuse.com/docs/observability/overview | https://github.com/tensorzero/tensorzero |
| Evaluation | https://github.com/EleutherAI/lm-evaluation-harness | https://crfm.stanford.edu/helm/ |
| Caching | https://github.com/vllm-project/vllm | https://arxiv.org/abs/2407.00079（Mooncake 论文）|
| Model Router | https://github.com/NVIDIA-AI-Blueprints/llm-router | https://docs.litellm.ai/docs/proxy_router |
| LoRA/PEFT | https://github.com/huggingface/peft | https://arxiv.org/abs/2305.14314（QLoRA 论文）|
| Unsloth | https://github.com/unslothai/unsloth | https://docs.unsloth.ai/ |
| Benchmark | https://github.com/EleutherAI/lm-evaluation-harness | https://chat.lmsys.org/ |
| Glossary | https://glossary.cncf.io/canary-deployment/ | https://opentelemetry.io/ |

### 第二天值得 Codex 先审的 3 个结果

1. **T161（AI Gateway 资料包）** — 新扩资料面，覆盖 Portkey、APIPark、LiteLLM 等多个实现，建议优先确认边界划分是否合适
2. **T171（Cache 资料包）** — KV cache / Prefix cache / Semantic cache 三层概念容易混淆，建议 Codex 确认边界说明是否准确
3. **T151（TensorRT-LLM 资料包修订）** — 补充了 NVIDIA Developer Blog 和 v1.2.0 release 链接，删除了不存在的 0.17.0 条目，建议确认"文档托管于 GitHub"的注记是否需要

### 补充说明

- T151、T153、T156 为修订任务（基于 review note 的定向收紧）
- T161-T175 为新资料包任务（扩资料面）
- T176 为汇总索引（基于以上实际产出）
- 术语 Glossary 收紧涉及：Canary Routing（来源换 CNCF）、Tracing（来源换 OpenTelemetry）、Replay（项目关系收回）

Sources:
- 各任务实际输出文件，均位于 `tasks/review-pending/`

Risk of Staleness:
- 各开源项目更新频繁，链接有效性以实际访问为准

Out of Scope Kept:
- 未新增分析结论
- 未写长文
- 仅基于当晚实际产出
