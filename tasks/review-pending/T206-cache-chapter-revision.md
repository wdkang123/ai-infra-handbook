Task ID: T206
Task Title: 收紧 Cache / Prefix Caching 章节初稿中的观测闭环
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T196 初稿和 T196-review 修订。只修最小实践的 TTFT 承诺超出命令能力这一问题，不重写整章。

Result:

# Cache / Prefix Caching

## 1. 这是什么

Cache 在 LLM 推理中指复用已有计算结果以减少重复推理的技术。按层次分为三类：

- **KV Cache**：GPU 显存中缓存 attention 的 K/V 矩阵，是底层基础设施
- **Prefix Caching**：多个请求共享相同前缀时复用此前缀的 KV cache 块
- **Semantic Cache**：在应用层判断请求语义相似度，命中则复用历史响应

三者构成"底层 → 中层 → 上层"的缓存分层体系。

## 2. 为什么重要

在 AI Infra 推理服务中，缓存是成本和延迟优化的关键：

1. **降低延迟**：Prefix Caching 减少重复 prefill 计算，首 token 时间显著降低
2. **节省成本**：缓存命中减少实际推理调用，节省 token 消耗
3. **提升吞吐**：KV cache 复用使 GPU 计算资源用于新请求而非重复计算
4. **支持高并发**：良好的缓存策略在高并发场景下效果尤为明显

## 3. 核心原理

### KV Cache（底层）
LLM 自回归推理中，Transformer 每层 attention 计算的中间结果（K、V 矩阵）被缓存于 GPU 显存。自回归生成时每个新 token 都需要访问此前所有 token 的 K/V，使用缓存可避免重复计算。

来源：https://github.com/vllm-project/vllm

### Prefix Caching（中层）
多个请求共享相同前缀（如 system prompt）时，复用此前缀对应的 KV cache 块。vLLM 通过 PagedAttention 管理 prefix cache block；SGLang 通过 RadixAttention 实现前缀感知的 KV cache 调度。

来源：https://docs.sglang.ai/backend/index.html

### Semantic Cache（上层）
在更上层判断新请求是否与历史请求语义相近（如 prompt embedding 相似度超过阈值），若命中则直接复用历史响应而非重新推理。与 prefix caching 依赖 token 级别前缀匹配不同，semantic cache 依赖 embedding 相似度。

来源：https://github.com/zilliztech/GPTCache

### 三者分层关系

```
应用层：Semantic Cache（向量相似度匹配，跨请求响应复用）
    ↓
引擎层：Prefix Caching（token 前缀匹配，KV cache 块复用）
    ↓
底层：KV Cache（GPU 显存中的 K/V 矩阵缓存）
```

## 4. 常见方案 / 组件

### 引擎层 — Prefix Caching / KV Cache 管理
| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **vLLM PagedAttention** | KV cache 分页管理 + prefix caching | https://github.com/vllm-project/vllm |
| **SGLang RadixAttention** | 前缀感知的 KV cache 调度 | https://github.com/sgl-project/sglang |
| **LMCache** | 跨引擎 KV cache 缓存（GPU+CPU/SSD） | https://github.com/LMCache/LMCache |

### 应用层 — Semantic Cache
| 工具 | 定位 | 官方入口 |
|------|------|---------|
| **GPTCache** | 语义相似度缓存，响应复用 | https://github.com/zilliztech/GPTCache |
| **Redis + Vector** | 通用向量数据库 + 相似度检索 | https://redis.io/docs/interact/vector-embeddings/ |

来源：https://github.com/vllm-project/vllm
来源：https://docs.sglang.ai/backend/index.html

## 5. 关键指标

| 指标 | 全称 | 说明 | 来源 |
|------|------|------|------|
| **Cache Hit Rate** | 缓存命中率 | 命中缓存的请求比例 | https://github.com/vllm-project/vllm |
| **Prefill Speed** | Prefill 速度 | 处理 prompt token 的速度 | https://docs.vllm.ai/ |
| **Memory Utilization** | 显存利用率 | KV cache 在 GPU 显存中的占用 | https://github.com/LMCache/LMCache |

## 6. 常见误区

1. **"KV Cache 就是 Prefix Caching"**：KV cache 是底层存储机制，prefix caching 是利用 KV cache 的调度策略，两者不同层次
2. **"Semantic Cache 和 Prefix Caching 是一回事"**：Prefix caching 依赖 token 级别精确匹配，semantic cache 依赖 embedding 相似度匹配，原理和适用场景都不同
3. **"缓存越大越好"**：缓存占用 GPU 显存，过大可能影响并发batch size，实际需要权衡

## 7. 与项目关系

在 AI Infra 学习路径中，Cache 位于推理引擎和应用的交界处：

- inference-service 中的 vLLM/SGLang 内置 KV cache 管理，是缓存的底层基础
- ai-gateway 可接入 semantic cache 层做请求相似度匹配
- 与 prefix caching 关系最直接的是推理引擎的调度器设计

## 8. 最小实践任务

**目标**：使用 vLLM 发送两个有共享前缀的请求，观察整体响应时间差异（TTFT 等细分指标需通过 tracing 工具观测，本实践只验证整体延迟趋势）。

```bash
# 1. 启动 vLLM（启用 prefix caching）
vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --enable-prefix-caching \
  --host 0.0.0.0 --port 8000

# 2. 发送第一个请求（含长 system prompt）
curl -w "\nTotal time: %{time_total}s\n" \
  http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"system","content":"[很长 system prompt...]"},{"role":"user","content":"你好"}]}'

# 3. 发送第二个请求（相同 system prompt，不同 user message）
curl -w "\nTotal time: %{time_total}s\n" \
  http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"system","content":"[相同很长 system prompt...]"},{"role":"user","content":"今天天气如何"}]}'

# 4. 对比两次 curl 的 Total time
# 第二次请求整体延迟通常低于第一次（prefix cache 命中）
```

来源：https://github.com/vllm-project/vllm
来源：https://docs.vllm.ai/

## 9. 输出物

- vLLM 服务运行中（端口 8000，启用 prefix caching）
- 两个共享前缀请求的整体响应时间记录
- 可观察到第二个请求整体延迟低于第一个请求

## 10. 延伸阅读

1. https://github.com/vllm-project/vllm — vLLM 主仓库（PagedAttention 实现）
2. https://docs.sglang.ai/backend/index.html — SGLang 后端架构文档（RadixAttention）
3. https://github.com/LMCache/LMCache — LMCache 主仓库
4. https://github.com/zilliztech/GPTCache — GPTCache 主仓库
5. https://redis.io/docs/interact/vector-embeddings/ — Redis 向量搜索文档

Sources:
1. https://github.com/vllm-project/vllm — vLLM 主仓库
2. https://docs.sglang.ai/backend/index.html — SGLang 后端架构文档
3. https://github.com/LMCache/LMCache — LMCache 主仓库
4. https://github.com/zilliztech/GPTCache — GPTCache 主仓库
5. https://redis.io/docs/interact/vector-embeddings/ — Redis 向量搜索文档

Risk of Staleness:
- vLLM 和 SGLang 的 prefix caching 实现随版本快速迭代
- LMCache 为较新项目（2025 年），稳定性待观察
- Redis 向量搜索功能持续更新

Out of Scope Kept:
- 未写完整缓存系统设计
- 未做性能排名
- 未写 KV cache 压缩量化等技术

Need Codex Review On:
- TTFT 等细分指标需要 tracing 工具（如 Langfuse）才能观测，本最小实践只承诺 curl 可见的整体延迟
