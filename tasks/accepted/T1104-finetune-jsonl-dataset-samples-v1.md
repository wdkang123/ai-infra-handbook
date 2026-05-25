# finetune-demo JSONL Dataset Samples v1

## Task ID: T1104
## Title: finetune-demo Fixture Pack
## Owner: MINIMAX
## Status: REVIEW_PENDING

---

# finetune-demo JSONL Dataset Samples

本文档定义 finetune-demo 使用的 JSONL 训练数据集样本，对应真实文件 `finetune-demo/data/samples/`。

## JSONL 格式说明

每行一个 JSON 对象，表示一条训练样本：
```json
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

---

## Sample 1: 通用对话样本

**对应文件：** `finetune-demo/data/samples/conversation_sample_01.jsonl`

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful math tutor."}, {"role": "user", "content": "What is 15% of 80?"}, {"role": "assistant", "content": "15% of 80 is 12. Here's how: 80 × 0.15 = 12"}]}
{"messages": [{"role": "system", "content": "You are a helpful math tutor."}, {"role": "user", "content": "Solve for x: 2x + 5 = 13"}, {"role": "assistant", "content": "2x + 5 = 13 → 2x = 8 → x = 4"}]}
{"messages": [{"role": "system", "content": "You are a helpful math tutor."}, {"role": "user", "content": "What is the square root of 144?"}, {"role": "assistant", "content": "The square root of 144 is 12, because 12 × 12 = 144."}]}
{"messages": [{"role": "system", "content": "You are a helpful math tutor."}, {"role": "user", "content": "If a train travels 60km in 2 hours, what is its speed?"}, {"role": "assistant", "content": "Speed = Distance / Time = 60km / 2h = 30 km/h"}]}
{"messages": [{"role": "system", "content": "You are a helpful math tutor."}, {"role": "user", "content": "What is 25% of 200?"}, {"role": "assistant", "content": "25% of 200 is 50. (200 × 0.25 = 50)"}]}
```

---

## Sample 2: 代码生成样本

**对应文件：** `finetune-demo/data/samples/code_generation_sample_01.jsonl`

```jsonl
{"messages": [{"role": "system", "content": "You are a Python coding assistant."}, {"role": "user", "content": "Write a function that checks if a string is a palindrome."}, {"role": "assistant", "content": "def is_palindrome(s):\n    s = s.lower().replace(' ', '')\n    return s == s[::-1]"}]}
{"messages": [{"role": "system", "content": "You are a Python coding assistant."}, {"role": "user", "content": "Write a function to calculate the factorial of a number."}, {"role": "assistant", "content": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)"}]}
{"messages": [{"role": "system", "content": "You are a Python coding assistant."}, {"role": "user", "content": "Write a function to find the maximum element in a list."}, {"role": "assistant", "content": "def find_max(lst):\n    return max(lst) if lst else None"}]}
{"messages": [{"role": "system", "content": "You are a Python coding assistant."}, {"role": "user", "content": "Write a function to flatten a nested list."}, {"role": "assistant", "content": "def flatten(nested):\n    result = []\n    for item in nested:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result"}]}
{"messages": [{"role": "system", "content": "You are a Python coding assistant."}, {"role": "user", "content": "Write a function to reverse a linked list."}, {"role": "assistant", "content": "def reverse_linked_list(head):\n    prev, curr = None, head\n    while curr:\n        next_temp = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_temp\n    return prev"}]}
```

---

## Sample 3: 指令微调样本（Alpaca 格式）

**对应文件：** `finetune-demo/data/samples/alpaca_format_sample_01.jsonl`

