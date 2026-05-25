Task ID: T134
Task Title: 编写 vLLM 章节模板化初稿
Owner: MINIMAX
Status: REVIEW_PENDING

Input Summary:
基于 T111 资料包（vLLM 主项目 / vLLM-Omni / vLLM-Ascend）和 base.md 章节模板，输出 vLLM 章节初稿。

Result:

# vLLM

## 1. 这是什么

vLLM 是一个开源的 LLM 推理与服务引擎，核心目标是在 NVIDIA GPU 上实现高吞吐、低延迟的批量推理。它通过 PagedAttention 算法管理 KV Cache，通过 Continuous Batching 最大化 GPU 利用率。

vLLM 与其姐妹项目的关系：
- **vLLM 主项目**（`vllm-project/vllm`）：GPU LLM 推理引擎，当前主力实现
- **vLLM-Omni**（`vllm-project/vllm-omni`）：独立子项目，专注于全模态模型（文本/图像/音频/视频统一生成），非主仓库一部分
- **vLLM-Ascend**（`vllm-project/vllm-ascend`）：社区维护的华为昇腾 NPU 插件，非主仓库一部分

## 2. 为什么重要

在 AI Infra 推理服务栈中，vLLM 解决了 LLM Serving 的两个核心瓶颈：

1. **显存效率**：PagedAttention 将 KV Cache 分块存储，避免传统连续存储的显存碎片，官方称显存利用率提升可达 4 倍
2. **GPU 利用率**：Continuous Batching 以单次 token 生成为调度粒度，避免静态 batching 中长请求阻塞导致的 GPU 空闲

vLLM 是理解 LLM Serving 原理的经典范本，是学习 PagedAttention 和 Continuous Batching 实际落地的首选框架。

## 3. 核心原理

### PagedAttention
将 KV Cache 分块（block）存储在非连续显存中，类似 OS 虚拟内存的分页思想。每个 block 存储固定数量的 KV entries，block 之间通过链表组织。好处：1）避免显存碎片；2）支持 prefix caching；3）实现 GPU-less Render Serving。

来源：https://docs.vllm.ai/en/latest/design/architecture.html

### Continuous Batching
以 iteration（单次 token 生成）为调度粒度，在每个 step 动态将已完成推理的请求移出批次、插入新到达请求。相比静态 batching，解决"短请求等待长请求"问题。vLLM 0.2+ 实现。

来源：https://docs.vllm.ai/

### OpenAI 兼容 API
vLLM 提供 REST 和 gRPC 双接口，协议兼容 OpenAI API 格式。生产环境可以直接将 OpenAI SDK 的 base_url 替换为 vLLM 地址。

来源：https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html

## 4. 常见方案 / 组件

- **Engine**：离线推理入口，`vllm.LLM` 类负责模型加载和推理
- **AsyncLLMEngine**：在线服务入口，支持高并发请求处理
- **PagedAttention Block Manager**：管理 KV Cache 块的分配和释放
- **Scheduler**：实现 Continuous Batching 的调度逻辑
- **Worker**：实际执行推理的 PyTorch 模型实例

来源：https://docs.vllm.ai/en/latest/design/architecture.html

## 5. 关键指标

- **Throughput（吞吐）**：tokens/second 或 requests/second，vLLM 的核心优势指标
- **Latency（P50/P99）**：TTFT 和 E2E latency，通常在 benchmark 报告中一起给出
- **显存占用（GPU Memory）**：KV Cache 块数量 × block size，由 `--gpu-memory-utilization` 控制
- **Context Length**：最大支持上下文长度，由模型决定，vLLM 通过 PagedAttention 支持长上下文

历史性能数据（早期 benchmark，非当前通用能力）：
- 早期 blog 声称"比 HuggingFace Transformers 高 14-24 倍吞吐量"——来自特定硬件和特定模型，需谨慎引用

来源：https://www.vllm.ai/（官方 blog）

## 6. 常见误区

1. **"vLLM 比 SGLang 快"**：两者吞吐量在相同硬件和模型下各有高低，vLLM 在简单场景下易用性更好，SGLang 在复杂 Agent 场景调度更灵活
2. **"PagedAttention 等于前缀缓存"**：PagedAttention 是 KV Cache 的分页管理机制，前缀缓存是其在共享前缀场景的具体应用
3. **"vLLM-Omni 是 vLLM 的一部分"**：vLLM-Omni 是独立项目，有独立 release 周期，不应与 vLLM 主仓库混淆
4. **"vLLM 不支持多模态"**：主项目主要面向纯文本 LLM；vLLM-Omni 专门处理多模态

## 7. 与项目关系

在 AI Infra 学习路径中，vLLM 是理解 LLM 推理引擎的第一站：

- 先掌握 vLLM 的 PagedAttention + Continuous Batching，理解 LLM Serving 的核心问题（显存效率 + GPU 利用率）
- 再对比 SGLang（RadixAttention vs PagedAttention）深化对调度差异的理解
- vLLM 的 OpenAI 兼容接口是 AI Gateway 层实现的关键依赖

## 8. 最小实践任务

**目标**：在单卡 GPU 上用 vLLM 启动一个 Qwen 模型的 OpenAI 兼容 API 服务，并验证流式输出。

```bash
# 安装（需要 CUDA 12.1+）
pip install vllm

# 启动服务
python -m vllm.entrypoints.openai.api_server \
    --model Qwen/Qwen2.5-7B-Instruct \
    --port 8000 \
    --gpu-memory-utilization 0.9

# 调用
curl http://localhost:8000/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{"model": "Qwen/Qwen2.5-7B-Instruct", "messages": [{"role": "user", "content": "Hello"}]}'
```

来源：https://docs.vllm.ai/en/latest/getting_started/installation.html

## 9. 输出物

- vLLM API 服务运行中（端口 8000）
- 可通过 `curl` 或 OpenAI SDK 调用验证
- 服务日志中的 throughput 和 latency 数字可记录为基础指标

## 10. 延伸阅读

1. https://docs.vllm.ai/ — 官方文档
2. https://github.com/vllm-project/vllm — 主仓库
3. https://docs.vllm.ai/en/latest/design/architecture.html — 架构设计文档
4. https://www.vllm.ai/ — PagedAttention 官方介绍
5. https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — API 文档
6. https://github.com/vllm-project/vllm/releases/latest — 最新 release（v0.18.0）

Sources:
1. https://docs.vllm.ai/ — vLLM 官方文档
2. https://github.com/vllm-project/vllm — 主仓库
3. https://docs.vllm.ai/en/latest/design/architecture.html — 架构文档
4. https://www.vllm.ai/ — PagedAttention 官方 blog
5. https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html — API 文档
6. https://github.com/vllm-project/vllm/releases/latest — 最新 release

Risk of Staleness:
- vLLM 版本更新快，最小实践中的 pip install 版本以实际安装时为准
- API 端口和参数在 major 版本升级时可能变化
- vLLM-Omni 和 vLLM-Ascend 为独立项目，上述最小实践不覆盖

Out of Scope Kept:
- 未写成完整推理服务手册
- 未做与 SGLang 的最终优劣对比
- 未写 vLLM-Omni 的实践

Need Codex Review On:
- "显存利用率提升 4 倍"的具体数字是否可引用，还是改为更保守的表述
- vLLM-Omni 和 vLLM-Ascend 是否需要在章节中有独立小节
