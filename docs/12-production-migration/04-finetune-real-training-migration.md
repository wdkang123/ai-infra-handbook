# Finetune 真实训练迁移

这一页说明 `finetune-demo` 如何从 mock train / export，迁移到更真实的 LoRA/QLoRA 训练流程。

当前 finetune-demo 的价值不在于“真的训练了一个可用模型”，而在于它已经把训练资产结构摆出来了：

- run manifest
- artifacts manifest
- dataset summary
- dataset registry
- checkpoint index
- export manifest
- run history
- export history

真实训练迁移时，最该保住这些结构。

## 迁移时最应该保留什么

优先保留这些命令：

```text
train
export
list-runs
list-datasets
diff-datasets
list-exports
```

优先保留这些产物：

```text
run_manifest.json
artifacts_manifest.json
data/dataset_summary.json
data/dataset_registry_entry.json
checkpoints/checkpoint_index.json
export_manifest.json
dataset_registry.jsonl
run_history.jsonl
export_history.jsonl
```

这些文件和命令让训练过程可以被解释。
真实 trainer 可以替换，但资产链路不应该消失。

## 第一阶段：先稳住数据层

真实 trainer 接入前，先确认数据层稳定。

至少保留：

- JSONL schema 校验
- role 分布
- record count
- message count
- dataset sha256
- dataset version
- dataset registry entry

如果数据不可解释，真实训练只会更难复盘。

数据层应该能回答：

- 这次训练用了哪份数据？
- 数据格式是否有效？
- 数据内容有没有变化？
- role 分布是否异常？
- 和上次训练相比，数据版本是否一致？

这一步比先接 GPU 更重要。

## 第二阶段：替换 Trainer 内部执行

可以逐步把 mock trainer 替换成：

- PEFT LoRA trainer
- QLoRA trainer
- Unsloth 风格训练入口
- Transformers Trainer / TRL SFTTrainer
- 自定义 SFT trainer
- 后续偏好优化 trainer

但 CLI 和产物目录不要一开始就大改。

理想迁移方式是：

```text
same train CLI
  -> real trainer backend
  -> same run manifest/artifacts manifest
  -> richer metrics/checkpoints
```

这样读者不需要重新学习整条资产链。

## 第三阶段：扩展训练配置记录

真实训练需要记录更多配置。

建议逐步加入：

- base model
- tokenizer version
- chat template
- LoRA rank / alpha / dropout
- QLoRA quantization settings
- batch size
- gradient accumulation
- learning rate schedule
- seed
- max sequence length
- precision
- optimizer
- dataset split
- library versions

这些配置应该进入：

- `training_args.json`
- `trainer_state.json`
- `run_manifest.json`
- `artifacts_manifest.json`

不要只存在于终端命令或临时日志里。

## 第四阶段：扩展 Checkpoint 策略

当前只有一个 mock checkpoint。
真实训练需要处理：

- 多 checkpoint
- latest checkpoint
- best checkpoint
- resume checkpoint
- adapter hash
- optimizer state
- scheduler state
- trainer state
- checkpoint metrics

`checkpoint_index.json` 应该成为 resume 和 export 的入口，而不是目录列表的附属品。

一个更真实的 checkpoint index 应该能回答：

- 有哪些 checkpoint？
- 哪个是 latest？
- 哪个是 best？
- 每个 checkpoint 的 adapter hash 是什么？
- 哪些文件可用于 resume？
- 哪个 checkpoint 已经 export？

## 第五阶段：让 Export 进入发布链路

export 不只是复制文件。
它应该回答：

- source checkpoint 是哪个？
- base model 是什么？
- dataset id/version 是什么？
- adapter hash 是什么？
- export 是否成功？
- export 用了多久？
- 后续 eval 如何引用它？

导出产物应该能进入：

```text
export -> eval run -> compare -> release decision
```

否则微调产物只是目录里的文件，不是可发布资产。

## 第六阶段：接 Eval 回归

真实训练迁移后，必须接 eval。

最小闭环是：

1. 训练生成 run。
2. export 生成 adapter。
3. eval-module 对 candidate 做 run。
4. compare baseline 和 candidate。
5. release recommendation 给出 promote/review/block。
6. 如果退化，能从 eval 回溯到 export、checkpoint、dataset。

