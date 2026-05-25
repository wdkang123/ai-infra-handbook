# Task Card

Task ID: T310
Title: 产出 observability comparison-index v1
Owner: MINIMAX
Type: C-普通章节任务
Priority: P1

## Input

基于：
- `tasks/accepted/T204-observability-chapter-revision.md`
- `tasks/accepted/T307-observability-sources-index-v1.md`

## Expected Output

产出一个 `comparison-index v1`，比较对象至少包含：

- OpenTelemetry
- Langfuse
- Phoenix
- TensorZero
- Grafana / Prometheus

比较维度至少包含：

- 定位
- 所处层级
- 典型使用场景
- 与本项目的关系

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 保持 comparison-index 风格，不扩写成章节
- 每个维度给出来源
- 清楚区分标准/采集层、observability 平台、指标展示层
- 不做排名式结论

## Allowed Sources

- 已通过的 T204 / T307

## Out of Scope

- 不扩写成 observability 手册
- 不做厂商横评
