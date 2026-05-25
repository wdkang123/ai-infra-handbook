Task ID: T182
Task Title: 收紧 cache 资料包中的无关条目和分层表达
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T171 结果和 T171-review 修订。删除无关条目（OpenAI Evals），修复"夸引擎"错误表达，强化 KV cache / prefix cache / semantic cache 三层边界。

Result:

## 一、术语边界说明

### KV Cache（Key-Value Cache）
LLM 自回归推理中，Transformer 每层 attention 计算的中间结果（K、V 矩阵）被缓存，避免重复计算。KV cache 是 LLM 推理优化的基础，所有 prefix caching 都建立在 KV cache 之上。

### Prefix Caching（前缀缓存）
多个请求共享相同前缀（如 system prompt）时，复用此前缀对应的 KV cache 块。vLLM 通过 PagedAttention 管理 prefix cache block；SGLang 通过 RadixAttention 实现前缀感知的 KV cache 复用。核心收益：减少 prefill 阶段的计算耗时。

### Semantic Cache（语义缓存）
在更上层判断新请求是否与历史请求语义相近（如 prompt 相似度超过阈值），若命中则直接复用历史响应而非重新推理。不同于 prefix caching 依赖 token 级别的前缀匹配，semantic cache 依赖 embedding 相似度判断。

### 三者分层关系

```
应用层：Semantic Cache（向量相似度匹配，跨请求响应复用）
    ↓
引擎层：Prefix Caching（token 前缀匹配，KV cache 块复用）
    ↓
底层：KV Cache（GPU 显存中的 K/V 矩阵缓存）
```

## 二、代表性实现

### 引擎层 — Prefix Caching / KV Cache 管理
| 实现 | 定位 | 官方入口 |
|------|------|---------|
| **vLLM PagedAttention** | KV cache 分页管理 + prefix caching | https://github.com/vllm-project/vllm |
| **SGLang RadixAttention** | 前缀感知的 KV cache 调度 | https://github.com/sgl-project/sglang |
| **LMCache** | 跨引擎 KV cache 缓存（GPU+CPU/SSD） | https://github.com/LMCache/LMCache |

### 应用层 — Semantic Cache
| 实现 | 定位 | 官方入口 |
|------|------|---------|
| **GPTCache** | 语义相似度缓存，响应复用 | https://github.com/zilliztech/GPTCache |
| **Redis + Vector** | 通用向量数据库 + 相似度检索 | https://redis.io/docs/interact/vector-embeddings/ |

注：Mooncake 论文属于 KVCache-centric serving 架构研究，与 cache 产品层面不同，适合作为架构参考而非工具选型。

## 三、官方主页 / GitHub / 文档

1. **vLLM PagedAttention**：https://github.com/vllm-project/vllm
2. **SGLang RadixAttention**：https://docs.sglang.ai/backend/index.html
3. **LMCache**：https://github.com/LMCache/LMCache
4. **GPTCache**：https://github.com/zilliztech/GPTCache
5. **Redis Vector 搜索**：https://redis.io/docs/interact/vector-embeddings/

## 四、精确优先阅读链接（5 个）

1. **vLLM PagedAttention GitHub**：https://github.com/vllm-project/vllm
2. **SGLang RadixAttention 文档**：https://docs.sglang.ai/backend/index.html
3. **LMCache GitHub**：https://github.com/LMCache/LMCache
4. **GPTCache GitHub**：https://github.com/zilliztech/GPTCache
5. **Redis Vector 文档**：https://redis.io/docs/interact/vector-embeddings/

Sources:
1. https://github.com/vllm-project/vllm — vLLM 主仓库（PagedAttention 实现）
2. https://docs.sglang.ai/backend/index.html — SGLang 后端架构文档（RadixAttention）
3. https://github.com/LMCache/LMCache — LMCache 主仓库
4. https://github.com/zilliztech/GPTCache — GPTCache 主仓库
5. https://redis.io/docs/interact/vector-embeddings/ — Redis 向量搜索文档

Risk of Staleness:
- vLLM 和 SGLang 的 prefix caching 实现随版本快速迭代
- LMCache 为较新项目（2025 年），稳定性待观察
- Redis 向量搜索功能持续更新

Out of Scope Kept:
- 未写完整章节
- 未做最佳方案结论
- 未包含 KV cache 压缩量化等技术
