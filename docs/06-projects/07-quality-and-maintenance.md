# 质量与维护入口

这个仓库的质量目标不是把学习项目伪装成生产系统，而是保证每一步学习、改动和联调都有清晰的验收入口。

## 本地检查

从仓库根目录执行：

```bash
PYTHON=.venv/bin/python make infra-check
```

这会依次运行：

- Python lint
- 四个项目的单元测试
- 文档质量检查，包括 Markdown 内链、heading 锚点、H1 结构、VitePress nav/sidebar 路由、首页配置与 Vue 组件链接和首页统计
- VitePress 文档构建和非 localhost 链接检查

如果你想跑完整闭环，再执行：

```bash
PYTHON=.venv/bin/python make infra-smoke
```

这会临时启动 inference-service 和 ai-gateway，并验证 gateway、inference、eval、finetune 四段是否还能连起来。

## 格式化与修复

```bash
PYTHON=.venv/bin/python make infra-format
```

这个命令只处理 Python 代码和脚本，不会改动文档正文。

## 什么时候必须跑 smoke

只改文档时，`infra-check` 通常足够。

改到以下内容时，建议再跑 `infra-smoke`：

- `projects/inference-service/`
- `projects/ai-gateway/`
- `projects/eval-module/`
- `projects/finetune-demo/`
- 根级 `Makefile`
- `scripts/integration_smoke_test.sh`

## 当前质量边界

现在这些检查能保证：

- 项目入口不会因为相对 Python 路径失效
- 文档站不会悄悄吞掉非 localhost 断链
- 新增文档页不会缺少顶层 H1 或出现多个 H1
- VitePress 顶部导航和 sidebar 不会悄悄指向不存在的内部页面
- 首页 frontmatter 入口、Vue 静态链接和数据驱动链接不会悄悄失效
- Markdown heading 锚点跳转不会在页面增长后漂移
- gateway/inference/eval/finetune 的最小闭环可重复运行
- inference adapter 的上游失败会稳定映射为结构化错误
- inference streaming 失败会以结构化 SSE error 结束
- gateway 普通请求和首 chunk 前 streaming 请求支持 fallback
- gateway streaming 全候选失败或中途失败会以结构化 SSE error 结束
- gateway cache 覆盖 TTL 过期和 token 隔离
- eval compare 可以用最小差异阈值避免噪声判定，并拒绝不同 task 混比
- 训练数据、训练产物与导出产物具备基本结构校验

它们还不能保证：

- 真实模型推理质量
- 真实 GPU 训练行为
- 生产级安全、追踪、背压和并发可靠性

这些会放在后续从学习型脚手架走向真实系统的阶段里推进。
