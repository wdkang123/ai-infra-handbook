# 文档与项目怎么联动

## 为什么项目总览后面还需要这一页

因为项目总览解决的是“这四个项目各自干什么”，  
但当你真正开始学习时，更常见的问题会变成：

- 我刚读完一页文档
- 现在应该回哪个项目、哪个文件

这一页就是用来解决这个问题的。

## 先记一张最简单的联动图

```text
基础概念 -> inference-service / ai-gateway
推理服务 -> inference-service
平台层 -> ai-gateway
评测与观测 -> eval-module + root smoke / metrics
微调训练 -> finetune-demo
```

你不需要一开始记所有文件，只要先记住“每组内容主要落在哪个项目”。

## inference-service 最适合承接哪些文档

它最适合承接：

- Prefill / Decode / KV Cache
- 从请求到首个 Token
- Streaming、Batching、Metrics
- vLLM / SGLang 的执行层理解

如果你读完这些页，最该回看的通常是：

- `server.py`
- `runtime.py`

## ai-gateway 最适合承接哪些文档

它最适合承接：

- 鉴权、路由、限流
- request id
- upstream health
- streaming 透传
- fallback headers / metrics
- response cache header
- 平台层与模型服务层边界
- 外部模型名与内部目标映射

如果你读完这些页，最该回看的通常是：

- `server.py`
- `router.py`
- `middleware/auth.py`

## eval-module 最适合承接哪些文档

它最适合承接：

- Run、Compare、History
- LLM Evaluation
- 从 Run 到发布决策
- benchmark 执行层理解
- sample outputs / sample summary
- leaderboard 展示层

如果你读完这些页，最该回看的通常是：

- `main.py`
- `runners/lm_eval_runner.py`
- `results/result_store.py`

## finetune-demo 最适合承接哪些文档

它最适合承接：

- LoRA / QLoRA / PEFT
- 训练产物、Checkpoint、Export
- 数据集、Run、Checkpoint
- dataset registry
- dataset version / export lineage
- History / reproducibility
- 什么时候该微调

如果你读完这些页，最该回看的通常是：

- `main.py`
- `config.py`
- `trainer/lora_trainer.py`
- `export/adapter_exporter.py`

## 最推荐的学习动作

最稳的节奏通常是：

1. 读一页文档
2. 回一个项目
3. 只开 1 到 2 个文件
4. 跑一条最小命令

这样最容易把：

- 概念
- 代码
- 结果

连成一条线。

## 这一页学完应该带走什么

项目页不是“代码目录说明”，文档页也不是“纯理论文章”。  
它们本来就应该联动起来看：一边解释为什么，一边展示现在是怎么做的。
