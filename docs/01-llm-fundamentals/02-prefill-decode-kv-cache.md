# Prefill、Decode、KV Cache

## Prefill 和 Decode 是什么

一次生成通常可以粗分成两个阶段：

- prefill：先把整段输入上下文“读进去”
- decode：再一个 token 一个 token 地往后生成

prefill 更像“先理解整段输入”，decode 更像“边看边续写”。

为什么这个拆分重要？因为两段的性能特征完全不同：

- prefill 更吃输入长度
- decode 更吃生成长度
- 两段对显存、吞吐、用户等待感知的影响也不同

## KV Cache 为什么重要

KV cache 的价值，是让模型在 decode 时不用每生成一个 token 就把前面上下文全部重新算一遍。  
你可以先把它理解成“为了后续生成而保存下来的中间状态”。

有了它之后：

- 长上下文不会每一步都从头算
- decode 阶段会明显更可接受
- 但显存占用会增加

所以 KV cache 本质上是在用空间换时间。

## 为什么这和基础设施直接相关

后面你看到：

- vLLM
- SGLang
- prefix caching
- request batching
- streaming

这些能力几乎都和 prefill / decode / KV cache 的组织方式有关。

也就是说，很多“推理框架差异”并不是表面 API 差异，而是它们如何管理这三样东西。

## 学这一节最重要的直觉

看到一个系统慢时，不要只问“模型为什么慢”，而要开始分阶段问：

1. 是 prefill 太重？
2. 是 decode 太慢？
3. 是 KV cache 管理方式不合适？

这会让你从“看起来都很慢”进入“我大概知道慢在哪一段”的状态。
