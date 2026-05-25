<template>
  <section class="home-system-map">
    <div class="home-section-head">
      <span class="eyebrow">System Map</span>
      <h2>这不是四个孤立 demo，而是一张最小 AI Infra 系统图</h2>
      <p>你后面无论是读文档、改代码还是让别的大模型继续细化，都可以先问自己：我现在动的是哪一层。</p>
    </div>

    <div class="system-flow">
      <div class="system-node">
        <span class="node-index">01</span>
        <h3>inference-service</h3>
        <p>执行层。负责 health、metrics、chat completion、streaming 和最小 request lifecycle。</p>
        <a href="/06-projects/01-inference-service">查看项目页</a>
      </div>
      <div class="system-arrow">→</div>
      <div class="system-node">
        <span class="node-index">02</span>
        <h3>ai-gateway</h3>
        <p>治理层。负责鉴权、模型名映射、代理、限流、upstream health 和 request id。</p>
        <a href="/06-projects/02-ai-gateway">查看项目页</a>
      </div>
      <div class="system-arrow">→</div>
      <div class="system-node">
        <span class="node-index">03</span>
        <h3>eval-module</h3>
        <p>质量层。负责 run、compare、bundle、history，把结果变成可判断对象。</p>
        <a href="/06-projects/03-eval-module">查看项目页</a>
      </div>
      <div class="system-arrow">→</div>
      <div class="system-node">
        <span class="node-index">04</span>
        <h3>finetune-demo</h3>
        <p>训练层。负责 train、checkpoint、export、manifest 和训练资产沉淀。</p>
        <a href="/06-projects/04-finetune-demo">查看项目页</a>
      </div>
    </div>
  </section>
</template>
