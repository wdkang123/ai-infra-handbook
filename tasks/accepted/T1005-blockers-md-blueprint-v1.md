# BLOCKERS.md Blueprint v1

## Task ID: T1005
## Title: Root / Dev Workflow Starter File Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

## Input Summary:
基于 T905 scaffold（codex-handoff），产出 BLOCKERS.md 蓝图。

---

# BLOCKERS.md Blueprint v1

## 概述

本文档定义 `BLOCKERS.md` 的蓝图——Codex 在实施过程中遇到阻塞问题时记录的文件。

## `BLOCKERS.md` 模板

```markdown
# Blockers

## 使用说明

本文档记录 Codex 在实施过程中遇到的阻塞问题。

记录规则：
1. 每个阻塞问题一条记录
2. 包含：问题描述、影响任务、发现时间、状态
3. 解决后标记为 RESOLVED，不删除记录

---

## Active Blockers

（暂无）

---

## Resolved Blockers

（暂无）

---

## 问题记录模板

### B-XXX: [简短描述]

**问题描述**:
> 详细描述问题

**影响任务**:
- T1-02
- T1-03

**发现时间**: YYYY-MM-DD
**状态**: ACTIVE | RESOLVED
**解决方式**:（解决后填写）
> 描述

**相关文件**:
- `path/to/file.py`
```

## BLOCKERS.md 使用规范

| 规则 | 说明 |
|------|------|
| 问题记录 | 每个阻塞一条，注明影响的任务 |
| 状态流转 | ACTIVE → RESOLVED |
| 保留历史 | 解决后保留记录，标记 RESOLVED |
| 上报机制 | ACTIVE blocker 立即通知 MiniMax |

## 问题优先级

| 优先级 | 定义 | 处理方式 |
|--------|------|---------|
| P1 | 阻塞核心功能（MVP） | 立即暂停相关任务，上报 |
| P2 | 阻塞单个任务 | 暂停当前任务，换其他任务 |
| P3 | 影响效率，不阻塞 | 记录，继续推进 |
```
