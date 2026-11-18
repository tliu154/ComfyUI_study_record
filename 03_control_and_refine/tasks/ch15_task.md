---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/提示词"
created: 2026-11-18
---
# 实操 15：提示词权重对照

> 对应章节：[第 15 章 提示词进阶](../docs/ch15_prompt_advanced.md) ｜ 预计耗时：25 分钟
> 状态：`[已完成]`

## 目标

用「锁 seed、单变量」的方法，验证权重语法 `(词:1.3)` 确实能让某个特征更突出，并体验过高权重的副作用。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 工作流会搭
- [ ] 已读 [ch15 15.2 语法](../docs/ch15_prompt_advanced.md#c15-02)

## 步骤

1. **锁 seed**：固定一个 seed，model/steps/cfg/sampler 全固定，只改提示词。

2. **基线 A**：正向 `a portrait of a woman, red hat, soft lighting, detailed`
   Queue Prompt，存图 A。

3. **加权 B**：正向改成 `a portrait of a woman, (red hat:1.4), soft lighting, detailed`
   （只给 red hat 加权）。Queue Prompt，存图 B。
   → 对比 A/B：B 里红帽子应更明显/更突出。

4. **减弱 C**：正向改成 `a portrait of a woman, (red hat:0.5), soft lighting, detailed`
   Queue Prompt，存图 C。→ 红帽子应变弱甚至消失。

5. **过高 D**：改成 `(red hat:2.0)`，看是否出现过饱和/畸形/画面崩——印证过高权重的副作用。

6. **半角坑演示**（可选）：把权重写成全角 `（red hat:1.4）`，跑一次，应发现加权不生效（当普通字符处理）。

## 验收标准

- [ ] A/B/C 显示权重 1.4 > 1.0 > 0.5 的红帽突出程度
- [ ] D 看出过高权重的副作用
- [ ] 全程锁 seed、只改一个词的权重

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 全角括号 `（）` | 加权不生效 | 必须半角，见 ch15 15.2 |
| 所有词都加权 | 等于没区分主次 | 只给关键少数加权，见 ch15 15.1 |
| 写成长句 | 效果可能变差 | 短语分隔更好，见 ch15 15.3 |

## 可复现参数记录

| 轮次 | 正向提示词 | seed | 观察 |
|---|---|---|---|
| A 基线 | a portrait of a woman, red hat, ... | 固定 | |
| B 加权 | ..., (red hat:1.4), ... | 同 | |
| C 减弱 | ..., (red hat:0.5), ... | 同 | |
| D 过高 | ..., (red hat:2.0), ... | 同 | |

## 常见问题

- 加权没变化 → 检查是不是全角符号，或 seed 之外还有别的变量
- 出图崩坏 → 权重过高，回到 1.1~1.4
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 16 章 节点操作进阶](../docs/ch16_node_skills.md)，学会整理复杂工作流（Reroute / Group / Mute）。
