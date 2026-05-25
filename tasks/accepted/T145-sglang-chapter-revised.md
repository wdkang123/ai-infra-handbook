Task ID: T145
Task Title: 修订 SGLang 章节初稿中的过强指标和不现实实践
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T135 初稿和 review note T135 修订。只改第 5 节关键指标和第 8 节最小实践，其余保留。

Result:

# SGLang

## 1. 这是什么

SGLang 是一个面向 LLM 和视觉语言模型的开源推理框架，通过共同设计后端运行时（RadixAttention、Continuous Batching）和前端语言（灵活的结构化生成控制），实现更快的模型交互和更细粒度的控制。

核心差异于 vLLM：SGLang 使用 RadixAttention 做前缀感知调度，在多轮对话、few-shot learning、多模态等共享前缀场景下有显著优势。

## 2. 为什么重要

在 AI Infra 推理服务栈中，SGLang 的价值在于：

1. **前缀共享优化**：RadixAttention 通过 Radix Tree 管理 KV Cache，相同前缀的多个请求共享缓存，减少重复计算，对多轮对话和 Agent 场景特别有效
2. **灵活的前端控制**：SGLang 提供 Python DSL，支持结构化输出（JSON、constrained decoding）、链式生成调用、外部工具交互，适合复杂 Agent 场景
3. **PD 分离（Prefill-Decode Disaggregation）**：将 prefill 和 decode 部署在不同硬件上，分别优化，是大模型分布式 Serving 的重要工程路径

## 3. 核心原理

### RadixAttention
在每次新请求到达时，将请求的前缀（prompt）挂载到 Radix Tree 上，并查找可复用的 KV Cache 子树。复用后只需计算新生成 token 部分的 attention。适用于 system prompt 共享、few-shot examples 共享、多轮对话前缀复用等场景。

来源：https://docs.sglang.ai/

### Continuous Batching
与 vLLM 类似，以单次 token 生成为调度粒度，动态管理批次。SGLang 的调度器在每个 step 重调度，是其 zero-overhead CPU scheduler 的核心。

来源：https://docs.sglang.ai/backend/index.html

### Chunked Prefill
将超长 prompt 的 prefill 分块，避免单个长 prompt 独占调度器导致其他短请求饥饿。是 SGLang 降低 P99 latency 的关键机制。

来源：https://docs.sglang.ai/

### PD 分离（Prefill-Decode Disaggregation）
将 prefill（输入处理）和 decode（逐 token 生成）部署在不同的 GPU 节点。Prefill 节点计算密度高，Decode 节点显存压力大，分离后各自优化。SGLang 支持多节点 EP（Expert Parallelism），在大规模 MoE 模型部署中尤为重要。

来源：https://lmsys.org/blog/2025-09-25-gb200-part-2/

## 4. 常见方案 / 组件

- **SGLang Runtime**：核心推理引擎，包含 RadixAttention、调度器、KV Cache 管理
- **Frontend Language（DSL）**：结构化生成接口，支持 JSON Schema、constrained decoding、链式调用
- **sgl-kernel**：SGLang 自研的高性能 CUDA kernel
- **FlashInfer Kernel Integration**：作为底层 attention kernel，与 SGLang 调度器配合
- **SGLang-Jax**：TPU 后端，实现 NVIDIA 之外的硬件支持（2025-10 发布）

来源：https://docs.sglang.ai/backend/index.html

## 5. 关键指标

- **TTFT（Time To First Token）**：交互式体验的首要指标，SGLang 在 benchmark 中会测量此项
- **ITL（Inter-Token Latency）**：生成流畅度指标，反映相邻 token 产出的间隔，是 SGLang 调度效果的体现。ITL 受模型大小、batch size、硬件配置等多因素影响，不存在通用达标值
- **Throughput**：token/s，SGLang 在长上下文和前缀共享场景下有优化优势
- **Prefix Cache Hit Rate**：前缀缓存命中率，是衡量共享前缀利用效率的核心指标，反映 RadixAttention 在实际工作负载中的效果

