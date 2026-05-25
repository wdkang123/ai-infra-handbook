# Task Card

Task ID: T132  
Title: 产出推理服务 comparison-index v1 草稿  
Owner: MINIMAX  
Type: C-普通章节任务  
Priority: P0

## Input

基于以下已通过资料包：

- `tasks/accepted/T111-vllm-sources-result.md`
- `tasks/accepted/T122-sglang-sources-result.md`
- `tasks/accepted/T113-triton-inference-server-result.md`

## Expected Output

输出一份 comparison-index 草稿，比较对象仅限：

- vLLM
- SGLang
- Triton Inference Server

固定比较维度至少包含：

1. 定位
2. 主要接口形态
3. 主要优化方向
4. 典型使用场景
5. 与项目的关系
6. 不适合的场景

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 只做结构化比较，不做“谁最好”的结论
- 每个维度都要尽量有来源支撑
- 保持索引页风格，不扩写成完整章节

## Allowed Sources

- 上述已通过资料包中的官方来源

## Out of Scope

- 不加入 TensorRT-LLM
- 不写 benchmark 排名
