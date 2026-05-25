# Long Plan Phase 04

目标：把 MiniMax 从“长跑专题包模式”继续升级到“0 接管链式长跑模式”，让一次运行可以连续吞下多个大包，而不是做完一个包就停。

## 为什么还要继续升级

当前长跑包已经比微任务强很多，但还是有两个瓶颈：

- 单包交付物数量仍然偏少，常见是 4 到 5 个文件
- 包之间没有形成强链路，MiniMax 做完一包后很快结束

这会让单次运行时长仍然偏短，用户还需要频繁回来继续分发。

## 新模式核心

改成“链式长跑”：

- 一次运行包含 3 到 4 个专题包
- 每包 6 到 8 个文件级交付物
- 后面的包可以复用前面刚产出的合法文件
- Codex 不在中途插入反馈，统一在长跑结束后批量验收

## 三层推进结构

### 1. 主题深化层

每个主题先做：

- sources-index 升级
- comparison / glossary / practice catalog
- decision memo

### 2. 项目映射层

基于主题资料，继续做：

- integration notes
- project map
- interface sketch
- dependency notes

### 3. 系统收敛层

最后把不同主题拉到同一个项目视角下，形成：

- dependency matrix
- build order
- milestone board
- risk register

## 最适合 0 接管的主题链

1. Inference Core Chain
2. Observability / Evaluation Chain
3. Finetuning / Training Chain
4. Cross-Project Systemization Chain

## 协作节奏

白天：

- Codex 批量审阅
- 收口少量高判断成本问题

夜间 / 长时间窗口：

- MiniMax 只跑 `Zero-Touch Run`
- 一次跑完整条链
- 不要求人工中途接管

## 本阶段目标

让单次运行从“10 分钟左右”继续提升到“明显更长”，并且让用户只需要：

1. 启动一次
2. 等全部跑完
3. 第二天回来批量验收
