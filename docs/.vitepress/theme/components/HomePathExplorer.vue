<script setup lang="ts">
import { computed, ref } from "vue";

type PathKey = "serving" | "platform" | "evaluation" | "training" | "sharing";

const active = ref<PathKey>("serving");

const paths: Record<
  PathKey,
  {
    label: string;
    title: string;
    summary: string;
    steps: { text: string; href: string }[];
  }
> = {
  serving: {
    label: "推理服务",
    title: "先理解“请求为什么会变成结果”",
    summary:
      "适合想把 prefill、decode、streaming、metrics 和执行层边界先看明白的人。",
    steps: [
      { text: "模型、Token、Context", href: "/01-llm-fundamentals/01-model-token-context" },
      { text: "从请求到首个 Token", href: "/01-llm-fundamentals/04-from-request-to-first-token" },
      { text: "vLLM", href: "/02-inference-serving/04-vllm" },
      { text: "Streaming、Batching、Metrics", href: "/02-inference-serving/09-streaming-batching-metrics" },
      { text: "inference-service", href: "/06-projects/01-inference-service" },
      { text: "Serving 与 Gateway 输出证据", href: "/13-output-gallery/01-serving-gateway-evidence" },
    ],
  },
  platform: {
    label: "平台层",
    title: "先理解“为什么还要多一层 gateway”",
    summary:
      "适合想先建立入口治理、模型名映射、错误路径和平台边界的人。",
    steps: [
      { text: "鉴权、路由、限流", href: "/03-ai-gateway-platform/01-auth-routing-rate-limit" },
      { text: "健康检查、Metrics、Request ID", href: "/03-ai-gateway-platform/02-health-metrics-request-id" },
      { text: "平台层与模型服务层边界", href: "/03-ai-gateway-platform/05-platform-vs-model-service" },
      { text: "外部模型名与内部目标映射", href: "/03-ai-gateway-platform/06-model-name-to-target-mapping" },
      { text: "ai-gateway", href: "/06-projects/02-ai-gateway" },
      { text: "失败症状到证据地图", href: "/13-output-gallery/05-failure-evidence-map" },
    ],
  },
  evaluation: {
    label: "评测观测",
    title: "先理解“结果怎么变成判断”",
    summary:
      "适合想先搞懂 run、compare、history、benchmark 和发布判断的人。",
    steps: [
      { text: "Run、Compare、History", href: "/04-evaluation-observability/01-run-compare-history" },
      { text: "Tracing、Metrics、Logs", href: "/04-evaluation-observability/03-observability-traces-metrics-logs" },
      { text: "从 Run 到发布决策", href: "/04-evaluation-observability/07-from-run-to-release-decision" },
      { text: "Benchmark 与生产质量不是一回事", href: "/04-evaluation-observability/08-benchmark-vs-production-quality" },
      { text: "eval-module", href: "/06-projects/03-eval-module" },
      { text: "Eval 报告证据", href: "/13-output-gallery/02-eval-report-evidence" },
    ],
  },
  training: {
    label: "训练微调",
    title: "先理解“训练为什么不只是一条 train 命令”",
    summary:
      "适合想先建立 run、checkpoint、export、history 和训练目标直觉的人。",
    steps: [
      { text: "LoRA、QLoRA、PEFT", href: "/05-finetuning-training/01-lora-qlora-peft" },
      { text: "训练产物、Checkpoint、Export", href: "/05-finetuning-training/02-run-artifacts-export" },
      { text: "什么时候该微调", href: "/05-finetuning-training/07-when-to-finetune" },
      { text: "从 Demo Training 到真实训练系统", href: "/05-finetuning-training/08-from-demo-training-to-real-training-system" },
      { text: "finetune-demo", href: "/06-projects/04-finetune-demo" },
      { text: "Finetune 产物证据", href: "/13-output-gallery/03-finetune-artifact-evidence" },
    ],
  },
  sharing: {
    label: "公开分享",
    title: "先理解“怎么让别人也能跟着学”",
    summary:
      "适合准备发到 GitHub、带学习小组、收集反馈或把项目做成公开课程的人。",
    steps: [
      { text: "面向分享的学习方式", href: "/00-overview/11-public-learning-guide" },
      { text: "公开发布总览", href: "/08-publication/00-overview" },
      { text: "共学与公开分享套件", href: "/14-workshop-kit/00-overview" },
      { text: "学习者工作簿", href: "/14-workshop-kit/02-learner-workbook" },
      { text: "复盘与评审模板", href: "/14-workshop-kit/04-review-templates" },
      { text: "GitHub 发布计划", href: "/14-workshop-kit/06-github-release-plan" },
    ],
  },
};

const current = computed(() => paths[active.value]);
</script>

<template>
  <section class="path-explorer">
    <div class="home-section-head">
      <span class="eyebrow">Choose Your Path</span>
      <h2>按目标切换学习路线</h2>
      <p>不用每次都从头顺读。如果你已经知道自己更想学什么，可以直接切过去。</p>
    </div>

    <div class="path-tabs" role="tablist" aria-label="learning tracks">
      <button
        v-for="(path, key) in paths"
        :key="key"
        class="path-tab"
        :class="{ active: active === key }"
        type="button"
        @click="active = key as PathKey"
      >
        {{ path.label }}
      </button>
    </div>

    <div class="path-panel">
      <div class="path-copy">
        <span class="panel-kicker">{{ current.label }}</span>
        <h3>{{ current.title }}</h3>
        <p>{{ current.summary }}</p>
      </div>
      <ol class="path-steps">
        <li v-for="step in current.steps" :key="step.href">
          <a :href="step.href">{{ step.text }}</a>
        </li>
      </ol>
    </div>
  </section>
</template>