来源：https://github.com/sgl-project/sglang/issues/10813

## 6. 常见误区

1. **"SGLang 比 vLLM 新，所以更好"**：两者解决不同维度的问题——vLLM 专注于显存效率和易用性，SGLang 专注于调度灵活性和 Agent 场景。选型应根据场景决定
2. **"RadixAttention 等于前缀缓存"**：RadixAttention 是实现前缀缓存的数据结构基础，前缀缓存是其在共享前缀场景的应用效果
3. **"SGLang 只适合 Agent"**：SGLang 也适合标准 LLM Serving，其调度器和 vLLM 一样高效，只是额外提供了 Agent 场景的优化
4. **"SGLang 不支持 vLLM 支持的硬件"**：SGLang 支持 CUDA（主力）、ROCm、TPU（SGLang-Jax）

## 7. 与项目关系

在 AI Infra 学习路径中，SGLang 是理解调度差异化的进阶框架：

- 掌握 vLLM 后，对比 SGLang 的 RadixAttention vs PagedAttention，理解不同调度策略的权衡
- PD 分离是分布式 Serving 的重要模式，理解 SGLang 在这方面的先行实践，对后续学习 inference-service 的架构设计有帮助
- SGLang 的前端 DSL 展示了结构化生成的重要性，可以帮助理解 AI Gateway 层的设计

## 8. 最小实践任务

**目标**：在单卡 GPU 上用 SGLang 启动 Llama 模型服务，并通过结构化输出验证 SGLang 的 JSON constrained decoding 功能。

```bash
# 安装（CUDA 12.1+）
pip install "sglang[all]>=0.4.4.post1"

# 启动服务
python -m sglang.launch_server \
    --model-path meta-llama/Llama-3.2-3B-Instruct \
    --port 30000 \
    --chat-template llama3

# 结构化输出验证（JSON mode）
curl http://localhost:30000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "meta-llama/Llama-3.2-3B-Instruct",
        "messages": [{"role": "user", "content": "Return a JSON with fields: name, age"}],
        "extra_body": {"guided_json": {"type": "object", "properties": {"name": {"type": "string"}, "age": {"type": "number"}}, "required": ["name", "age"]}}
    }'
```

来源：https://docs.sglang.ai/start/install.html

## 9. 输出物

- SGLang API 服务运行中（端口 30000）
- 可通过 `curl` 或 OpenAI SDK 调用验证
- JSON constrained decoding 效果可观察

## 10. 延伸阅读

1. https://docs.sglang.ai/ — 官方文档
2. https://github.com/sgl-project/sglang — 主仓库
3. https://docs.sglang.ai/backend/index.html — Backend 架构文档
4. https://lmsys.org/blog/2024-09-04-sglang-v0-3/ — v0.3 官方 blog
5. https://lmsys.org/blog/2024-12-04-sglang-v0-4/ — v0.4 官方 blog
6. https://lmsys.org/blog/2025-09-25-gb200-part-2/ — PD+EP 性能数据

Sources:
1. https://docs.sglang.ai/ — SGLang 官方文档
2. https://github.com/sgl-project/sglang — 主仓库
3. https://docs.sglang.ai/backend/index.html — Backend 架构文档
4. https://github.com/sgl-project/sglang/issues/10813 — ITL 定义背景
5. https://lmsys.org/blog/2025-09-25-gb200-part-2/ — GB200 PD+EP blog
6. https://docs.sglang.ai/start/install.html — 安装文档

Risk of Staleness:
- SGLang 版本更新快，pip install 版本以实际安装时为准
- PD-Multiplexing、Elastic EP、HiSparse 均为实验性特性
- SGLang-Jax TPU 后端 2025-10 发布，文档完善度待观察

Out of Scope Kept:
- 未写成完整推理服务手册
- 未做与 vLLM 的最终优劣对比

Need Codex Review On:
- ITL 的工程描述是否足够稳健，"不存在通用达标值"的说法是否准确
