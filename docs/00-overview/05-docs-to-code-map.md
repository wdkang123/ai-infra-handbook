# 文档与代码怎么对应

## 为什么这一页值得先看

因为这套仓库本来就不是纯文档站，也不是纯代码仓库。  
它真正想做的，是把：

- 学习内容
- 可运行脚手架
- 观察结果

三者绑成一条学习路径。

所以一个更高效的学习方式，不是“先把文档全部看完”或“先把源码全部翻完”，  
而是知道每一组内容大概对应哪一层代码。

## 最粗的一张对应图

先记这张最粗的图就够了：

```text
基础概念 -> 推理请求生命周期的共同语言
推理服务 -> inference-service
平台层 -> ai-gateway
评测与观测 -> eval-module + metrics / smoke
微调训练 -> finetune-demo
```

你后面如果发现自己“概念懂了一点，但不知道该回哪里看”，就回到这张图。

## 这页应该怎么用

这页不建议一次性背完。更好的用法是：每读完一个概念页，就回到这里找一个最小代码入口，然后只带着一个问题去看代码。

比如你刚读完“request id 为什么重要”，不要马上打开整个 `projects/` 目录。先问自己：

- request id 是从哪里进入系统的？
- 如果调用方没有传 request id，谁负责生成？
- 它会不会继续传给下游？
- 响应 header、events、metrics 里哪里能看到它？

然后只看 gateway 和 inference 的入口文件。这样你不是在“阅读源码”，而是在验证一个系统假设。

这也是本仓库希望训练的能力：不是把每个文件都看完，而是知道一个问题应该落到哪一层、哪几个文件、哪条命令和哪份输出证据。

## 三种常见阅读方式

不同阶段适合不同的读法。

| 读法 | 适合阶段 | 你要做什么 | 不要做什么 |
| --- | --- | --- | --- |
| 按请求链路读 | 刚跑通第一次实操 | 从 gateway 入口追到 inference 入口 | 不要先研究所有配置项 |
| 按产物读 | 开始看 eval / finetune | 从输出 JSON / manifest 反推生成代码 | 不要只看命令帮助 |
| 按失败路径读 | 开始做 lab 或案例 | 先看错误响应，再看事件和测试 | 不要只猜“哪里坏了” |

这三种读法会反复出现。第一次学习时，你可能只会按请求链路读；等你开始写案例复盘时，就会更多按失败路径和产物读。

## 基础概念更适合对到哪里

如果你在读：

- 模型、Token、Context
- Prefill、Decode、KV Cache
- 从请求到首个 Token

最适合对照看的通常是：

- `projects/inference-service/src/inference_service/server.py`
- `projects/inference-service/src/inference_service/runtime.py`
- `projects/ai-gateway/src/ai_gateway/server.py`

因为这些文件最容易把“一个请求是怎么走完整条链的”具体化。

### 读这些文件时重点看什么

不要把基础概念页和代码入口硬凑在一起。你要看的不是“Prefill 在代码里哪一行”，因为当前学习型实现还没有真实模型执行器；你要看的是接口层为真实执行器预留了哪些边界。

可以重点观察：

- 请求体如何表达 `model`、`messages`、`stream`
- 响应体如何保留 OpenAI-compatible 的形状
- streaming 和非 streaming 为什么共享同一个 `/v1/chat/completions`
- token usage 为什么要区分 prompt 和 completion
- engine adapter 为什么要把上游错误转换成结构化错误

这些结构一旦理解了，后面接真实 vLLM、SGLang 或其他 OpenAI-compatible backend 时，就不会把 API 层、执行层和观测层混成一团。

## 推理服务章节更适合对到哪里

如果你在读：

- vLLM
- SGLang
- Cache / Prefix Caching
- Streaming、Batching、Metrics

最适合先回看的就是 `inference-service`。

虽然当前仓库还没有把真实 vLLM / SGLang 深度接满，  
但它已经把理解 serving 最重要的结构留出来了：

- 普通响应
- streaming
- metrics
- request lifecycle

所以它很适合当“真实框架接入前的学习骨架”。

### 从文档问题落到代码问题

读推理服务章节时，可以把每个概念变成一个代码问题：

| 文档问题 | 代码里应该找什么 | 输出里应该看什么 |
| --- | --- | --- |
| 服务是否健康 | `/health` 路由和 runtime 状态 | health JSON |
| 请求是否成功 | chat completions 入口 | 状态码、响应 body、`x-request-id` |
| streaming 是否真的发生 | SSE 生成逻辑 | `data:` chunk 和结束事件 |
| token usage 是否有区分 | usage 估算逻辑 | `prompt_tokens` / `completion_tokens` |
| 上游失败如何表达 | engine error 映射 | `502` 或 SSE error event |

