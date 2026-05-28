# 失败案例手册

> 本页解决：把四类常见失败整理成可触发、可观察、可定位、可修复的工程案例。
> 读完能做：按症状、命令、证据、定位路径、修复方式和复盘问题写出自己的失败案例。
> 关联代码：`projects/ai-gateway`、`projects/inference-service`、`projects/eval-module`、`projects/finetune-demo`、`scripts/integration_smoke_test.sh`。
> 验证命令：`PYTHON=.venv/bin/python make infra-smoke`。

失败案例不是为了证明项目不稳定，而是为了训练读者：AI Infra 里最有价值的能力，常常是把“看起来坏了”变成“知道坏在哪里、证据是什么、修完怎么验证”。

## 案例一：Gateway upstream timeout

### 症状

客户端请求 gateway 后返回 `502`、`504` 或等待很久。用户只看到请求失败，但不知道是鉴权、路由、gateway 还是 inference-service 的问题。

### 触发命令

学习环境可以先用一个不存在或不可达的 upstream 配置复现。真实实现前，至少用 failure summary 和 request timeline 练习定位：

```bash
curl -sD - -X POST http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_timeout_demo_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"timeout demo"}]}'
```

如果要构造真实 timeout，后续 lab 可以把 upstream target 指向一个会 sleep 的测试服务。

### 观察证据

```bash
curl -s 'http://localhost:8080/events/requests/req_timeout_demo_1'
curl -s 'http://localhost:8080/events/failures'
curl -s http://localhost:8080/metrics
curl -s http://localhost:8000/health
```

重点看：

- gateway 是否记录 `upstream_attempt`
- failure summary 是否出现 timeout 或 upstream error
- inference `/health` 是否健康
- gateway metrics 是否有 upstream error 或 fallback

### 定位路径

1. 先看响应 header 中的 `x-request-id`。
2. 用 request id 查 gateway timeline。
3. 如果 gateway 没有进入 upstream call，优先查 auth、rate limit、model mapping。
4. 如果进入 upstream call 但 inference 无对应 request id，怀疑网络、端口、timeout。
5. 如果 inference 有 request id 但失败，进入 inference events。

### 修复方式

- 调整 upstream URL 或端口。
- 给 gateway 增加合理 timeout 和错误映射。
- 在 events 中明确 `upstream_timeout`。
- 如果允许 fallback，必须记录 `x-fallback-used` 和 fallback metrics。
- smoke 增加 timeout 失败路径验证。

### 复盘问题

- 客户端看到的 status 是否能表达 upstream timeout？
- request id 是否贯穿到了失败事件？
- timeout 后是否触发 fallback？
- fallback 如果成功，release / eval 是否知道主路径不健康？

## 案例二：Fallback used

### 症状

客户端返回 `200`，但 header 里出现 `x-fallback-used: true`，或者 events 显示主 upstream 失败后走了备用目标。

### 触发命令

```bash
curl -sD - -X POST http://localhost:8080/v1/chat/completions \
  -H 'Authorization: Bearer dev-gateway-key-1' \
  -H 'X-Request-ID: req_fallback_demo_1' \
  -H 'Content-Type: application/json' \
  -d '{"model":"vllm-local","messages":[{"role":"user","content":"fallback demo"}]}'
```

### 观察证据

```bash
curl -s 'http://localhost:8080/events/requests/req_fallback_demo_1'
curl -s 'http://localhost:8080/events/failures'
curl -s http://localhost:8080/metrics
```

重点看：

- `x-fallback-used`
- `x-upstream-model`
- `ai_gateway_fallback_attempts_total`
- request timeline 中是否有主 upstream error 和 fallback success

### 定位路径

1. 不要被 `200` 迷惑，先看 headers。
2. 如果 fallback 使用了备用模型，确认对外模型名和内部 upstream model 是否一致。
3. 查看 failure summary，判断主 upstream 是偶发失败还是持续异常。
4. 如果这次请求进入 eval，标记运行证据：fallback 输出不一定和主模型质量等价。

### 修复方式

- 修复主 upstream 健康问题。
- 调整 fallback 策略：哪些错误可 fallback，哪些必须失败。
- 在 release brief 中把 fallback 作为 warn 信号。
- 对 fallback 结果单独跑 eval 或样本审查。

### 复盘问题

- 这次成功是否应该算作主路径成功？
- fallback 模型是否经过同样 eval？
- cache 是否可能缓存了 fallback 结果？
- 用户是否需要知道降级发生过？

