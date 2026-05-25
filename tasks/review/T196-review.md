# Review Note

Task ID: T196  
Task Title: 产出 Cache / Prefix Caching 章节初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. 最小实践写了“对比两个请求的 TTFT”，但示例命令并没有说明如何采集 TTFT，也没有给出可观察该指标的明确方法。
2. 第 9 节把“第二个请求 TTFT 低于第一个请求”写成输出物，会让这段实践看起来像已经具备了可验证的测量闭环，但当前示例还没做到。

## Action

- 把最小实践改成当前命令真能支撑的结果，例如“复用共享前缀请求并观察整体响应时间或服务日志”
- 如果保留 `TTFT`，必须补上明确的观测方式；否则应从实践和输出物里去掉