如果你能把这张表走完一遍，就已经不是只会“调用接口”，而是开始理解推理服务的最小工程边界。

## 平台层章节更适合对到哪里

如果你在读：

- 鉴权、路由、限流
- 健康检查、Request ID
- 平台层与模型服务层边界
- 外部模型名与内部目标映射

那最值得回看的就是 `ai-gateway`：

- `server.py`
- `router.py`
- `middleware/auth.py`
- `tests/test_proxy.py`

因为平台层的很多学习价值，本来就体现在边界行为里。

### 平台层最值得追的四条线

gateway 的源码不要按文件名平均用力。最值得追的是这四条线：

1. 鉴权线：请求没有 token、token 格式错误、token 不在配置里时分别怎么返回。
2. 路由线：外部模型名如何映射到下游目标、fallback 候选如何生成。
3. 代理线：非 streaming 与 streaming 请求如何转发、headers 如何回传。
4. 观测线：request id、metrics、events、failure summary 如何记录路径。

这四条线对应的是平台层的真实职责。一个 gateway 是否“像平台”，不是看它能不能转发，而是看它能不能把入口治理、下游差异和失败证据收敛到统一边界。

## 评测与观测章节更适合对到哪里

如果你在读：

- Run、Compare、History
- LLM Evaluation
- 从 Run 到发布决策
- Tracing、Metrics、Logs

最该回看的是：

- `projects/eval-module/src/eval_module/main.py`
- `projects/eval-module/src/eval_module/results/result_store.py`
- 根级 `scripts/integration_smoke_test.sh`

这里最重要的不是复杂评测算法，而是理解：

- 为什么一次 run 不是只留一个分数
- compare 为什么重要
- history 为什么能支撑长期判断

### 从结果文件反推评测系统

评测模块最好的读法不是先打开 runner，而是先打开一次 run 生成的结果目录。

可以按这个顺序反推：

1. 主结果 JSON 里有哪些字段。
2. sample outputs 为什么单独保存。
3. sample analysis 如何把样本层失败变成摘要。
4. compare 为什么会产出 recommendation，而不只是 delta。
5. run history 和 comparison history 为什么是追加式文件。
6. leaderboard 为什么从 history 聚合，而不是凭空生成。

反推完之后再看 `result_store.py`，你会更容易明白它为什么存在。它不是普通文件工具，而是把一次评测变成后续可比较、可复盘、可发布判断的证据对象。

## 微调训练章节更适合对到哪里

如果你在读：

- LoRA、QLoRA、PEFT
- 训练产物、Checkpoint、Export
- 实验追踪、History、复现
- 什么时候该微调

最适合回看的就是 `finetune-demo`：

- `main.py`
- `config.py`
- `trainer/lora_trainer.py`
- `export/adapter_exporter.py`

这里的重点不是“训练已经有多生产级”，而是你能不能看清训练工程资产到底长什么样。

### 训练代码最容易被误读的地方

第一次看 `finetune-demo` 时，很容易误以为核心只有 `train` 命令。实际上更重要的是训练前后那些“看起来不那么模型”的文件：

- 数据集校验决定坏数据能不能提前失败。
- dataset summary 决定别人能不能知道训练输入是什么。
- dataset registry 决定多次 run 之间能不能追踪输入差异。
- checkpoint index 决定 checkpoint 能不能被定位和复用。
- run manifest 决定一次训练能不能被完整复盘。
- export manifest 决定导出的 adapter 能不能追溯回训练来源。

所以读训练代码时，可以少问“这里是不是真训练”，多问“如果以后换成真训练，这些资产边界是否仍然成立”。这会比单纯追框架 API 更接近工程学习目标。

## 四条典型追踪路线

当你不知道从哪里下手时，可以直接选下面一条路线。

### 路线 1：追一条成功请求

适合刚学完 Serving / Gateway。

1. 在 gateway 打一条带 `X-Request-ID` 的请求。
2. 看响应 header 里的 request id、cache、upstream model。
3. 看 gateway `/events/requests/{request_id}`。
4. 看 inference `/events/requests/{request_id}`。
5. 对照 gateway 和 inference 的 `/metrics`。
6. 回到 `server.py` 找这些证据分别在哪里写入。

这条路线能帮你把“请求成功”拆成多个可观察证据，而不是只看 body 有没有返回。

### 路线 2：追一条失败请求

适合做 Gateway 韧性 Lab 或案例复盘。

