# Review Note

Task ID: T172  
Task Title: 搜集 router / model routing 官方资料与核心链接  
Review Decision: REVISE_REQUIRED

## Findings

1. `vLLM` 和 `SGLang` 被列成 router 实现不够准确，它们更接近被路由的推理引擎，而不是独立 router 产品。
2. 资料包里存在一个明显坏链接：`distributedributed_serving.html`。
3. 这份材料需要更明确地区分“router 产品/组件”和“被路由的后端推理引擎”。

## Action

- 修正坏链接
- 把 vLLM/SGLang 从 router 实现名单中挪出或改成“后端引擎参考”
- 收紧术语边界
