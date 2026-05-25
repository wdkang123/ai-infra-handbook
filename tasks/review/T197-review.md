# Review Note

Task ID: T197  
Task Title: 产出 LoRA / PEFT 章节初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. 最小实践代码示例中把 `LoraConfig` 从 `transformers` 导入，这会误导读者；当前主流用法应来自 `peft`。
2. 第 8 节硬编码了一组具体的 `trainable params` 输出，这类数值强依赖模型和配置，不适合作为通用章节里的固定结果。
3. 第 4 节把 Unsloth 写进“常见方案 / 组件”没有问题，但当前章主体应更聚焦 LoRA / QLoRA / PEFT 本身，避免加速层喧宾夺主。

## Action

- 修正最小实践的导入和示例代码，使其至少在接口层面是正确的
- 删除具体的硬编码参数输出，改成“可打印 trainable params 占比”
- 收紧 Unsloth 的出现频率，保持它作为相关工具而不是主角
