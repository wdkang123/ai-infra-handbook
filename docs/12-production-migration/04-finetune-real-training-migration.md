# Finetune 真实训练迁移

这一页说明 `finetune-demo` 如何从 mock train / export，迁移到更真实的 LoRA/QLoRA 训练流程。

当前 finetune-demo 的价值在于资产结构：

- run manifest
- artifacts manifest
- dataset summary
- dataset registry
- checkpoint index
- export manifest
- run/export history

真实训练迁移时，最该保住这些结构。

## 当前边界

迁移时应该保留：

- `train`
- `export`
- `list-runs`
- `list-datasets`
- `diff-datasets`
- `list-exports`
- `run_manifest.json`
- `artifacts_manifest.json`
- `checkpoints/checkpoint_index.json`
- `export_manifest.json`
- `dataset_registry.jsonl`

这些文件和命令让训练过程可以被解释。

## 迁移顺序

### 第一步：保留数据校验和 dataset summary

真实 trainer 接入前，先确认数据层稳：

- JSONL schema 校验
- role 分布
- message count
- dataset sha256
- dataset version
- dataset registry entry

如果数据不可解释，真实训练只会更难复盘。

### 第二步：替换 trainer 内部执行

可以逐步把 mock trainer 替换成：

- PEFT LoRA trainer
- QLoRA trainer
- Unsloth 风格训练入口
- 自定义 SFT trainer

但 CLI 和产物目录不要一开始就大改。

### 第三步：扩展 checkpoint 策略

当前只有一个 mock checkpoint。真实训练需要：

- 多 checkpoint
- latest checkpoint
- best checkpoint
- resume checkpoint
- adapter hash
- optimizer / scheduler state 指纹

`checkpoint_index.json` 应该成为 resume 和 export 的入口，而不是目录列表的附属品。

### 第四步：让 export 进入发布链路

export 不只是复制文件。它应该回答：

- 源 checkpoint 是哪个
- dataset 是哪个
- adapter hash 是什么
- export 是否成功
- 后续 eval 如何引用它

这也是 [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage) 的核心。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 数据漂移 | 两次训练看似相同但数据不同 | dataset sha256 / registry diff |
| checkpoint 混乱 | 不知道导出自哪个 checkpoint | checkpoint index |
| 训练不可复现 | 只剩日志和权重 | run manifest / training args / artifact hashes |
| export 不可追溯 | adapter 无法回到 run | export manifest / export history |
| eval 无来源 | 评测不知道模型来自哪个训练 | export lineage 写入评测说明 |

## 验收清单

- [ ] 数据校验失败路径仍然有测试
- [ ] dataset summary 仍然包含 role stats 和 sha256
- [ ] run manifest 能解释训练参数和产物
- [ ] checkpoint index 能列出 checkpoint、文件和 hash
- [ ] export manifest 能追溯 source checkpoint
- [ ] run/export index 能聚合历史
- [ ] `finetune-test` 通过
- [ ] `infra-smoke` 通过

## 应该更新的文档

- [finetune-demo](/06-projects/04-finetune-demo)
- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [训练产物复现案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [产物与文件索引](/09-reference/03-artifacts-and-files)

## 一句话结论

Finetune 迁移的关键，不是只把训练跑得更真，而是让真实训练仍然留下可解释、可校验、可追溯、可进入 eval 的资产链。
