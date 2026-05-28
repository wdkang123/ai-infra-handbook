# AI Infra 入门

> 本页解决：第一次接触 AI Infra 时应该从哪条主线开始。
> 读完能做：理解 AI Infra 的四层系统图，并选择 Quickstart、学习路线或专题章节。
> 关联代码：`projects/inference-service`、`projects/ai-gateway`、`projects/eval-module`、`projects/finetune-demo`。
> 验证命令：`PYTHON=.venv/bin/python make quickstart`。

AI Infra 不是把模型 API 包一层，也不是只看 serving benchmark。它更像一组围绕模型能力交付、运行、治理、评估和迭代的工程系统。

这个学习站把 AI Infra 拆成四层：

| 层 | 当前项目 | 你要学会的问题 |
| --- | --- | --- |
| 模型运行层 | `inference-service` | 模型如何变成可调用服务 |
| 平台治理层 | `ai-gateway` | 请求如何鉴权、路由、限流、fallback |
| 质量闭环层 | `eval-module` | 输出如何被评测、比较、用于发布判断 |
| 训练迭代层 | `finetune-demo` | 数据、run、checkpoint、export 如何复现 |

## 推荐路径

1. [15 分钟 Quickstart](/quickstart/15-minute-demo)
2. [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
3. [学习路线图](/00-overview/02-learning-route)
4. [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
5. [示例输出与证据库](/13-output-gallery/00-overview)

## 你应该关注什么

新手最容易被工具名带偏。更稳的学习方式是先问：

- 请求有没有 request id
- 失败有没有 events
- 服务有没有 metrics
- 评测有没有 report
- 训练有没有 manifest
- 跑完有没有 evidence packet

这些证据比“听过多少工具名”更重要。

## FAQ

### 这个项目能直接上生产吗

不能。它是学习项目，不是生产平台。

### 不懂 vLLM / SGLang 可以开始吗

可以。先跑通 mock 学习链路，再看 [vLLM Adapter 设计](/12-production-migration/05-vllm-adapter-design) 和 [SGLang 迁移对比](/12-production-migration/08-sglang-migration-notes)。

### 学完后应该产出什么

至少写出一份端到端复盘：命令、request id、events、metrics、eval report、manifest 和下一步问题。
