Task ID: T601
Task Title: Inference Core Zero-Touch Pack
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
围绕推理栈选型给出资料级输入：本地开发默认路线、服务化分工边界、TensorRT-LLM 前提条件。

Result:

# Inference Stack Decision Memo v1

## 概述

本文档围绕推理栈选型的关键决策点，给出资料级输入，帮助 Codex 做最终判断。

---

## 决策点一：本地开发推理栈默认路线

### 推荐候选：vLLM

**理由**：
- **接入成本低**：pip install vllm，无需编译
- **动态加载**：模型切换灵活，适合研发迭代
- **生态成熟**：文档完善，社区活跃，问题易解
- **OpenAI 兼容**：API 与 OpenAI 接口一致，降低 gateway 适配成本

### 备选：SGLang

**适用条件**：
- 多轮对话场景（prefix caching 收益大）
- 需要更细粒度的调度控制
- 需要 RadixAttention 特有能力

### 不推荐作为默认：TensorRT-LLM

**原因**：
- 必须预编译，模型切换成本高
- 编译时间长（数GB模型可能需要数十分钟）
- 适合明确模型、固定部署的生产环境，不适合快速迭代

### 资料级建议

| 阶段 | 推荐默认 | 理由 |
|------|---------|------|
| 本地开发 / 快速验证 | vLLM | 动态加载，切换灵活 |
| 多轮对话为主 | SGLang | RadixAttention 前缀复用 |
| 生产环境（已确定模型） | vLLM 或 TensorRT-LLM | 视性能需求而定 |

来源：https://docs.vllm.ai/
来源：https://sglang.readthedocs.io/

---

## 决策点二：服务化场景下 Triton / vLLM / SGLang 的分工边界

### 分工框架（资料级）

```
ai-gateway（路由 / 鉴权 / 限流）
    ↓
Triton IS（可选：多模型编排 / 动态批处理）
    ↓
vLLM / SGLang（推理引擎，实际计算）
```

### 何时需要 Triton IS

**需要 Triton**：
- 需要同时管理多个推理引擎（TensorRT-LLM + vLLM）
- 需要统一 HTTP/gRPC 接口
- 需要模型 ensemble（多模型串联）

**不需要 Triton**：
- MVP 阶段只需要 vLLM/SGLang 之一
- 模型数量少，不需要统一编排
- 追求简单，不想增加运维复杂度

### vLLM vs SGLang 分工

| 场景 | 推荐 | 理由 |
|------|------|------|
| 单引擎推理 | vLLM 或 SGLang 均可 | 选谁取决于模型特性 |
| 多轮对话为主 | SGLang | RadixAttention 优势 |
| 快速迭代为主 | vLLM | 动态加载，切换快 |

### 资料级建议

- **MVP 阶段**：ai-gateway → vLLM/SGLang 直连，不引入 Triton
- **后续迭代**：根据是否需要多模型编排决定是否引入 Triton

来源：https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/

---

## 决策点三：TensorRT-LLM 更适合什么前提条件

### TensorRT-LLM 的定位

TensorRT-LLM 是"极致性能"路线，适合已确定模型、不需要频繁切换的生产环境。

### 必要前提条件

| 条件 | 说明 |
|------|------|
| **模型已确定** | 编译耗时，频繁切换模型则不适合 |
| **性能是主要矛盾** | 对延迟/吞吐量有明确 SLA |
| **GPU 型号明确** | TensorRT-LLM 与 GPU 型号强相关（Hopper/Ampere） |
| **运维能力足够** | 编译 + 部署流程比 vLLM 复杂 |
| **显存充足** | 编译时需要足够显存 |

### 不适合 TensorRT-LLM 的场景

- 本地开发、快速验证（模型频繁切换）
- 模型种类多、需要动态路由
- 团队没有 NVIDIA GPU 使用经验

### 资料级建议

TensorRT-LLM 适合在以下条件满足后引入：
1. 模型已确定，不需要频繁更换
2. 性能成为明确瓶颈或明确需求
3. 团队有足够时间做编译优化验证

来源：https://nvidia.github.io/TensorRT-LLM/

---

## 总结：资料级建议（不下结论）

| 决策点 | 建议方向 | 关键依据 |
|--------|---------|---------|
| 本地开发默认 | vLLM | 动态加载，生态成熟 |
| 服务化引入 Triton | MVP 不引入，后续按需 | 运维复杂度增加 |
| TensorRT-LLM 时机 | 模型确定 + 性能优先 | 需要编译，灵活度低 |

---

## 需要 Codex 最终判断

1. **本地开发默认是否确认用 vLLM**？
2. **Triton IS 是否在 MVP 阶段引入**？
3. **TensorRT-LLM 是否作为后续性能优化的必选**？

Sources:
1. https://docs.vllm.ai/ — vLLM
2. https://sglang.readthedocs.io/ — SGLang
3. https://docs.nvidia.com/deeplearning/triton-inference-server/ — Triton IS
4. https://nvidia.github.io/TensorRT-LLM/ — TensorRT-LLM

Risk of Staleness:
- 各引擎版本更新快，具体功能以实际版本为准
- TensorRT-LLM 与 GPU 型号相关

Out of Scope Kept:
- 未写代码实现
- 未写部署配置文件
- 未写性能 benchmark 结果
