# 文档与代码怎么对应

## 为什么这一页值得先看

因为这套仓库本来就不是纯文档站，也不是纯代码仓库。  
它真正想做的，是把：

- 学习内容
- 可运行脚手架
- 观察结果

三者绑成一条学习路径。

所以一个更高效的学习方式，不是“先把文档全部看完”或“先把源码全部翻完”，  
而是知道每一组内容大概对应哪一层代码。

## 最粗的一张对应图

先记这张最粗的图就够了：

```text
基础概念 -> 推理请求生命周期的共同语言
推理服务 -> inference-service
平台层 -> ai-gateway
评测与观测 -> eval-module + metrics / smoke
微调训练 -> finetune-demo
```

你后面如果发现自己“概念懂了一点，但不知道该回哪里看”，就回到这张图。

## 基础概念更适合对到哪里

如果你在读：

- 模型、Token、Context
- Prefill、Decode、KV Cache
- 从请求到首个 Token

最适合对照看的通常是：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

因为这些文件最容易把“一个请求是怎么走完整条链的”具体化。

## 推理服务章节更适合对到哪里

如果你在读：

- vLLM
- SGLang
- Cache / Prefix Caching
- Streaming、Batching、Metrics

最适合先回看的就是 `inference-service`。

虽然当前仓库还没有把真实 vLLM / SGLang 深度接满，  
但它已经把理解 serving 最重要的结构留出来了：

- 普通响应
- streaming
- metrics
- request lifecycle

所以它很适合当“真实框架接入前的学习骨架”。

## 平台层章节更适合对到哪里

如果你在读：

- 鉴权、路由、限流
- 健康检查、Request ID
- 平台层与模型服务层边界
- 外部模型名与内部目标映射

那最值得回看的就是 `ai-gateway`：

- `server.py`
- `router.py`
- `middleware/auth.py`
- `tests/test_proxy.py`

因为平台层的很多学习价值，本来就体现在边界行为里。

## 评测与观测章节更适合对到哪里

如果你在读：

- Run、Compare、History
- LLM Evaluation
- 从 Run 到发布决策
- Tracing、Metrics、Logs

最该回看的是：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/results/result_store.py`
- 根级 `scripts/integration_smoke_test.sh`

这里最重要的不是复杂评测算法，而是理解：

- 为什么一次 run 不是只留一个分数
- compare 为什么重要
- history 为什么能支撑长期判断

## 微调训练章节更适合对到哪里

如果你在读：

- LoRA、QLoRA、PEFT
- 训练产物、Checkpoint、Export
- 实验追踪、History、复现
- 什么时候该微调

最适合回看的就是 `finetune-demo`：

- `main.py`
- `config.py`
- `trainer/lora_trainer.py`
- `export/adapter_exporter.py`

这里的重点不是“训练已经有多生产级”，而是你能不能看清训练工程资产到底长什么样。

## 最推荐的学习动作

最稳的学习节奏通常是：

1. 先读一页文档
2. 只打开 1 到 2 个对应代码文件
3. 带着一个明确问题去看
4. 再跑一条最小命令验证

比如：

- 读完 request id，再去看 gateway 的 server
- 读完 run/history，再去看 eval 的 result store
- 读完 checkpoint/export，再去看 finetune 的 exporter

这样会比无差别翻代码更快建立结构感。

## 这一页学完应该带走什么

文档更像问题地图，代码更像当前实现。  
把两者连起来看，你学到的就不只是概念，也不只是源码，而是“这套系统现在为什么长成这样”。
