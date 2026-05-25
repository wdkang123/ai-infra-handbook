# Run、Compare、History

## 为什么一次评测不该只留下一个分数

如果一次 run 最后只剩一个总分，你后面会很难回答：

- 这次到底怎么跑的
- 用了什么模型和任务
- 原始结果在哪里
- 为什么它和上次不一样

所以评测结果至少应该是“分数 + 运行上下文 + 结果目录”。

## Run

run 解决的是“这次单次评测留下什么”。  
它通常应该至少带上：

- task
- model
- backend
- score
- sample outputs
- sample summary
- output bundle

`sample_outputs.json` 适合解释“哪些样本具体长什么样”，`sample_summary.json` 适合先看样本数量、通过/失败数量、平均分和 token 汇总，`sample_analysis.json` 则继续把 pass rate、score bucket、失败样本 id 和 judge reason 计数整理出来。

## Compare

compare 解决的是“这次和上次差在哪”。  
它不只是算一个 delta，更重要的是把比较本身也留成一个对象。

所以当前仓库里 compare 会留下：

- 对比结果 JSON
- 报告 Markdown
- comparison bundle
- release recommendation 和 release reasons

## History

history 的价值，是把离散 run / compare 连接成可追踪序列。  
否则你每次都像在看一次性截图，很难形成长期视角。

学习阶段如果把 history 这层理解透了，后面再看 benchmark、leaderboard 或实验追踪系统会容易很多。

## Leaderboard

leaderboard 解决的是“多次 run 怎么放在一起看”。  
它不重新执行评测，而是读取 history 指向的结果，把同一 task 下不同 model/backend/few-shot 的 best accuracy、latest accuracy 和 run count 汇总出来。

所以在当前仓库里，leaderboard 是 history 的展示层。  
它帮你横向观察，但不能替代 run 的事实记录，也不能替代 compare 的发布判断。

## Run Index

run index 解决的是“历史里到底有哪些 run”。  
它会把 timestamp、task、model、backend、few-shot、accuracy、result file 和 sample summary 列出来，也可以先用 backend/few-shot 过滤出更可比的一组 run。

它还会提供 `task_summaries`：按 task 汇总 run count、模型/后端/few-shot 覆盖数、best/latest accuracy 和对应 result file。这样 run index 既是历史清单，也能先给你一个“这个 task 最近状态如何”的轻量判断。

所以一个合理顺序是：先用 run index 盘点历史，再用 leaderboard 看横向排名，最后用 compare 做发布判断。

## Comparison Index

comparison index 解决的是“过去做过哪些 compare 判断”。  
它读取 `comparison_history.jsonl`，把 baseline、candidate、delta、verdict、release recommendation、comparison file、verdict counts、recommendation counts、task summaries 和平均 delta 汇总出来。

这样 compare 就不只是一个个孤立文件，而能沉淀成可回看的发布判断历史。
