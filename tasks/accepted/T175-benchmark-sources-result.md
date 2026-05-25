Task ID: T175
Task Title: 搜集 inference benchmark / serving eval 官方资料与核心链接
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
搜集推理服务 benchmark、serving eval、latency/throughput 测试资料包，包含术语边界、代表性工具、官方入口、核心指标定义、优先阅读链接。

Result:

## 一、术语边界说明

### Benchmark（评测基准）
在标准数据集上评估模型能力（MMLU、GSM8K、HumanEval 等），关注"模型懂不懂、会不会"。不关注推理速度、成本、并发。

### Serving Eval / Inference Benchmark（推理服务评测）
关注"模型服务得好不好"——吞吐量、延迟、并发稳定性、资源利用率。核心工具是负载测试工具（wrk、locust）和推理服务自带的 benchmark 工具。

### 核心指标

| 指标 | 全称 | 说明 |
|------|------|------|
| **TTFT** | Time To First Token | 首个 token 产出时间，反映 prefill 效率 |
| **ITL** | Inter-Token Latency | 相邻 token 产出间隔，反映 decode 效率 |
| **Throughput** | 吞吐 | 单位时间产出 token 数 |
| **RPS** | Requests Per Second | 每秒请求数 |
| **P99 Latency** | 99th Percentile Latency | 99% 请求的最大延迟 |
| **GPU Util** | GPU Utilization | GPU 利用率 |

## 二、代表性官方资料与工具

### 模型能力 Benchmark
| 工具 | 官方入口 |
|------|---------|
| **Stanford HELM** | https://crfm.stanford.edu/helm/ |
| **Open LLM Leaderboard** | https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard |
| **LMSYS Chatbot Arena** | https://chat.lmsys.org/ |
| **EleutherAI LM-Eval Harness** | https://github.com/EleutherAI/lm-evaluation-harness |
| **BigCode Evaluation Harness** | https://github.com/bigcode-project/bigcode-eval-harness |

### Serving / Inference Benchmark
| 工具 | 官方入口 |
|------|---------|
| **vLLM benchmark** | https://github.com/vllm-project/vllm/tree/main/benchmarks |
| **SGLang benchmark** | https://github.com/sgl-project/sglang/tree/main/benchmarks |
| **lm-eval-harness（EleutherAI）** | https://github.com/EleutherAI/lm-evaluation-harness |
| **wrk / wrk2** | https://github.com/wg/wrk |
| **Locust** | https://github.com/locustio/locust |

## 三、官方主页 / GitHub / 文档

1. **Stanford HELM**：https://crfm.stanford.edu/helm/ — 全面评测框架，覆盖 50+ 场景
2. **Open LLM Leaderboard**：https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Hugging Face 官方开源模型排行榜
3. **LMSYS Chatbot Arena**：https://chat.lmsys.org/ — 基于人类盲评的模型排名
4. **EleutherAI LM-Eval Harness**：https://github.com/EleutherAI/lm-evaluation-harness — 本地化模型能力评测工具
5. **vLLM Benchmarks**：https://github.com/vllm-project/vllm/tree/main/benchmarks — vLLM 吞吐量/latency benchmark
6. **SGLang Benchmarks**：https://github.com/sgl-project/sglang/tree/main/benchmarks — SGLang 性能评测

## 四、Serving Eval 中的关键指标关系

```
Request → TTFT（prefill 完成）→ ITL（decode 每步）→ E2E Latency
                ↓
         Throughput（RPS × token/request）
```

- **TTFT** 取决于 prefill 速度，与 prompt 长度强相关
- **ITL** 取决于 decode 吞吐，与 batch size、模型大小相关
- **P99 latency** 综合反映 prefill + decode + 调度的端到端表现

## 五、精确优先阅读链接（7 个）

1. **Stanford HELM**：https://crfm.stanford.edu/helm/
2. **Open LLM Leaderboard**：https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
3. **LMSYS Chatbot Arena**：https://chat.lmsys.org/
4. **EleutherAI LM-Eval Harness GitHub**：https://github.com/EleutherAI/lm-evaluation-harness
5. **vLLM Benchmarks 目录**：https://github.com/vllm-project/vllm/tree/main/benchmarks
6. **SGLang Benchmarks 目录**：https://github.com/sgl-project/sglang/tree/main/benchmarks
7. **BigCode Evaluation Harness**：https://github.com/bigcode-project/bigcode-eval-harness

Sources:
1. https://crfm.stanford.edu/helm/ — Stanford HELM 官网
2. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard — Open LLM Leaderboard
3. https://chat.lmsys.org/ — LMSYS Chatbot Arena
4. https://github.com/EleutherAI/lm-evaluation-harness — LM-Eval Harness 主仓库
5. https://github.com/vllm-project/vllm/tree/main/benchmarks — vLLM benchmark 工具
6. https://github.com/sgl-project/sglang/tree/main/benchmarks — SGLang benchmark 工具
7. https://github.com/bigcode-project/bigcode-eval-harness — BigCode 评测工具

Risk of Staleness:
- LMSYS Arena 和 Open LLM Leaderboard 按季度更新，排名变化较快
- LM-Eval Harness 版本更新可能影响 benchmark 结果可比性
- 各框架 benchmark 工具因版本不同参数和输出格式可能有变化

Out of Scope Kept:
- 未写完整评测章节
- 未写 benchmark 排名结论
- 未做具体模型选型建议