1. 故意去掉 Authorization，观察 `401`。
2. 故意请求不存在的模型，观察 `404`。
3. 故意让下游不可用，观察 `502` 或 streaming error。
4. 看 `/events/failures` 的状态码分布。
5. 回到测试文件，找对应失败路径的断言。

这条路线能训练你区分“入口失败、路由失败、下游失败、流式中途失败”。真实系统排障时，这种分类比背概念更重要。

### 路线 3：追一次评测判断

适合学完 eval-module。

1. 跑一次 `run`。
2. 跑一次 `compare`。
3. 看 `release_recommendation` 和 `release_reasons`。
4. 看 sample analysis，确认推荐结论有没有样本证据支撑。
5. 看 comparison history，确认这次判断被追加记录。
6. 回到 `result_store.py` 看 bundle 和 history 的写入逻辑。

这条路线训练的是发布判断。它会让你意识到：评测分数只是输入，真正的工程结论要把配置、样本、历史和阈值一起看。

### 路线 4：追一次训练产物

适合学完 finetune-demo。

1. 跑一次 `train`。
2. 看 `dataset_summary.json` 和 `dataset_registry_entry.json`。
3. 看 `checkpoint_index.json`。
4. 跑一次 `export`。
5. 看 `export_manifest.json` 的 lineage。
6. 回到 `artifacts.py`、`dataset_registry.py` 和 `adapter_exporter.py`。

这条路线训练的是资产意识。你会看到一次训练不是“命令结束”，而是生成了一组未来 eval、复现、发布都要依赖的工程对象。

## 最推荐的学习动作

最稳的学习节奏通常是：

1. 先读一页文档
2. 只打开 1 到 2 个对应代码文件
3. 带着一个明确问题去看
4. 再跑一条最小命令验证

比如：

- 读完 request id，再去看 gateway 的 server
- 读完 run/history，再去看 eval 的 result store
- 读完 checkpoint/export，再去看 finetune 的 exporter

这样会比无差别翻代码更快建立结构感。

## 一次完整的代码对照练习

如果你想把这页真正用起来，可以做下面这个 45 分钟练习。

### 第一步：选一个问题

只选一个，不要贪多：

- 一条 gateway 请求如何被路由到 inference？
- 为什么 compare 能给出发布建议？
- export manifest 如何追溯到训练 run？

### 第二步：写下预期证据

在打开代码前，先写：

```text
我预计会看到的接口：
我预计会看到的输出文件：
我预计会看到的 header 或字段：
我预计最可能出错的地方：
```

这一步会迫使你先形成假设。读代码时你是在验证假设，而不是漫无目的地浏览。

### 第三步：只打开三个文件

最多三个。比如请求链路可以选：

- `projects/ai-gateway/src/ai_gateway/server.py`
- `projects/ai-gateway/src/ai_gateway/router.py`
- `projects/inference-service/src/inference_service/server.py`

如果三个文件还不够，再补第四个；但不要一开始就打开十几个文件。

### 第四步：跑一条命令验证

代码看完后必须跑一条命令。没有命令验证，理解很容易停留在“我感觉它应该是这样”。

### 第五步：写三句复盘

```text
我原来以为：
我在代码和输出里确认了：
我还不能确认的是：
```

这三句比长篇笔记更有效，因为它会把“已确认”和“未确认”分开。

## 常见误区

### 把代码入口当成源码阅读顺序

这页列出的文件不是让你从上到下逐行读完。它们是定位入口。真正的顺序应该由问题决定。

### 只看实现，不看测试

很多边界行为在测试里更清楚，比如 `401 / 404 / 429 / 502`、fallback、cache、compare threshold、dataset schema 校验。读测试不是额外工作，而是理解系统契约最快的方式。

### 只看命令，不看产物

命令成功只能说明流程跑完了，不能说明你理解了什么。至少要打开一个 header、一个 events、一个 JSON 或一个 manifest。

### 把 mock 理解成无价值

mock 不等于随便写。这里的 mock 价值在于保留接口、状态、事件、history、manifest 等工程边界。只要边界清楚，未来替换真实后端时才有路径。

### 看到生产框架名就跳过去

vLLM、SGLang、Triton、TensorRT-LLM 等页面不是要求你立刻接入生产框架，而是帮你理解当前学习型骨架以后会怎么长。先把当前骨架跑明白，再进入真实框架，会稳很多。

## 这一页学完应该带走什么

文档更像问题地图，代码更像当前实现。  
把两者连起来看，你学到的就不只是概念，也不只是源码，而是“这套系统现在为什么长成这样”。