```jsonl
{"messages": [{"role": "user", "content": "What is the capital of France?"}, {"role": "assistant", "content": "The capital of France is Paris."}]}
{"messages": [{"role": "user", "content": "Explain photosynthesis in one sentence."}, {"role": "assistant", "content": "Photosynthesis is the process by which plants convert sunlight, water, and CO2 into glucose and oxygen."}]}
{"messages": [{"role": "user", "content": "Write a haiku about autumn."}, {"role": "assistant", "content": "Autumn leaves fall down\nGolden and crimson and brown\nQuiet earth below"}]}
{"messages": [{"role": "user", "content": "What is the boiling point of water in Celsius?"}, {"role": "assistant", "content": "The boiling point of water is 100°C at standard atmospheric pressure."}]}
{"messages": [{"role": "user", "content": "How does a refrigerator keep food cold?"}, {"role": "assistant", "content": "A refrigerator uses a refrigerant that absorbs heat from inside and releases it outside, driven by a compressor cycle."}]}
```

---

## Sample 4: 角色扮演对话样本

**对应文件：** `finetune-demo/data/samples/roleplay_sample_01.jsonl`

```jsonl
{"messages": [{"role": "system", "content": "You are a medieval knight. Speak formally and with honor."}, {"role": "user", "content": "Good sir knight, what is your quest?"}, {"role": "assistant", "content": "My quest is to protect the realm from the dragon that lurks in the northern mountains. I shall not rest until it is vanquished."}]}
{"messages": [{"role": "system", "content": "You are a medieval knight. Speak formally and with honor."}, {"role": "user", "content": "Have you any news from the front?"}, {"role": "assistant", "content": "The scouts report that the enemy forces have retreated beyond the river. We may have a brief respite, my liege."}]}
{"messages": [{"role": "system", "content": "You are a medieval knight. Speak formally and with honor."}, {"role": "user", "content": "What is your name and house?"}, {"role": "assistant", "content": "I am Sir Aldric of House Thornwood, sworn protector of the Northern Reach."}]}
```

---

## Sample 5: 多轮对话样本

**对应文件:** `finetune-demo/data/samples/multiturn_sample_01.jsonl`

```jsonl
{"messages": [{"role": "system", "content": "You are a helpful coding assistant."}, {"role": "user", "content": "How do I sort a list in Python?"}, {"role": "assistant", "content": "You can use the sorted() function or the list.sort() method. sorted() returns a new list, while sort() sorts in place."}, {"role": "user", "content": "What about sorting in descending order?"}, {"role": "assistant", "content": "For descending order, use sorted(lst, reverse=True) or lst.sort(reverse=True)."}]}
{"messages": [{"role": "system", "content": "You are a helpful coding assistant."}, {"role": "user", "content": "What is a dictionary in Python?"}, {"role": "assistant", "content": "A dictionary (dict) is a built-in data structure that stores key-value pairs. It's unordered, mutable, and indexed by keys."}, {"role": "user", "content": "How do I add a new key-value pair?"}, {"role": "assistant", "content": "Use d[new_key] = new_value, e.g., my_dict['name'] = 'Alice'."}]}
{"messages": [{"role": "system", "content": "You are a helpful coding assistant."}, {"role": "user", "content": "How do I read a file in Python?"}, {"role": "assistant", "content": "Use with open('file.txt', 'r') as f: content = f.read(). This ensures the file is properly closed after reading."}, {"role": "user", "content": "What about reading line by line?"}, {"role": "assistant", "content": "Use with open('file.txt', 'r') as f: for line in f: print(line.strip())"}]}
```

---

## 数据集预处理要求

| 要求 | 说明 |
|---|---|
| 格式 | JSONL（每行一个 JSON） |
| 编码 | UTF-8 |
| 无尾随逗号 | JSONL 行末不能有逗号 |
| `messages` 字段 | 必须为 array，包含 role/content 对象 |
| 角色顺序 | 必须为 `system` → `user` → `assistant` |
| `system` 消息 | 可选，若存在必须在最前 |
| 最小样本长度 | 至少 1 条 user + assistant 对 |
| 最大样本长度 | 不超过 `max_model_len`（如 8192 tokens） |

---

Sources:
1. https://github.com/EleutherAI/lm-evaluation-harness — data format
2. https://github.com/tloen/alpaca-lora — Alpaca dataset format

Risk of Staleness:
- JSONL + chat format is the de facto standard for instruction tuning; stable
