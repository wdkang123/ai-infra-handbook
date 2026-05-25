# eval-module First Codex Batch v1

## Task ID: T1303
## Title: eval-module Execution Slice Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# eval-module First Codex Batch

本文档定义适合第一轮真实 Codex 编码的文件批次。

## 建议批次

**第一批（当前批次）：E1 + E3**

理由：
- 无外部依赖（不需要 lm-eval、inference-service）
- CLI 骨架和 Result Store 可并行开发
- 是后续所有 slice 的基础

**第二批：E2（Runner）**

理由：核心模块，依赖 E1 的 CLI 框架。

**第三批：E6（测试骨架）**

理由：依赖 E2 的 runner 实现。

**第四批：E4（Comparator）**

理由：依赖 E3 的 result store，独立的比较逻辑。

**第五批：E5（CLI 完整化）**

理由：依赖 E2 + E3 + E4 全部完成后。

---

## 第一批文件清单（E1 + E3）

### E1 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/eval_module/__init__.py` | 包声明 | T1003 |
| `src/eval_module/__version__.py` | 版本常量 | T1003 |
| `src/eval_module/main.py` | Typer CLI 入口，三个子命令 | T1003 |
| `pyproject.toml` | 项目元数据 | T1003 |
| `.env.example` | 环境变量模板 | T1003 |

### E3 产出

| 文件 | 说明 | 蓝本 |
|---|---|---|
| `src/eval_module/results/__init__.py` | results 包 | T1003 |
| `src/eval_module/results/result_store.py` | ResultStore 类，`save()` + `load()` | T1003 |

---

## 第一批 Handoff Note for Codex

1. **CLI 结构：** `main.py` 使用 Typer，三个子命令：`run`、`compare`、`list-tasks`
2. **命令口径：** `python -m eval_module.main run --task mmlu --model Qwen/Qwen2.5-0.5B-Instruct`
3. **Result Store：** `save(result, path)` 和 `load(path)` 返回/读取 JSON
4. **lm-eval 版本：** 锁定 `lm-eval>=0.4.7,<0.6`
5. **backend 字段：** JSON 中 `backend` 是字符串 `"vllm"`，不是 URL
6. **inference-service 依赖：** E1/E3/E4/E6 不需要 inference-service 运行，E2/E5 需要

---

Sources:
- T1003: accepted starter manifest
- T813: accepted validation checklist
- T1203: accepted implementation map