没有 eval，训练迁移只能证明“能跑”，不能证明“值得保留”。

## 当前仓库相关文件

重点看：

```text
projects/finetune-demo/src/finetune_demo/main.py
projects/finetune-demo/src/finetune_demo/config.py
projects/finetune-demo/src/finetune_demo/trainer/lora_trainer.py
projects/finetune-demo/src/finetune_demo/dataset_registry.py
projects/finetune-demo/src/finetune_demo/run_history.py
projects/finetune-demo/src/finetune_demo/export/adapter_exporter.py
projects/finetune-demo/tests/test_trainer.py
```

迁移时常改：

- `lora_trainer.py`：替换真实训练执行。
- `config.py`：扩展训练参数。
- `dataset_registry.py`：增强数据资产登记。
- `adapter_exporter.py`：增强 export lineage。
- tests：保护数据校验、manifest、history、export。

## 风险清单

| 风险 | 表现 | 防线 |
| --- | --- | --- |
| 数据漂移 | 两次训练看似相同但数据不同 | dataset sha256 / registry diff |
| checkpoint 混乱 | 不知道导出自哪个 checkpoint | checkpoint index |
| 训练不可复现 | 只剩日志和权重 | run manifest / training args / artifact hashes |
| export 不可追溯 | adapter 无法回到 run | export manifest / export history |
| eval 无来源 | 评测不知道模型来自哪个训练 | export lineage 写入评测说明 |
| loss 误导 | loss 下降但任务退化 | eval compare / release gate |
| 配置丢失 | 终端命令忘记保存 | training args / config snapshot |

## 验收清单

Finetune 迁移至少确认：

- [ ] 数据校验失败路径仍然有测试
- [ ] dataset summary 仍然包含 role stats 和 sha256
- [ ] dataset registry 能记录 dataset id/version
- [ ] run manifest 能解释训练参数和产物
- [ ] artifacts manifest 能列出文件和 hash
- [ ] checkpoint index 能列出 checkpoint、文件和 hash
- [ ] export manifest 能追溯 source checkpoint
- [ ] run/export index 能聚合历史
- [ ] 训练产物能进入 eval 回归路径
- [ ] `PYTHON=.venv/bin/python make finetune-test` 通过
- [ ] `PYTHON=.venv/bin/python make infra-smoke` 通过

## 应该更新的文档

- [finetune-demo](/06-projects/04-finetune-demo)
- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [Finetune 到 Eval 的资产链路案例](/11-case-studies/03-finetune-to-eval-asset-lineage)
- [CLI Surface 速查](/09-reference/06-cli-surface)
- [产物与文件索引](/09-reference/03-artifacts-and-files)

## 常见误区

### “真实训练迁移就是把 mock 换成 trainer”

不够。
还要保留数据、配置、checkpoint、export、history 和 eval 链路。

### “有 checkpoint 就能复现”

不够。
你还需要数据版本、训练配置、manifest、hash 和 export lineage。

### “训练 loss 好就可以发布”

不稳。
发布判断应该来自 eval run/compare 和关键样本分析。

### “Export 只是保存权重”

不是。
export 是把训练中间产物整理成可交付资产，并保留来源。

### “真实训练太复杂，学习项目结构可以先不要”

恰好相反。
真实训练越复杂，越需要一开始保住清晰资产结构。

## 学完应该能回答

读完这一页后，你应该能回答：

1. Finetune 迁移时哪些资产结构最应该保留？
2. 为什么数据层要先于真实 trainer 接入稳定下来？
3. checkpoint index 在真实训练里解决什么问题？
4. export 为什么必须进入 eval 和 release 链路？
5. 真实训练迁移后应该跑哪些检查？

## 继续阅读

- [训练产物、Checkpoint、Export](/05-finetuning-training/02-run-artifacts-export)
- [实验追踪、History、复现](/05-finetuning-training/06-experiment-tracking-history-reproducibility)
- [什么时候该微调](/05-finetuning-training/07-when-to-finetune)
- [验证矩阵](/09-reference/07-validation-matrix)
