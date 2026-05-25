# Long Plan Phase 02

目标：从“资料包和单章起草”进入“章节批量化 + MVP 设计闭环 + sources-index 沉淀”的第二阶段，让 MiniMax 可以持续跑更久、而且每轮都能留下稳定资产。

## 当前状态

目前已经稳定通过的内容包括：

- 推理主线资料：vLLM / SGLang / Triton IS / TensorRT-LLM
- 推理主线章节：vLLM / SGLang / Triton IS / TensorRT-LLM
- 推理主线索引：comparison-index v2 / sources-index v1
- gateway 边界资料：AI Gateway / Cache / Router
- 辅助主线资料：Observability / Evaluation / Benchmark / LoRA / PEFT / Unsloth
- 项目设计：`inference-service` / `ai-gateway` MVP 设计稿

这意味着我们已经不再是“先搜一点资料再看”，而是可以稳定进入多线并行推进。

## 第二阶段的 4 条主线

### 1. 索引沉淀线

目标：把已通过资料变成后续章节和项目都能复用的稳定入口。

优先任务：

- `gateway / cache / router sources-index v1`
- `finetuning sources-index v1`
- 后续再补 `observability / benchmark sources-index`

### 2. 章节批量化线

目标：继续把已通过资料转成手册正文。

优先任务：

- AI Gateway 章节
- Observability 章节
- Evaluation 章节
- Cache / Prefix Cache 章节
- LoRA / PEFT 章节
- Unsloth 章节

### 3. MVP 设计闭环线

目标：把“只有文档”继续往“有项目骨架”推进。

优先任务：

- `eval-module` MVP 设计
- `finetune-demo` MVP 设计

完成后就能把 4 个项目位都占住：

- `inference-service`
- `ai-gateway`
- `eval-module`
- `finetune-demo`

### 4. Skeleton 准备线

目标：为后续真正开始写代码做铺垫。

这一条先不让 MiniMax 直接做实现，而是先把输入准备齐：

- 明确每个 MVP 设计稿里的“提案接口”
- 区分哪些命令只是文档草案，哪些会变成真实 CLI
- 为 Codex 后续写 skeleton 留出最小真实入口

## 推荐推进顺序

### 第一批

先做 6 个低耦合任务：

1. `T164` gateway / cache / router sources-index v1
2. `T165` finetuning sources-index v1
3. `T193` AI Gateway 章节初稿
4. `T194` Observability 章节初稿
5. `T303` eval-module MVP 设计
6. `T304` finetune-demo MVP 设计

### 第二批

在第一批通过后继续：

1. Evaluation 章节
2. Cache / Prefix Cache 章节
3. LoRA / PEFT 章节
4. Unsloth 章节
5. Benchmark / Eval index

### 第三批

再进入“文档到代码”的交界区：

1. `inference-service` skeleton
2. `ai-gateway` skeleton
3. `eval-module` skeleton
4. `finetune-demo` skeleton

## 适合长跑的任务类型

特别适合让 MiniMax 连续执行的：

- sources-index
- 模板化章节初稿
- MVP 边界设计
- 小范围修订

不适合无人值守长跑的：

- README 总收敛
- 总论章节
- 代码实现中的目录大改
- 多模块联动重写

## 验收原则

1. 先验索引任务，再验章节任务，再验 MVP 设计
2. 章节任务重点看边界、来源、最小实践是否低门槛
3. MVP 设计重点看“是不是设计稿”，避免把提案接口写成现实实现
