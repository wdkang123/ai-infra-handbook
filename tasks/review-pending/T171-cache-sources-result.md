Task ID: T171
Task Title: 搜集 caching / prefix caching / semantic cache 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集缓存相关能力资料包，包含术语边界（Prefix caching / KV cache reuse / Semantic cache 区别）、代表性实现、官方入口、优先阅读链接。

Result:

## 一、术语边界说明

### KV Cache（Key-Value Cache）
LLM 自回归推理中，Transformer 每层 attention 计算的中间结果（K、V 矩阵）被缓存，避免重复计算。KV cache 是 LLM 推理优化的基础，所有 prefix caching 都建立在 KV cache 之上。

### Prefix Caching（前缀缓存）
多个请求共享相同前缀（如 system prompt）时，复用此前缀对应的 KV cache 块。vLLM 通过 PagedAttention 管理 prefix cache block；SGLang 通过 RadixAttention 实现前缀感知的 KV cache 复用。核心收益：减少 prefill 阶段的计算耗时。

### Semantic Cache（语义缓存）
在更上层判断新请求是否与历史请求语义相近（如 prompt 相似度超过阈值），若命中则直接复用历史响应而非重新推理。不同于 prefix caching 依赖 token 级别的前缀匹配，semantic cache 依赖 embedding 相似度判断。

### 三者关系
- **KV cache** 是底层数据结构
- **Prefix caching** 是 KV cache 在"相同前缀多请求"场景下的复用策略
- **Semantic cache** 是更上层（应用层）的响应复用策略，不依赖共享 KV cache

## 二、代表性实现

### Prefix Caching / KV Cache 管理
| 实现 | 官方入口 |
|------|---------|
| **vLLM PagedAttention** | https://github.com/vllm-project/vllm |
| **SGLang RadixAttention** | https://github.com/sgl-project/sglang |
| **LMCache** | https://github.com/LMCache/LMCache |
| **Mooncake**（Kimi KVCache-centric）| https://arxiv.org/abs/2407.00079 |

### Semantic Cache
| 实现 | 官方入口 |
|------|---------|
| **GPTCache** | https://github.com/zilliztech/GPTCache |
| **Vearch** | https://github.com/vearch/vearch |
| **Redis + Vector**（通用方案）| https://redis.io/ |

## 三、官方主页 / GitHub / 文档

1. **vLLM PagedAttention**：https://github.com/vllm-project/vllm — PagedAttention 是 prefix caching 的基础实现
2. **SGLang RadixAttention**：https://docs.sglang.ai/backend/index.html — RadixAttention 做前缀感知调度
3. **LMCache**：https://github.com/LMCache/LMCache — 跨引擎 KV cache 缓存，支持 vLLM 和 SGLang
4. **Mooncake**：https://arxiv.org/abs/2407.00079 — Kimi 自研 KVCache-centric disaggregated serving 架构论文
5. **GPTCache**：https://github.com/zilliztech/GPTCache — 语义缓存开源实现，Milvus/Zilliz 团队维护
6. **OpenAI Evals**（相关工具）：https://github.com/openai/evals

## 四、核心能力对比

| 类型 | 缓存位置 | 匹配粒度 | 适用场景 |
|------|---------|---------|---------|
| KV Cache（vLLM） | GPU 显存 | Block 级别 | 多请求共享前缀 |
| Prefix Cache（SGLang） | GPU 显存 | Radix Tree 节点 | 多轮对话、few-shot |
| LMCache | GPU + CPU/SSD | Block 级别夸引擎 | 夸引擎/夸实例复用 |
| Semantic Cache | 外部向量库 | Embedding 相似度 | 语义重复请求 |

## 五、精确优先阅读链接（6 个）

1. **vLLM PagedAttention GitHub**：https://github.com/vllm-project/vllm
2. **SGLang RadixAttention 文档**：https://docs.sglang.ai/backend/index.html
3. **LMCache GitHub**：https://github.com/LMCache/LMCache
4. **Mooncake 论文**：https://arxiv.org/abs/2407.00079
5. **GPTCache GitHub**：https://github.com/zilliztech/GPTCache
6. **Redis Vector 文档**：https://redis.io/docs/interact/vector-embeddings/

Sources:
1. https://github.com/vllm-project/vllm — vLLM 主仓库（PagedAttention 实现）
2. https://docs.sglang.ai/backend/index.html — SGLang 后端架构文档（RadixAttention）
3. https://github.com/LMCache/LMCache — LMCache 主仓库
4. https://arxiv.org/abs/2407.00079 — Mooncake 论文
5. https://github.com/zilliztech/GPTCache — GPTCache 主仓库
6. https://redis.io/ — Redis 官方（向量搜索能力）

Risk of Staleness:
- vLLM 和 SGLang 的 prefix caching 实现随版本快速迭代
- LMCache 为较新项目（2025 年），稳定性待观察
- Mooncake 论文反映 2024 年状态，具体实现可能已有变化

Out of Scope Kept:
- 未写完整章节
- 未做最佳方案结论
- 未包含模型层面的缓存压缩（如 KV cache 量化）
