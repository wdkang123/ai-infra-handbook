# Task Card

Task ID: T113  
Title: 重做 Triton 资料包，目标改为 NVIDIA Triton Inference Server  
Owner: MINIMAX  
Type: D-资料型任务  
Priority: P0

## Input

参考 `tasks/review/T103-review.md`。  
本任务中的 Triton 明确指 **NVIDIA Triton Inference Server**，不是 OpenAI Triton language/compiler。

## Expected Output

输出一份结构化资料包，至少包含：

1. 官方文档入口
2. 官方 GitHub 仓库
3. 核心定位
4. 模型仓库 / backend / protocol 支持摘要
5. 与 `vLLM`、`SGLang` 的边界说明
6. 最近 6-12 个月值得关注的更新线索
7. 5 到 8 个优先阅读链接

## Template

使用 MiniMax 标准输出协议。

## Acceptance Criteria

- 全部围绕 NVIDIA Triton Inference Server
- 至少 6 个精确官方链接
- 明确说明它是推理服务平台，不是 kernel/compiler 项目
- 边界说明清楚，但不做全面优劣评判

## Allowed Sources

- `https://docs.nvidia.com/`
- `https://github.com/triton-inference-server/`
- NVIDIA 官方博客 / release notes

## Out of Scope

- 不写 Triton language/compiler
- 不写部署教程细节
- 不做完整对比结论
