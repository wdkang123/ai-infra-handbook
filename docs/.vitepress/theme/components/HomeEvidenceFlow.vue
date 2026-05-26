<template>
  <section class="evidence-flow">
    <div class="home-section-head">
      <span class="eyebrow">Evidence Loop</span>
      <h2>从课程地图到运行证据，形成可分享闭环</h2>
      <p>首页现在直接给出维护和公开演示最常用的九步：先确认学习站结构，再整理课程目录，最后把运行结果变成可复盘、可带练、可测评、可开 issue 的材料。</p>
    </div>

    <div class="evidence-steps" aria-label="learning site evidence loop">
      <a class="evidence-step" href="/09-reference/08-learning-inventory">
        <span class="step-index">01</span>
        <h3>盘点课程地图</h3>
        <p>用 <code>make docs-inventory</code> 生成章节、页面、课程主线和维护信号。</p>
        <span class="step-meta">learning_inventory.json / .md</span>
      </a>
      <a class="evidence-step" href="/09-reference/10-course-catalog">
        <span class="step-index">02</span>
        <h3>生成课程目录</h3>
        <p>用 <code>make course-catalog</code> 把课程主线整理成可带练模块。</p>
        <span class="step-meta">course_catalog.json / .md</span>
      </a>
      <a class="evidence-step" href="/09-reference/07-validation-matrix">
        <span class="step-index">03</span>
        <h3>选择验证层级</h3>
        <p>根据改动影响面选择 docs-quality、infra-check、smoke 或证据包生成。</p>
        <span class="step-meta">按改动类型选择命令</span>
      </a>
      <a class="evidence-step" href="/13-output-gallery/07-generated-evidence-packet">
        <span class="step-index">04</span>
        <h3>汇总运行证据</h3>
        <p>用 <code>make infra-evidence</code> 把 serving、eval 和 finetune 产物收成证据包。</p>
        <span class="step-meta">evidence_packet.json / .md</span>
      </a>
      <a class="evidence-step" href="/09-reference/09-release-brief">
        <span class="step-index">05</span>
        <h3>生成发布摘要</h3>
        <p>用 <code>make release-brief</code> 把课程地图和运行证据合成公开复盘材料。</p>
        <span class="step-meta">release_brief.json / .md</span>
      </a>
      <a class="evidence-step" href="/14-workshop-kit/07-generated-workshop-packet">
        <span class="step-index">06</span>
        <h3>生成共学包</h3>
        <p>用 <code>make workshop-packet</code> 把课程目录和发布摘要整理成带练材料。</p>
        <span class="step-meta">workshop_packet.json / .md</span>
      </a>
      <a class="evidence-step" href="/10-assessments/06-generated-assessment-pack">
        <span class="step-index">07</span>
        <h3>生成测评包</h3>
        <p>用 <code>make assessment-pack</code> 把课程模块整理成题目、证据要求和评分标准。</p>
        <span class="step-meta">assessment_pack.json / .md</span>
      </a>
      <a class="evidence-step" href="/08-publication/05-generated-roadmap-pack">
        <span class="step-index">08</span>
        <h3>生成路线图包</h3>
        <p>用 <code>make roadmap-pack</code> 把发布摘要和测评弱点整理成 GitHub issue 种子。</p>
        <span class="step-meta">roadmap_pack.json / .md</span>
      </a>
      <a class="evidence-step" href="/08-publication/13-generated-launch-pack">
        <span class="step-index">09</span>
        <h3>生成首发运营包</h3>
        <p>用 <code>make launch-pack</code> 统一 release notes、starter issues 和发布后检查表。</p>
        <span class="step-meta">launch_pack.json / .md</span>
      </a>
    </div>
  </section>
</template>
