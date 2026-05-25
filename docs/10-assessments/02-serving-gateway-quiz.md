# Serving 与 Gateway 自测

这页检查你是否理解执行层和治理层的边界。

建议先完成：

- [Serving 可观测性 Lab](/07-hands-on-labs/01-serving-observability-lab)
- [Gateway 韧性 Lab](/07-hands-on-labs/02-gateway-resilience-lab)

## A. 基础概念

请用自己的话回答：

1. token、context、prompt、completion 分别是什么？
2. prefill 和 decode 为什么会影响延迟结构？
3. TTFT 和总耗时的差别是什么？
4. streaming 为什么能改善体感延迟，但不能让模型真的更快完成？
5. KV cache 解决的是什么重复计算问题？
6. prefix caching 和普通 response cache 的边界在哪里？
7. inference-service 为什么不负责用户鉴权？
8. gateway 为什么适合做模型名映射？

## B. 请求路径

请描述一次普通非 streaming 请求的路径：

```text
client
-> ai-gateway
-> inference-service
-> engine
-> inference-service
-> ai-gateway
-> client
```

要求说明每一段至少做一件事：

| 阶段 | 你需要说明 |
| --- | --- |
| client -> gateway | 认证头、模型名、请求体 |
| gateway -> inference | 路由、request id、下游 header |
| inference -> engine | 请求对象如何进入 engine |
| engine -> inference | 生成结果或抛出错误 |
| inference -> gateway | status、body、request id |
| gateway -> client | 是否缓存、是否 fallback、metrics |

## C. Streaming 路径

请回答：

1. SSE 响应为什么不能完全等同普通 JSON 响应？
2. streaming 已经发出第一段 chunk 后，再失败时为什么不能简单改成普通 `502`？
3. gateway 在 streaming fallback 上为什么要区分“首个 chunk 前”和“首个 chunk 后”？
4. streaming error event 对客户端有什么价值？
5. 哪些 metrics 应该能反映 streaming 请求？

## D. 错误语义

请填写下面表格：

| 场景 | 期望 status | 主要归属层 | 你会先看哪里 |
| --- | --- | --- | --- |
| 缺少认证头 |  |  |  |
| 认证格式错误 |  |  |  |
| 模型名不存在 |  |  |  |
| 超过限流 |  |  |  |
| upstream 5xx |  |  |  |
| engine adapter 映射上游错误 |  |  |  |
| request body 缺少 messages |  |  |  |

## E. 代码阅读任务

请打开对应项目，完成这些定位：

1. 找到 inference-service 的 `/health`
2. 找到 inference-service 的 `/metrics`
3. 找到普通 chat completion 入口
4. 找到 streaming chat completion 路径
5. 找到 engine error 到 HTTP error 的映射
6. 找到 gateway 的认证逻辑
7. 找到 gateway 的限流逻辑
8. 找到 gateway 的 fallback 候选选择
9. 找到 gateway response cache 的 key 设计
10. 找到 request id 在两个服务之间如何传递

写下每个定位对应的文件和函数。  
如果你只能找到文件但解释不出函数职责，还没有真正通过。

## F. 实操题

在本地运行：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

然后解释 smoke 里的这些步骤：

- `IT-00 gateway upstream health`
- `IT-01b direct inference`
- `IT-01 gateway proxy`
- `IT-01c gateway stream proxy`
- `IT-04 no auth`
- `IT-06 unknown model`
- `IT-07 gateway metrics`
- `IT-07b inference metrics requests`
- `IT-07c inference prompt token metric`
- `IT-07d inference completion token metric`

每一步至少说明：

- 它验证哪一层
- 它覆盖正常路径还是失败路径
- 如果失败，你第一反应会查哪里

## G. 加分题

任选一个改进方向，写出设计方案和验证方式：

1. 给 gateway 增加更细的 upstream timeout 分类
2. 给 inference-service 增加更明确的 engine latency metric
3. 给 streaming 响应增加更完整的 error event schema
4. 给 cache 增加更可观察的 hit / miss reason

要求说明：

- 你会改哪些文件
- 你会新增哪些测试
- 你担心什么兼容性问题
