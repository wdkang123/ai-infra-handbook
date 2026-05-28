# 公开数据与证据规范

> 本页解决：公开仓库里哪些数据、日志、截图和证据可以提交，哪些必须脱敏或禁止提交。
> 读完能做：把 toy data、request id、events、metrics、eval report、manifest 和 evidence packet 整理成可公开材料。
> 关联代码：`SECURITY.md`、`scripts/security_scan.py`、`projects/finetune-demo/data`、`scripts/build_evidence_packet.py`。
> 验证命令：`PYTHON=.venv/bin/python make public-check`。

这个项目鼓励读者提交可复现证据，但公开证据必须安全。原则很简单：

1. 用 toy data 解释机制。
2. 用占位符替代真实账号、路径、endpoint 和 token。
3. 用 request id 串联证据，但不要暴露真实用户内容。
4. 任何不确定是否敏感的材料，都先不要公开贴。

## 可以提交

| 材料 | 要求 |
| --- | --- |
| toy prompt | 不包含真实用户、客户、公司、内部项目、隐私内容 |
| request id | 使用 `req_demo_*`、`req_smoke_*`、`req_lab_*` 这类示例值 |
| events 输出 | 只保留字段结构、状态、耗时、错误类型和脱敏摘要 |
| metrics | 可以提交计数器、直方图、标签名，不提交真实业务标签 |
| eval report | 使用示例任务和 toy samples |
| manifest | 数据集、checkpoint、export 使用示例 id 和相对路径 |
| screenshot | 不包含浏览器账号、邮箱、真实路径、token 或私有 repo |

## 不应提交

| 材料 | 风险 |
| --- | --- |
| `.env`、API key、Bearer token、cookie | 直接泄露凭据 |
| 真实用户对话、客服记录、工单、日志 | 可能包含隐私和业务机密 |
| 私有模型权重、checkpoint、dataset dump | 文件大且许可不清 |
| 本机绝对路径、内网 endpoint、私有 IP | 暴露个人或组织环境 |
| 云账号、项目 id、bucket 名、registry 地址 | 可能被关联到真实资源 |
| 未授权 benchmark 或第三方数据 | 许可和复用风险 |

## Toy data checklist

给 `finetune-demo` 或 eval 示例补数据时，先回答：

- 数据来源是否可公开解释
- 是否完全由示例内容构造
- 是否没有真实个人、公司、客户、账号、地理位置、联系方式
- 是否没有复制受版权保护的大段文本
- schema 是否和文档一致
- manifest 是否能追溯到 dataset registry
- eval 样本是否能解释 pass / warn / block 的判断

## Evidence sanitization checklist

提交证据前，逐项检查：

- request id 是否是示例 id
- headers 是否移除了 `Authorization`、cookie、真实 trace id
- events 是否移除了 prompt 原文中的敏感信息
- metrics 标签是否没有 tenant、user、org、project 的真实值
- eval report 是否没有真实业务样本
- manifest 是否没有本机绝对路径
- 图片是否没有账号头像、邮箱、浏览器个人资料和私有 tab
- markdown 里是否没有复制真实错误日志里的 token

## 推荐占位符

| 场景 | 占位符 |
| --- | --- |
| API key | `dev-gateway-key-1`、`sk-placeholder` |
| request id | `req_demo_001`、`req_lab_timeout_1` |
| user id | `user_demo_1` |
| tenant | `tenant_demo` |
| model | `vllm-local`、`mock-fast` |
| endpoint | `http://localhost:8080`、`https://example.invalid` |
| path | `./data/toy-dataset.jsonl`、`./artifacts/demo-run` |

## PR 里的证据怎么写

推荐写成短证据链：

```markdown
## Evidence

- request id: `req_lab_timeout_1`
- events: `/events/requests/req_lab_timeout_1`
- metrics: `gateway_upstream_failures_total` increased by 1
- eval report: `.tmp/smoke/eval/compare.md`
- manifest: `.tmp/smoke/finetune/export_manifest.json`
- evidence packet: `.tmp/evidence/evidence_packet.md`
```

不要贴真实 key、真实 prompt、真实用户输出。需要说明内容时，写脱敏摘要：

```text
prompt_summary: "toy request asking the mock model to explain gateway timeout"
```

## 发现误提交怎么办

如果你发现 PR、issue、commit 或截图里出现敏感内容：

1. 立即删除公开评论或关闭 PR。
2. 不要在新的公开评论里复述敏感内容。
3. 按 `SECURITY.md` 的方式报告。
4. 轮换已经泄露的 token 或凭据。
5. 等维护者确认处理方式后再重新提交脱敏版本。

安全问题优先级高于功能推进。公开学习项目越容易传播，越要把证据边界讲清楚。

## 继续阅读

- [First PR Playbook](/community/01-first-pr-playbook)
- [失败案例手册](/11-case-studies/06-failure-case-playbook)
- [示例输出与证据库](/13-output-gallery/00-overview)
- [公开仓库卫生规范](/08-publication/06-public-repo-hygiene)
