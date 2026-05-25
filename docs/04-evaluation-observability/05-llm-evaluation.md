# LLM Evaluation

## 先把 evaluation 放在什么位置理解

evaluation 更适合先理解成：  
**系统已经能跑了之后，你如何判断它输出得好不好。**

这句话里有两个重点：

1. 它关心的是输出质量
2. 它通常建立在“请求已经能被系统执行”这件事之上

所以 evaluation 和 inference、gateway、observability 都有关，但又不是同一层。

## 为什么它是单独一条主线

因为一个系统“跑通”并不代表它“答案靠谱”。

你完全可能遇到这种情况：

- 服务稳定
- 延迟正常
- metrics 也很好看

但模型回答质量就是不行。  
这时 observability 解决不了全部问题，evaluation 才是真正的下一层。

## evaluation 最核心在回答什么

它主要在回答三类问题：

### 1. 模型选型问题

哪一个模型更适合当前任务。

### 2. 版本回归问题

新版本上线后，质量有没有变差。

### 3. 场景边界问题

这个模型在什么任务上表现好，在什么任务上容易翻车。

## evaluation 常见的三种思路

### 标准 benchmark

这是最容易形成结构化结果的一类。  
优势是可重复、可比较；限制是任务边界较固定。

### LLM-as-Judge

更适合开放式任务。  
当“正确答案”很难写成规则时，让更强模型来做判断，会更灵活。

### Heuristic / rule-based eval

适合有明确标准答案或明确规则的任务。  
这类评测比较硬，但可解释性通常更强。

## 学习时最值得先建立的判断

### 判断一：evaluation 不是 observability 的附属物

两者关系很近，但不是包含关系。  
observability 描述系统行为；evaluation 描述输出质量。

### 判断二：单次分数不够

真正有用的 evaluation，通常至少还要留下：

- task
- model
- backend
- run metadata
- 原始输出或结果 bundle

这就是为什么当前仓库里的 `eval-module` 会特别强调 run、compare、history。

### 判断三：评测不是只有排行榜

排行榜只是结果展示的一种形式。  
evaluation 本身更像一套执行、比较、沉淀结果的过程。

## 在当前仓库里怎么对应

当前 `eval-module` 的价值，不在于它已经是完整 benchmark 平台，  
而在于它把评测最重要的结构先收出来了：

- run
- compare
- result bundle
- history

这会帮助你建立一个很关键的直觉：

评测不是一次性命令，而是一种可追踪、可比较、可沉淀的对象化流程。

## 学习时常见误区

### “有 benchmark 分数就够了”

不够。  
因为你还需要知道那次分数是怎么来的，以及和上次有什么不同。

### “evaluation 只在大模型选型时才有用”

也不对。  
即使是同一个模型，不同 prompt、不同版本、不同部署方式，也都可能需要评测。

### “先把系统做完，评测以后再说”

风险很大。  
因为如果不早点建立评测习惯，后面系统一复杂，质量回归会更难追。

## 这一章学完应该带走什么

evaluation 是输出质量层。  
它和 inference、gateway、observability 一起，才构成一条完整的 AI Infra 学习主线。