## 案例三：Eval regression blocks release

### 症状

candidate 平均分看起来变化不大，甚至略有提升，但 compare report 的 `release_recommendation` 是 `block`。

### 触发命令

```bash
PYTHON=.venv/bin/python make infra-smoke
```

或者只运行 compare：

```bash
cd projects/eval-module
PYTHON=../../.venv/bin/python PYTHONPATH=src ../../.venv/bin/python -m eval_module.main compare \
  --baseline ../../.tmp/smoke/eval/baseline.json \
  --candidate ../../.tmp/smoke/eval/baseline.json \
  --output ../../.tmp/eval/compare.json
```

### 观察证据

```text
.tmp/smoke/eval/compare.json
.tmp/smoke/eval/compare.md
.tmp/smoke/eval/baseline/sample_analysis.json
.tmp/smoke/eval/comparison_index.json
.tmp/evidence/evidence_packet.md
```

重点看：

- `release_recommendation`
- `release_reasons`
- `regression_count`
- `settings_changed`
- failed sample 或 low score sample

### 定位路径

1. 先确认 baseline 和 candidate 是否可比。
2. 再看 delta 是否超过 min threshold。
3. 检查 regression 是否集中在核心能力。
4. 回到 sample outputs，确认是不是 judge 偏差或真实退化。
5. 结合 gateway / inference events，确认评测期间没有 fallback、timeout、cache 异常。

### 修复方式

- 修 prompt、模型或 adapter 后重跑 candidate。
- 固定 eval settings，避免不可比。
- 增加关键样本集，防止平均分掩盖退化。
- release notes 中如实标注 warn / block，不要改报告来迎合发布。

### 复盘问题

- block 的证据来自质量、配置、运行还是资产？
- 如果人工不同意 block，需要补什么证据？
- 这次 gate 是否应该进入 starter issue 或 regression lab？
- release brief 是否能解释阻断原因？

## 案例四：Finetune export manifest lineage mismatch

### 症状

export manifest 指向的 run、checkpoint 或 dataset 和实际产物不一致。模型或 adapter 文件可能存在，但无法证明它来自哪份数据和哪次训练。

### 触发命令

先生成正常产物：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

然后查看 export manifest：

```bash
cat .tmp/smoke/finetune/exported/export_manifest.json
```

后续 lab 可以通过人为修改 manifest 中的 dataset id 或 checkpoint pointer 来构造 mismatch。

### 观察证据

```text
.tmp/smoke/finetune/run/run_manifest.json
.tmp/smoke/finetune/run/checkpoints/checkpoint_index.json
.tmp/smoke/finetune/exported/export_manifest.json
.tmp/smoke/finetune/dataset_registry.jsonl
.tmp/smoke/finetune/export_index.json
```

重点看：

- export manifest 的 `lineage`
- run manifest 的 dataset id 和 model
- checkpoint index 的 checkpoint path 和 hash
- dataset registry 的 dataset version 和 sha

### 定位路径

1. 从 export manifest 开始，找到来源 run 和 checkpoint。
2. 用 checkpoint index 确认 checkpoint 是否属于这个 run。
3. 用 run manifest 确认 dataset id、dataset version、model、method。
4. 用 dataset registry 确认 dataset hash 是否一致。
5. 如果任何一环对不上，export 不应该进入 eval 或 release。

### 修复方式

- 重新 export，确保 checkpoint 来自正确 run。
- 修复 manifest 生成逻辑，而不是手动改 JSON。
- 给 export index 增加 lineage consistency check。
- release gate 中把 lineage mismatch 视为 `block`。

### 复盘问题

- 这个 export 能否被别人复现？
- eval candidate 是否引用了正确 export？
- 如果 dataset 变了，run history 是否能看出来？
- manifest mismatch 是否应该变成自动检查？

## 总结

四类失败对应四种工程意识：

| 失败 | 训练的能力 |
| --- | --- |
| upstream timeout | 用 request id 和 failure summary 定位跨服务错误 |
| fallback used | 不被成功响应迷惑，识别平台降级风险 |
| eval regression blocks release | 用质量证据保护发布主线 |
| lineage mismatch | 用 manifest 保护训练资产复现 |

读完之后，建议回到 [验证矩阵](/09-reference/07-validation-matrix)，把每类失败对应到应该运行的检查命令。
