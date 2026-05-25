Task ID: T111
Task Title: 修订 vLLM 资料包，补精确官方链接并拆分主项目/Omni/Ascend
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T101 初稿和 review note T101 修订。要求区分 vllm 主项目 / vllm-omni / vllm-ascend，所有链接精确化，删除无关来源，把历史 benchmark 数字与当前能力分开。

Result:

## 一、项目关系说明

- **vLLM 主项目**（`vllm-project/vllm`）：LLM 推理与服务引擎，GPU 上的主力实现
- **vLLM-Omni**（`vllm-project/vllm-omni`）：独立子项目，针对全模态模型（文本/图像/音频/视频统一生成）的推理框架，非主仓库一部分
- **vLLM-Ascend**（`vllm-project/vllm-ascend`）：社区维护的华为昇腾 NPU 硬件插件，独立仓库，非主仓库一部分

## 二、vLLM 主项目资料包

### 官方入口
- 文档站：https://docs.vllm.ai/
- GitHub 仓库：https://github.com/vllm-project/vllm
- 最新 release（v0.18.0，2026-03-25）：https://github.com/vllm-project/vllm/releases/latest

### 核心特性（当前主线稳定能力）
- **PagedAttention**：KV cache 分页管理，减少显存碎片，提升显存利用率（来源：vLLM 主仓库 README）
- **Continuous Batching（Iteration-level Scheduling）**：以单次 token 生成为调度粒度动态批处理，吞吐量优于静态 batching（来源：vLLM 文档 / architecture 设计文档）
- **OpenAI 兼容 API**：REST + gRPC 双接口，兼容 OpenAI API 格式（来源：https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html）
- **多硬件后端**：CUDA（主力）、ROCm、CPU（AVX512）、Neuron、Intel OpenVINO（来源：主仓库 README）

### 历史性能数据（标注为历史背景，非当前能力）
- 早期 blog 声称"比 HuggingFace Transformers 高 14-24 倍吞吐量"——为 vLLM 团队早期 benchmark，结果来自特定硬件（V100/A100）和特定模型，不应作为当前通用能力引用
- 来源：https://www.vllm.ai/（官方 blog，发布于 PagedAttention 论文公开初期）

### 近 6-12 个月稳定更新线索（主线）
- **v0.17.0**（2026-03）：PyTorch 2.10 升级（breaking change），FlashAttention 4 集成，699 commits from 272 contributors
- **v0.18.0**（2026-03-25）：gRPC serving 支持（`--grpc` flag），GPU-less Render Serving（`vllm launch render`），Engine Core Model Runner V2
- 来源：https://github.com/vllm-project/vllm/releases/tag/v0.17.0、https://github.com/vllm-project/vllm/releases/latest

### 安全公告
- GHSA-hj4w-hm2g-p6w5（2025-04）：Mooncake 集成 RCE 漏洞，影响 >=0.6.5 且使用 Mooncake 的部署，已在 v0.8.5 修复
- 来源：https://github.com/vllm-project/vllm/security/advisories/GHSA-hj4w-hm2g-p6w5

### 优先阅读链接（精确 URL）
1. README 概览：https://github.com/vllm-project/vllm
2. 文档首页 / Getting Started：https://docs.vllm.ai/en/latest/getting_started/installation.html
3. Architecture 文档：https://docs.vllm.ai/en/latest/design/architecture.html
4. OpenAI 兼容接口文档：https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html
5. Release v0.17.0：https://github.com/vllm-project/vllm/releases/tag/v0.17.0
6. Release v0.18.0（最新）：https://github.com/vllm-project/vllm/releases/latest
7. 安全公告：https://github.com/vllm-project/vllm/security/advisories/GHSA-hj4w-hm2g-p6w5

## 三、vLLM-Omni 独立资料

- GitHub 仓库：https://github.com/vllm-project/vllm-omni
- 定位：全模态推理框架（文本+图像+音频+视频统一生成），与主 vLLM 是不同代码库
- 发布时间：2025-12 公告（CSDN/微博公开报道），项目本身为早期活跃状态
- 来源：https://github.com/vllm-project/vllm-omni（直接访问确认仓库存在）

## 四、vLLM-Ascend 独立资料

- GitHub 仓库：https://github.com/vllm-project/vllm-ascend
- 文档站：https://vllm-ascend.readthedocs.io/en/latest/
- 定位：华为昇腾 NPU 的 vLLM 插件，社区维护，非官方主项目
- 状态：独立 release 周期，与主 vLLM 版本号不同步
- 来源：https://github.com/vllm-project/vllm-ascend、https://vllm-ascend.readthedocs.io/en/latest/

Sources:
1. https://github.com/vllm-project/vllm — 主仓库
2. https://docs.vllm.ai/ — 官方文档
3. https://github.com/vllm-project/vllm/releases/latest — 最新 release（v0.18.0）
4. https://github.com/vllm-project/vllm/releases/tag/v0.17.0 — v0.17.0 release notes
5. https://www.vllm.ai/ — PagedAttention 官方介绍（历史 benchmark 来源）
6. https://github.com/vllm-project/vllm/security/advisories/GHSA-hj4w-hm2g-p6w5 — 安全公告
7. https://github.com/vllm-project/vllm-omni — vLLM-Omni 独立仓库
8. https://github.com/vllm-project/vllm-ascend — vLLM-Ascend 独立仓库
9. https://vllm-ascend.readthedocs.io/en/latest/ — vLLM-Ascend 文档

Risk of Staleness:
- release 版本号随时间变化，v0.18.0 为 2026-03-25 最新，pip install 默认版以实际安装时为准
- vLLM-Omni 和 vLLM-Ascend 为独立项目，进化速度快，文档更新可能滞后
- GHSA 安全公告描述基于 2025-04，Mooncake 用户需确认实际部署版本

Out of Scope Kept:
- 未写成完整章节
- 未做 vLLM vs SGLang 深度对比
- 未混入 Triton / SGLang 来源

Need Codex Review On:
- "14-24 倍吞吐量"历史数字是否可保留为背景引用，还是应完全删去
- vLLM-Omni 的全模态方向是否需要在 AI Infra 章节中单独占位，还是归于"多模态"大类
