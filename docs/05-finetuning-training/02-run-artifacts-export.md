# 训练产物、Checkpoint、Export

## 为什么训练不该只留下一个 checkpoint

如果一次训练最后只剩一个 checkpoint，后面你会很难回答：

- 这次是用什么配置跑的
- 数据大概是什么
- 训练过程中指标如何变化
- 导出时用了哪个版本

所以训练 run 最好沉淀成一个目录，而不是一个孤零零的权重文件。

## 训练产物应该包括什么

学习阶段先看这几类就够了：

- trainer state
- training args
- metrics
- logs
- dataset summary
- dataset registry entry
- dataset version / dataset sha256
- checkpoint 索引
- checkpoint index
- run manifest
- artifacts manifest

它们共同解决的是“把一次训练变成可回看对象”。  
其中 dataset summary 偏单次 run，dataset registry entry 则把这份训练输入登记成可跨 run 追踪的数据资产。`list-datasets` 可以把追加式 registry 转成 JSON/Markdown 报告，支持按 method/model 过滤，并展示重复登记数量，方便人读和工具继续处理。`diff-datasets` 则负责比较两份登记数据的 version、sha256、records 和 role counts，帮助你判断训练输入是否真的发生了变化。

## Export 为什么要单独保留

export 不是多余步骤，它是在把“训练过程中的中间产物”整理成“更适合后续使用的输出”。  
如果不把这一步单独留出来，后面：

- 部署
- 迁移
- 对比不同 run

都会更混乱。

## History 为什么仍然重要

训练和评测一样，也不该只看单次结果。  
run history / export history 的意义，是把多次实验连起来看。  
当 run history 里保留 dataset id、dataset version、checkpoint 和 run manifest pointer 时，你就能从训练历史反查每次 run 的证据文件；当 export history 里继续保留 dataset id、dataset version 和 adapter hash 时，你就能从交付资产反查训练输入与具体导出文件。

`checkpoints/checkpoint_index.json` 会把 checkpoint 文件、adapter hash 和 resumable 标记放在一起。当前只有一个 mock checkpoint，但这层结构对应真实训练里常见的“多个 checkpoint 怎么选择、怎么导出、怎么恢复”的问题。

`list-runs` 会把 `run_history.jsonl` 转成 run index。它不重新训练，只是把 method、model、dataset id、dataset version、output dir、checkpoint、run manifest pointer、checkpoint index pointer、model summaries 和 dataset summaries 摆出来，让训练 run 本身可以被盘点。

`list-exports` 会把 `export_history.jsonl` 转成 export index。它不改变任何 adapter，只是把 output dir、export manifest pointer、status、duration、base model、dataset id、dataset version、adapter hash、model summaries 和 dataset summaries 摆出来，让导出资产也能像 run 一样被盘点。

学习阶段先建立这个习惯，以后接更真实的实验追踪系统会顺很多。
