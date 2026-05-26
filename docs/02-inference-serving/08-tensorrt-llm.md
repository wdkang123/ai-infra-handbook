# TensorRT-LLM

TensorRT-LLM 更适合先理解成：

> NVIDIA 生态里的 LLM 执行优化层。

它不是 gateway。
它不是通用平台入口。
它也不应该先被理解成“完整模型服务产品”。

更稳的分层是：

| 层 | 代表 |
| --- | --- |
| 平台入口 | AI Gateway |
| 服务边界 | inference-service / model service |
| LLM serving runtime | vLLM / SGLang |
| 通用模型服务容器 | Triton |
| 底层执行优化 | TensorRT-LLM |

TensorRT-LLM 的重点是：如何让 LLM 在 NVIDIA GPU 上跑得更高效。

## 它主要解决什么问题

TensorRT-LLM 关注的是执行效率。

你可以先把它的问题空间理解成：

- 同一个模型能不能更低延迟？
- 同一个 GPU 能不能更高吞吐？
- 显存占用能不能更合理？
- 量化后性能和质量如何平衡？
- 多 GPU 场景下通信和并行如何组织？
- runtime 能不能更充分利用硬件能力？

这些问题比 HTTP API 更底层。

## 它和服务层的区别

服务层回答：

- 请求怎么进来？
- API 怎么定义？
- streaming 怎么返回？
- metrics 怎么暴露？
- 错误怎么映射？
- request id 怎么贯穿？

TensorRT-LLM 更关注：

- engine 如何构建？
- kernel 如何优化？
- quantization 如何执行？
- batch / sequence 如何在 runtime 中处理？
- GPU 资源如何利用？

两者都重要，但不是同一层。

## 它为什么值得学习

因为它能帮你建立一个关键分层意识：

> 模型服务做得好，不只靠服务框架；底层执行优化也是独立主线。

当模型规模、流量和成本上来后，纯粹“能服务”不够。
你会开始关心：

- 同样硬件能不能服务更多 token？
- 长上下文是否能承受？
- 延迟是否能下降？
- 成本是否能压下来？
- 是否能使用更低精度量化？

这些问题会把你带到 TensorRT-LLM 这类执行优化层。

## 它和 Triton 为什么常一起出现

Triton 和 TensorRT-LLM 可以形成自然组合：

```text
Triton Inference Server
  -> TensorRT-LLM backend
     -> optimized LLM execution on NVIDIA GPU
```

Triton 更像：

- 模型服务容器
- backend 管理
- 模型仓库
- 服务暴露

TensorRT-LLM 更像：

- LLM engine
- kernel/runtime 优化
- quantization
- GPU 执行效率

这组组合说明：推理系统可以分层拼装，而不是一个框架解决所有问题。

## 它和 vLLM / SGLang 怎么比较

不要直接问“谁更快”。
先问：

- 我需要完整 LLM serving runtime 吗？
- 我需要通用服务容器吗？
- 我需要 NVIDIA GPU 上的极致执行优化吗？
- 我有没有能力维护更复杂的构建和部署？

vLLM/SGLang 更适合先建立 LLM serving runtime 直觉。
TensorRT-LLM 更适合在性能、硬件、部署成熟度要求更高时深入。

## TensorRT-LLM 通常会带来哪些工程复杂度

学习时也要看到代价。

TensorRT-LLM 可能会让你面对：

- 硬件和 CUDA 版本要求
- 镜像和构建复杂度
- 模型转换
- engine build
- 量化配置
- 多 GPU 并行策略
- backend 集成
- 更复杂的性能调优

这些不是坏事，但说明它不适合一开始就放进低门槛学习路径。

## 当前仓库为什么不直接接入

当前仓库的目标是公开学习站。
默认路径必须让普通读者能快速跑通。

如果默认接入 TensorRT-LLM，会立刻引入：

- NVIDIA GPU 依赖
- Docker/CUDA/driver 版本问题
- 模型权重和 engine 构建
- 更复杂排障

这会压过主线。

所以当前仓库先保留：

- inference-service 服务边界
- engine adapter
- gateway 分层
- eval 和 finetune 证据链
- production migration 指南

等读者理解边界后，再把 TensorRT-LLM 作为进阶执行优化路线。

## 一个具体使用场景

假设你已经有：

- 稳定 gateway
- 稳定 inference API
- 清楚 eval baseline
- 明确 latency/cost 目标
- NVIDIA GPU 环境
- 需要更高 tokens/sec

这时可以考虑 TensorRT-LLM 路线。

