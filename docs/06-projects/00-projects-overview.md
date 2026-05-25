# 项目学习总览

现在这套学习站里，最重要的 4 个项目分别对应 4 种能力：

1. `inference-service`：模型服务本体
2. `ai-gateway`：平台治理和代理层
3. `eval-module`：评测、对比和最小结果展示层
4. `finetune-demo`：训练与导出产物层

也就是说，这四个项目不是四个并列 demo，而是四种不同层次的问题：

- 模型怎么被服务出来
- 请求怎么被治理
- 结果怎么被判断
- 多次结果怎么被横向观察
- 能力怎么被继续迭代

如果你把这四层关系看清楚，后面再接触更复杂系统时，就不太容易把组件混在一起。

推荐学习顺序：

1. [inference-service](/06-projects/01-inference-service)
2. [ai-gateway](/06-projects/02-ai-gateway)
3. [eval-module](/06-projects/03-eval-module)
4. [finetune-demo](/06-projects/04-finetune-demo)

这个顺序对应的是一条比较稳的系统学习线：

1. 先看执行层
2. 再看治理层
3. 再看质量闭环
4. 最后看训练迭代

它不是唯一顺序，但对第一次系统性接触这套仓库来说最稳。

如果你已经准备开始第一次动手，还是优先从 [第一次实操演练](/00-overview/04-first-walkthrough) 进入最顺。

如果你想知道“某篇文档大概对应仓库里的哪些项目和文件”，再接着看：

- [文档与项目怎么联动](/06-projects/05-docs-and-projects-map)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [质量与维护入口](/06-projects/07-quality-and-maintenance)

## 每个项目最适合解决哪类困惑

### 如果你最困惑的是“请求到底怎么产生结果”

先看 [inference-service](/06-projects/01-inference-service)。

### 如果你最困惑的是“为什么还要多一层 gateway”

先看 [ai-gateway](/06-projects/02-ai-gateway)。

### 如果你最困惑的是“跑完之后怎么判断结果好不好”

先看 [eval-module](/06-projects/03-eval-module)。

这里不仅看单次分数，也看 run bundle、compare、history 和最小 leaderboard 如何串起来。

### 如果你最困惑的是“训练为什么会留下这么多产物”

先看 [finetune-demo](/06-projects/04-finetune-demo)。

## 这四个项目在当前仓库里最重要的学习价值

这套仓库并不是在用四个项目拼一个完整商业产品，  
而是在用四个最小项目，帮助你建立四类最重要的 AI Infra 直觉：

- 服务直觉
- 平台直觉
- 评测直觉
- 训练直觉

只要这四种直觉建立起来，后面无论你继续做真实代码接入、替换后端、还是用别的大模型细化实现，都会容易很多。
