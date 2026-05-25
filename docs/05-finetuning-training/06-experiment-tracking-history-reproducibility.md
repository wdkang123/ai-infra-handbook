# 实验追踪、History、复现

## 为什么训练学习最终会走到“追踪”这一步

因为训练最容易出现的，不是“完全跑不起来”，而是：

- 跑是能跑
- 结果也有
- 但过几天你已经说不清它是怎么来的

如果没有实验追踪和 history，训练很快就会从“学习过程”变成“随机留下的一堆目录”。

## History 在训练里为什么特别重要

因为训练不像一次普通 API 请求，它天然是多次尝试、逐步迭代的。

你很少只跑一次就结束。  
更常见的是：

- 改一点数据
- 改一点配置
- 换一个 LoRA rank
- 再跑一轮

这时 history 的价值就非常明确：  
它帮你把离散实验连成可追踪序列。

## 复现到底在回答什么

复现不是为了学术洁癖，而是为了让你后面还能回答这些问题：

- 这个结果是怎么来的
- 如果我重跑一次，大概会不会得到同类结果
- 这个 export 对应的是哪个 run
- 这次训练到底比上次好在哪里

如果这些问题回答不了，训练结果就很难积累成真正有用的经验。

## 当前仓库为什么反复强调 manifest 和 history

因为这是学习型项目里最值得提前养成的习惯。

当前 `finetune-demo` 虽然不是完整训练平台，但已经故意把这些对象留出来了：

- `run_manifest.json`
- `artifacts_manifest.json`
- `run_history.jsonl`
- `run_index.json`
- `export_history.jsonl`
- `export_index.json`
- run manifest pointer
- export status / duration
- export model/dataset summaries
- export manifest pointer
- 数据集摘要
- 数据集登记
- 数据集登记报告
- 数据集 diff
- method/model 过滤和重复登记统计
- checkpoint 索引
- dataset version / dataset sha256
- adapter 文件 hash

它们的价值不在于“文件格式多”，而在于：

`run_history.jsonl` 适合追加记录，`run_index.json` / `run_index.md` 则适合把这些记录变成可读目录：按 method/model/dataset 汇总，并保留 `run_manifest_file`。这让你能从一份训练历史直接回到对应 run 的证据清单。

你会第一次把训练看成一组可回看、可解释、可继续使用的资产。

## 学习时常见误区

### “学习阶段不用管复现”

其实越早管越好。  
因为学习阶段正是你建立工程习惯的时候。

### “history 只是日志附属物”

不对。  
history 更像实验目录之间的连接层。

### “有 checkpoint 就等于可复现”

也不够。  
checkpoint 只是一部分；  
你还需要知道配置、数据版本、输出产物、文件指纹和导出关系。

## 实验追踪不一定一开始就要上完整平台

这是很重要的一点。  
很多人一想到实验追踪，就会想到必须立刻接一个完整平台。

但对学习来说，顺序可以更稳：

1. 先把本地 run / export / history 结构做好
2. 先保证目录和 manifest 能解释一次实验
3. 以后再接更完整的 tracking system

当前仓库就是在走这条路线。

## 这一章学完应该带走什么

训练学习真正会留下价值的，不只是模型产物，而是实验上下文。  
history、manifest 和复现意识，会决定你后面能不能把一次次练习真正积累起来。
