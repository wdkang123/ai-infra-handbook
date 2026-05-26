<script setup lang="ts">
const rows = [
  {
    module: "系统地图",
    question: "这四个项目为什么要分层？",
    artifact: "一张四层系统图",
    validation: "系统地图自测",
    href: "/10-assessments/01-system-map-check",
  },
  {
    module: "推理服务",
    question: "请求如何变成 token 输出？",
    artifact: "普通响应、streaming、metrics",
    validation: "Serving Lab",
    href: "/07-hands-on-labs/01-serving-observability-lab",
  },
  {
    module: "平台治理",
    question: "入口层如何处理鉴权、路由和失败？",
    artifact: "request timeline、failure summary",
    validation: "Gateway Lab",
    href: "/07-hands-on-labs/02-gateway-resilience-lab",
  },
  {
    module: "评测闭环",
    question: "结果如何变成发布判断？",
    artifact: "run bundle、comparison、sample analysis",
    validation: "Eval Lab",
    href: "/07-hands-on-labs/03-eval-release-gate-lab",
  },
  {
    module: "训练资产",
    question: "训练为什么要留下可复现资产？",
    artifact: "manifest、checkpoint index、export lineage",
    validation: "Finetune Lab",
    href: "/07-hands-on-labs/04-finetune-reproducibility-lab",
  },
  {
    module: "证据复盘",
    question: "跑完命令后应该看哪些输出？",
    artifact: "端到端复盘证据包",
    validation: "示例输出与证据库",
    href: "/13-output-gallery/00-overview",
  },
  {
    module: "共学分享",
    question: "如何把个人学习变成可复用的公开材料？",
    artifact: "工作簿、议程、评审模板、发布计划",
    validation: "共学与公开分享套件",
    href: "/14-workshop-kit/00-overview",
  },
];
</script>

<template>
  <section class="course-matrix">
    <div class="home-section-head">
      <span class="eyebrow">Learning Outcomes</span>
      <h2>每一阶段都有问题、产物和验收</h2>
      <p>这套站点现在更适合作为公开学习项目：读者不只知道要读哪一页，也知道每一阶段要交付什么。</p>
    </div>

    <div class="matrix-table" aria-label="learning outcome matrix">
      <div class="matrix-head">模块</div>
      <div class="matrix-head">核心问题</div>
      <div class="matrix-head">学习产物</div>
      <div class="matrix-head">验收入口</div>

      <template v-for="row in rows" :key="row.module">
        <div class="matrix-cell strong">{{ row.module }}</div>
        <div class="matrix-cell">{{ row.question }}</div>
        <div class="matrix-cell">{{ row.artifact }}</div>
        <a class="matrix-cell matrix-link" :href="row.href">{{ row.validation }}</a>
      </template>
    </div>

    <div class="matrix-mobile-list" aria-label="learning outcome cards">
      <a v-for="row in rows" :key="row.module" class="matrix-mobile-card" :href="row.href">
        <span class="matrix-mobile-kicker">{{ row.module }}</span>
        <strong>{{ row.question }}</strong>
        <p>{{ row.artifact }}</p>
        <span class="matrix-mobile-meta">{{ row.validation }}</span>
      </a>
    </div>

    <div class="matrix-actions">
      <a href="/00-overview/14-project-maturity-map">查看当前项目成熟度</a>
      <a href="/00-overview/15-two-week-learning-plan">按两周计划学习</a>
      <a href="/11-case-studies/00-overview">阅读案例复盘</a>
      <a href="/13-output-gallery/00-overview">查看示例输出</a>
      <a href="/09-reference/08-learning-inventory">生成学习站清单</a>
      <a href="/09-reference/10-course-catalog">生成课程目录</a>
      <a href="/14-workshop-kit/07-generated-workshop-packet">生成共学包</a>
      <a href="/10-assessments/06-generated-assessment-pack">生成测评包</a>
      <a href="/08-publication/05-generated-roadmap-pack">生成路线图包</a>
      <a href="/14-workshop-kit/00-overview">打开共学套件</a>
      <a href="/12-production-migration/00-overview">查看生产迁移路线</a>
      <a href="/07-hands-on-labs/06-public-release-readiness-lab">做发布前验收 Lab</a>
    </div>
  </section>
</template>
