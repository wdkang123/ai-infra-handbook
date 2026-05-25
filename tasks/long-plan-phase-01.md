# Long Plan Phase 01

目标：把当前“推理服务主线”的资料、索引、章节、项目设计四条线并行推进，形成一个可以持续多天滚动执行的长任务框架。

## 当前基础

已通过的关键资产：

- vLLM 资料包
- SGLang 资料包
- Triton IS 资料包
- TensorRT-LLM 资料包
- 推理服务 comparison-index v1
- inference stack sources-index v1
- vLLM 章节初稿
- SGLang 章节初稿
- Triton IS 章节初稿
- observability/evaluation 资料包
- LoRA / QLoRA / PEFT 资料包
- Unsloth 资料包
- benchmark / serving eval 资料包

这意味着我们已经具备继续往下推进的条件，不需要再停留在纯搜资料阶段。

## 接下来 4 条主线

### 1. 收口线

先把还没完全收稳的资料补齐：

- AI Gateway 资料包
- Cache / Prefix Cache / Semantic Cache 资料包
- Router / Model Routing 资料包
- Triton 章节最后一轮收口

这条线的目标是减少“边界模糊”的内容。

### 2. 索引线

把已通过资料沉淀成可复用索引：

- inference stack comparison-index v2（加入 TensorRT-LLM）
- gateway / router / cache sources-index
- observability / evaluation sources-index
- finetuning sources-index

这条线的目标是让后续写章节和做项目时有稳定入口。

### 3. 章节线

基于已通过资料包批量写章节草稿：

- TensorRT-LLM 章节
- AI Gateway 章节
- Observability 章节
- Evaluation 章节
- Cache / Prefix Cache 章节
- LoRA / QLoRA / PEFT 章节
- Unsloth 章节

这条线的目标是把资料逐步转成手册正文。

### 4. 项目线

开始把“文档系统”拉回到“项目系统”：

- `inference-service` MVP 边界设计
- `ai-gateway` MVP 边界设计
- `eval-module` MVP 边界设计
- `finetune-demo` MVP 边界设计

这条线的目标是避免仓库变成只有文档没有项目的空壳。

## 推荐节奏

### 今明两天

优先完成：

1. 收口 AI Gateway / Cache / Router
2. 产出 comparison-index v2
3. 产出 TensorRT-LLM 章节草稿
4. 启动 inference-service / ai-gateway MVP 边界设计

### 接下来 3 到 5 天

优先完成：

1. Observability / Evaluation 章节草稿
2. LoRA / QLoRA / PEFT / Unsloth 章节草稿
3. 项目 MVP 目录与接口说明
4. README 和 overview 的一次统一收敛

### 再下一阶段

进入“文档 + 项目联动”：

1. 为每章绑定一个最小实践
2. 为每个项目产出最小 runnable skeleton
3. 开始做 glossary/comparison/sources 的统一整理

## MiniMax 长任务使用原则

夜间或长任务更适合做：

- 资料包
- sources-index
- glossary 批次
- comparison-index
- 模板化章节初稿
- 小范围修订

不适合无人值守地做：

- 总论章节
- README 风格收敛
- 项目架构结论
- 多章联动重写
- 高耦合目录调整

## 明日验收顺序

1. AI Gateway / Cache / Router 三个资料包先验
2. 再验 TensorRT-LLM / Triton 余下修订
3. 再进入 comparison-index v2 和章节草稿批量生产
