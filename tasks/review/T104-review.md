# Review Note

Task ID: T104  
Task Title: Glossary 第一批术语初稿  
Review Decision: REVISE_REQUIRED

## Findings

1. 术语主体结构基本合格，但 `Sources` 中有多条不是精确可追溯链接，而是泛称或占位描述。
2. 个别术语表述仍偏强结论，例如 `decode ≠ 解码`、`vLLM 和 SGLang 都没有内置 Router`，这类说法需要更谨慎或给出更明确语境。
3. glossary 的目标是做稳固底层定义，不适合把尚未稳定收敛的架构判断混进术语解释里。

## Action

- 把所有来源替换成精确 URL
- 收紧高争议表述，改成更稳妥的工程描述
- 保留 10 个术语结构，但把定义写得更“可长期复用”
