# Review Note

Task ID: T103  
Task Title: Triton 官方资料与核心链接搜集  
Review Decision: REVISE_REQUIRED

## Findings

1. 任务语境是“推理服务栈中的 Triton”，但结果整体写成了 OpenAI `triton-lang/triton` 编译器项目，目标组件理解错误。
2. 与 `vLLM / SGLang / Triton` 并列时，更合理的对象应是 NVIDIA Triton Inference Server，而不是 Triton language/compiler。
3. 因为目标对象错误，当前文档里的官方主页、仓库、核心定位、近况更新、优先阅读链接都整体失焦，不能直接进入手册资料库。

## Action

- 以 NVIDIA Triton Inference Server 为唯一目标重做资料包
- 重点覆盖：官方文档、GitHub、模型仓库、后端支持、HTTP/gRPC/metrics、与 vLLM/SGLang 的关系边界
- 不再混入 Triton language/compiler 内容
