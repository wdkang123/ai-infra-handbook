---
layout: home

hero:
  name: "AI Infra Handbook"
  text: "工程学习手册"
  tagline: "面向后端、平台和 AI 应用开发者。先跑通，再系统学习。学习项目，不是生产平台。"
  actions:
    - theme: brand
      text: 15 分钟跑通
      link: /quickstart/15-minute-demo
    - theme: alt
      text: 系统学习路线
      link: /00-overview/02-learning-route
    - theme: alt
      text: GitHub 仓库
      link: https://github.com/wdkang123/ai-infra-handbook
---

<section class="home-proof-cards">
  <div>
    <strong>跑得起来</strong>
    <p>用 make quickstart 跑通四层服务，并生成 evidence packet。</p>
  </div>
  <div>
    <strong>看得见证据</strong>
    <p>request id、events、metrics、report、manifest 都有固定入口。</p>
  </div>
  <div>
    <strong>学得出系统</strong>
    <p>四层项目边界清楚，适合从后端、平台或 AI 应用视角理解 AI Infra。</p>
  </div>
</section>

<section class="home-artifact-strip">
  <a href="/13-output-gallery/01-serving-gateway-evidence"><span>request id</span><strong>串起一次请求</strong></a>
  <a href="/13-output-gallery/01-serving-gateway-evidence"><span>events</span><strong>还原链路时间线</strong></a>
  <a href="/12-production-migration/07-prometheus-metrics-map"><span>metrics</span><strong>观察服务与平台信号</strong></a>
  <a href="/04-evaluation-observability/09-eval-regression-gate-example"><span>eval report</span><strong>形成发布建议</strong></a>
  <a href="/13-output-gallery/03-finetune-artifact-evidence"><span>manifest</span><strong>追溯训练资产</strong></a>
  <a href="/13-output-gallery/07-generated-evidence-packet"><span>evidence packet</span><strong>汇总复盘材料</strong></a>
</section>

<section class="home-audience">
  <div>
    <span class="home-kicker">适合谁</span>
    <ul>
      <li>想把 LLM API 使用升级成 AI Infra 系统理解的后端、平台和 AI 应用开发者。</li>
      <li>想边读边跑，能用命令、输出、request id 和 manifest 验证学习结果的人。</li>
      <li>准备把学习内容分享给同事、学习小组或 GitHub 读者的维护者。</li>
    </ul>
  </div>
  <div>
    <span class="home-kicker">不适合谁</span>
    <ul>
      <li>想直接拿来承载生产流量的人：当前是学习项目，不是生产平台。</li>
      <li>只想看模型榜单或 prompt 技巧，而不想理解服务、网关、评测和训练资产的人。</li>
      <li>完全不想运行命令或查看输出证据的人：这个站点的核心收获来自验证。</li>
    </ul>
  </div>
</section>

<section class="home-public-entry">
  <div class="home-section-head">
    <span class="eyebrow">Growth Path</span>
    <h2>先跑通，再学习，再贡献</h2>
    <p>首页只保留最重要的三步；更细的路线、发布、社区和迁移内容下沉到独立页面。</p>
  </div>
  <div class="launch-grid">
    <a class="launch-card primary" href="/quickstart/15-minute-demo">
      <span class="launch-kicker">15 min</span>
      <h3>跑通第一条端到端链路</h3>
      <p>clone、install、make quickstart、发请求、查 request id、生成 evidence packet。</p>
      <span class="launch-meta">可运行 / 可验证 / 可复盘</span>
    </a>
    <a class="launch-card" href="/landing/ai-infra-intro">
      <span class="launch-kicker">learn</span>
      <h3>按主题进入学习</h3>
      <p>从 AI Infra 入门、Gateway、Observability、Evaluation 到 Production Migration。</p>
      <span class="launch-meta">主题页 → 主线章节 → lab</span>
    </a>
    <a class="launch-card" href="/community/00-overview">
      <span class="launch-kicker">contribute</span>
      <h3>从学习者变成贡献者</h3>
      <p>选择 starter issue，按证据标准补文档、lab、案例或真实迁移设计。</p>
      <span class="launch-meta">issue → PR → release note</span>
    </a>
  </div>
</section>

<HomeSystemMap />

<section class="home-next-grid">
  <a href="/08-publication/15-starter-issues">
    <span>Starter Issues</span>
    <strong>20 个适合公开首发的任务种子</strong>
  </a>
  <a href="/08-publication/16-v0-1-release-notes">
    <span>v0.1.0 Release</span>
    <strong>发布说明、验证命令和学习边界</strong>
  </a>
  <a href="/12-production-migration/05-vllm-adapter-design">
    <span>Real Backend</span>
    <strong>vLLM adapter、OTel、Prometheus、SGLang 迁移锚点</strong>
  </a>
  <a href="/11-case-studies/06-failure-case-playbook">
    <span>Failure Cases</span>
    <strong>timeout、fallback、eval block、lineage mismatch</strong>
  </a>
</section>
