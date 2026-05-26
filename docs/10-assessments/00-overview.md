# 学习自测总览

这一组页面不是为了考试，而是为了回答一个更实用的问题：

> 我是不是已经能把这套 AI Infra 小系统讲清楚、跑清楚、改清楚？

如果说 [课程大纲](/00-overview/12-course-syllabus) 是学习路线，[深度实战](/07-hands-on-labs/00-overview) 是动手任务，[示例输出与证据库](/13-output-gallery/00-overview) 是证据解释，那么学习自测就是阶段验收。它适合在你准备分享、写文章、录视频、做 GitHub 项目展示之前使用。

如果你想把当前 7 个课程模块自动整理成题目、证据要求和评分标准，可以先生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)。
如果你想把测评薄弱点继续转成 GitHub issue，再看 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)。
如果你准备首发 release 或首批 issues，再看 [自动生成首发运营包](/08-publication/13-generated-launch-pack)。

## 怎么使用

建议每学完一个大模块就做一次自测：

1. 先不看参考答案，独立写出你的回答
2. 能运行命令的题目，尽量真的跑一遍
3. 能指向代码的题目，写出具体文件和函数
4. 能指向输出证据的题目，写出 header、event、JSON 或 manifest
5. 对照参考答案时，不要只看关键词，要看推理过程
6. 把答不稳的问题回链到对应文档或 lab

如果你是带别人学习，可以把这些题目当成讨论提纲。  
如果你是自己学习，可以把它们当成复盘清单。

## 自测分级

每个主题都可以用同一套标准判断：

| 等级 | 表现 |
| --- | --- |
| Level 1 | 能复述名词，但解释不出系统边界 |
| Level 2 | 能跑通命令，也知道主要文件在哪里 |
| Level 3 | 能解释正常路径和失败路径，并能指出测试覆盖和输出证据 |
| Level 4 | 能提出一个合理改进方案，并说明风险和验证方式 |

公开分享时，建议至少达到 Level 3。  
如果你能稳定达到 Level 4，这套项目就不只是“能跑”，而是开始变成你自己的工程作品。

## 自测目录

- [系统地图自测](/10-assessments/01-system-map-check)
- [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)
- [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)
- [Capstone 答辩稿](/10-assessments/04-capstone-defense)
- [参考答案与讲解](/10-assessments/05-answer-key)
- [自动生成测评包](/10-assessments/06-generated-assessment-pack)
- [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
- [自动生成首发运营包](/08-publication/13-generated-launch-pack)

## 推荐节奏

如果你正在从头学：

1. 学完模块 0 和模块 1 后，做 [系统地图自测](/10-assessments/01-system-map-check)
2. 学完推理服务和平台治理后，做 [Serving 与 Gateway 自测](/10-assessments/02-serving-gateway-quiz)
3. 学完评测和训练后，做 [Eval 与 Finetune 自测](/10-assessments/03-eval-finetune-quiz)
4. 对照 [示例输出与证据库](/13-output-gallery/00-overview) 整理一份证据包
5. 完成所有 lab 后，做 [Capstone 答辩稿](/10-assessments/04-capstone-defense)
6. 准备带练或公开展示前，生成 [自动生成测评包](/10-assessments/06-generated-assessment-pack)
7. 准备开放贡献前，生成 [自动生成路线图包](/08-publication/05-generated-roadmap-pack)
8. 准备创建 release 或首批 issue 前，生成 [自动生成首发运营包](/08-publication/13-generated-launch-pack)

如果你已经学过一遍，直接从 Capstone 开始也可以。  
答辩过程中卡住的地方，就是你下一轮最值得回补的地方。