迁移时不要只看“能不能跑”。
还要看：

- accuracy / quality 是否保持
- TTFT 是否改善
- throughput 是否改善
- memory footprint 是否改善
- streaming 是否仍然稳定
- errors 是否仍然可观测
- eval compare 是否通过

执行优化必须接回质量和平台观测。

## 什么时候不该先上 TensorRT-LLM

学习路线里也要知道“不上”的理由。

如果你还处在这些状态，先不要把 TensorRT-LLM 放进主线：

- 还没有稳定的模型服务 API
- 还没有 request id、metrics、events
- 还没有 eval baseline
- 还不知道目标是降低 TTFT、提高 throughput，还是降低显存
- 还没有固定硬件环境
- 团队还不能稳定维护 CUDA、driver、container、engine build

这时更好的顺序是先把服务边界跑稳，再把运行证据和评测链路补齐。否则性能优化会把注意力从“系统是否可解释”带到“环境为什么跑不起来”。

## 接入前要先定义指标

TensorRT-LLM 这类执行优化层不应该用一句“更快”来验收。

建议至少定义四组指标：

| 维度 | 观察点 | 为什么重要 |
| --- | --- | --- |
| 延迟 | TTFT、TPOT、端到端 latency | 区分首 token 和持续生成体验 |
| 吞吐 | requests/sec、tokens/sec、并发下吞吐 | 判断 GPU 是否被更充分利用 |
| 资源 | 显存、GPU 利用率、CPU、网络 | 防止把瓶颈转移到其他层 |
| 质量 | eval score、sample regression、格式成功率 | 确认优化没有伤害输出 |

如果没有指标，迁移后很容易只剩“感觉快了”。

## 一个迁移检查清单

从当前学习项目迁移到 TensorRT-LLM 路线，可以按这个清单推进：

```text
[ ] 保留 /v1/chat/completions 或清楚的 adapter contract
[ ] 保留 request id、events、metrics
[ ] 记录 model、engine、quantization、GPU、driver、container version
[ ] 建立 baseline/candidate eval
[ ] 对比 TTFT、TPOT、tokens/sec、error rate
[ ] 记录 streaming 是否保持稳定
[ ] 记录 fallback 和错误映射是否仍然可解释
[ ] 把 migration notes 写回文档或 case study
```

真正的迁移不是“把 backend 换掉”，而是让新 backend 进入同一套服务、观测和评测链路。

## 学习时可以怎么读官方文档

读 TensorRT-LLM 官方资料时，可以按这条路径走：

1. 先看产品总览，确认它是 NVIDIA GPU 上的 LLM 推理优化工具。
2. 再看 quick start，理解它如何构建和运行 LLM 请求。
3. 然后看 architecture，理解 toolkit、runtime、engine、backend 的分层。
4. 最后看 support matrix 和 release notes，确认模型、硬件、软件版本约束。

不要一开始就陷入单个 kernel 或 API。先把“它进入系统哪一层”想清楚，后面的细节才有位置。

## 常见误区

### “TensorRT-LLM 是完整服务平台”

不是。
它更偏底层 LLM 执行优化，需要被集成到服务体系里。

### “它只和性能有关，和架构无关”

不对。
它恰好能帮助你理解服务层、容器层和执行层为什么要分开。

### “学它必须先掌握所有 CUDA 细节”

不用。
学习阶段先理解它的层次和价值，再逐步下钻。

### “用了 TensorRT-LLM 就不用 eval”

不对。
任何执行优化都可能影响质量、输出、延迟和错误路径，必须评测。

### “越早接入越专业”

不一定。
如果边界还不清楚，过早接入会让学习成本暴涨。

## 学完应该能回答

读完这一页后，你应该能回答：

1. TensorRT-LLM 在推理系统里属于哪一层？
2. 它和 Triton 的关系是什么？
3. 它和 vLLM/SGLang 的比较应该先看哪些维度？
4. 为什么当前仓库默认不直接接入它？
5. 执行优化接入后为什么仍然要跑 eval 和 observability？

## 继续阅读

- [Triton Inference Server](/02-inference-serving/07-triton-inference-server)
- [Triton 与 TensorRT-LLM](/02-inference-serving/02-triton-tensorrt-llm)
- [服务选型与取舍](/02-inference-serving/03-serving-tradeoffs)
- [Benchmark 与生产质量不是一回事](/04-evaluation-observability/08-benchmark-vs-production-quality)
- [NVIDIA TensorRT-LLM 官方文档](https://docs.nvidia.com/tensorrt-llm/index.html)
