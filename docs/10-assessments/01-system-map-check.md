# 系统地图自测

这页检查你是否真正理解这个仓库为什么分成四个项目，以及这些项目之间的边界。

## 自测前准备

先打开这些页面：

- [什么是 AI Infra](/00-overview/01-what-is-ai-infra)
- [项目学习总览](/06-projects/00-projects-overview)
- [四个项目怎么连成系统](/06-projects/06-end-to-end-system-map)
- [文档与代码怎么对应](/00-overview/05-docs-to-code-map)

然后在不看答案的情况下，用一张纸或一个文档写出：

```text
执行层：
治理层：
质量层：
训练层：
每一层的输入：
每一层的输出：
每一层最重要的失败路径：
```

## 题目 A：四层系统地图

请回答：

1. `inference-service` 解决的核心问题是什么？
2. `ai-gateway` 为什么不能只理解成 HTTP proxy？
3. `eval-module` 为什么属于质量闭环，而不是普通脚本？
4. `finetune-demo` 为什么强调 run、checkpoint、export，而不是只强调训练命令？
5. 如果一个请求返回 `401`，你应该优先检查哪一层？
6. 如果一个请求返回 `502`，你应该优先检查哪一层和哪条下游链路？
7. 如果 eval compare 失败，为什么不应该立刻归因到模型能力下降？
8. 如果 export manifest 缺字段，为什么这会影响复现？

## 题目 B：代码定位

请在项目里找到这些入口，并写出它们的职责：

| 目标 | 你要找到什么 |
| --- | --- |
| inference API | chat completion 的 HTTP 入口 |
| inference engine | mock engine 或 OpenAI-compatible adapter |
| gateway proxy | 接收外部请求并转发到 upstream 的逻辑 |
| gateway routing | 外部模型名映射到内部 target 的逻辑 |
| eval runner | 执行一次评测 run 的逻辑 |
| eval comparison | 比较两个 run 的逻辑 |
| finetune trainer | 生成训练 run 资产的逻辑 |
| finetune export | 从 checkpoint 生成 export 资产的逻辑 |

要求不是背路径，而是能解释“为什么这个文件在这里”。

## 题目 C：系统行为推理

请解释下面几个场景：

### 场景 1：gateway 正常，但 inference-service 没启动

你预期会看到：

- gateway `/health` 怎么变化
- chat completion 返回什么类型的错误
- smoke 测试中哪类步骤会失败

### 场景 2：inference-service 正常，但请求里没有认证头

你预期会看到：

- 错误来自 gateway 还是 inference-service
- HTTP status 应该是什么
- 这类失败是否应该计入 upstream failure

### 场景 3：两次 eval run task 不同，却被拿来 compare

请解释为什么系统应该拒绝比较。  
再说明如果不拒绝，会带来什么误导。

### 场景 4：finetune run 成功，但 checkpoint 不完整

请解释为什么 export 应该失败。  
再说明 manifest 在这里解决了什么问题。

## 通过标准

你可以认为自己通过了这页自测，如果你能做到：

- 不看文档画出四层结构
- 给每个项目说出一个正常路径和一个失败路径
- 找到每个项目的核心入口和测试文件
- 解释为什么 smoke 是跨项目验收，而不是单元测试替代品

## 复盘问题

做完后写下三句话：

```text
我最清楚的一层是：
我最容易混淆的一层是：
我下一步应该回看哪一页：
```

