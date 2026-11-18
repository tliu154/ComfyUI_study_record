---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/提示词"
created: 2026-11-18
---
# 实操 06：玩转正向与负向提示词

> 对应章节：[第 6 章 提示词与条件](../docs/ch06_conditioning.md) ｜ 预计耗时：25 分钟
> 状态：`[已完成]`

## 目标

通过对照实验，直观看到正向提示词「决定画什么」、负向提示词「抑制什么」，理解绿线（CONDITIONING）的作用。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 的工作流已保存
- [ ] 固定 seed（保证对照实验只有提示词一个变量）

## 步骤

1. **加载 ch03 工作流**，把 `KSampler` 的 seed 固定（点seed框旁边的锁，或记住这个值，每轮手动填同一个）。

2. **基线**：正向 `a cute cat sitting on a windowsill, sunlight, high detail`，负向 `blurry, low quality, watermark, extra limbs`。Queue Prompt，存图，记为 A。

3. **只改正向**：把 `cat` 改成 `dog`，其它不动（含 seed）。Queue Prompt，存图，记为 B。
   → 对比 A/B：主体应从猫变狗，证明正向决定内容。

4. **清空负向**：把负向提示词框清空（保留正向为原始 cat 版），seed 不变。Queue Prompt，记为 C。
   → 对比 A/C：C 的质量/瑕疵通常更多，证明负向在抑制问题。

5. **观察绿线**：悬停在 `CLIP Text Encode → KSampler` 的线上，确认类型是 `CONDITIONING`。

## 验收标准

- [ ] A/B 对照看出「正向改 → 内容改」
- [ ] A/C 对照看出「负向清空 → 瑕疵变多」
- [ ] 确认绿线类型是 CONDITIONING

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 正向写中文「一只猫」| 可能效果变差/跑偏 | SD1.5 主要靠英文训练，见 ch06 6.1 |
| 正向/负向端口接反 | 出图反向恶化 | 条件方向反了，见 ch06 6.2 |
| 提示词堆一大段无关词 | 主体反而不突出 | 关键词被稀释，进阶见 ch15 |

## 可复现参数记录

| 轮次 | 正向 | 负向 | seed | 观察 |
|---|---|---|---|---|
| A 基线 | a cute cat... | blurry, low quality... | 固定 | |
| B 改主体 | a cute dog... | 同上 | 同 A | |
| C 清负向 | a cute cat... | （空） | 同 A | |

## 常见问题

- 换了提示词但图没变化 → 检查是不是没重新 Queue Prompt，或 seed 之外还有别的变量
- 中文提示词效果差 → 先用英文，或用中文 CLIP 节点
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 7 章 潜空间](../docs/ch07_latent.md)，搞清那条橙线（LATENT）到底是什么。
