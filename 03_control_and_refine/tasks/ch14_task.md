---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/参考图"
created: 2026-11-18
---
# 实操 14：固定一张脸换场景

> 对应章节：[第 14 章 参考图与一致性](../docs/ch14_reference.md) ｜ 预计耗时：35 分钟
> 状态：`[已完成]`

## 目标

用 IP-Adapter 加载一张人物参考图，保持脸部特征不变，换不同的提示词场景，看是否还认得出是同一人；并体验 weight 的影响。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 文生图会搭
- [ ] 已装 IP-Adapter 节点包（如 ComfyUI_IPAdapter_plus，见 [ch24](../../06_ecosystem/docs/ch24_manager.md)）
- [ ] 已下 ip-adapter 模型（放 `models/ipadapter/`）和 CLIP Vision 模型（放 `models/clip_vision/`），按 `R` 刷新
- [ ] 一张清晰正脸参考图（放 `input/`）

## 步骤

1. **搭 IP-Adapter 分支**（照 [ch14 14.2 骨架](../docs/ch14_reference.md#c14-02)）：
   ```
   Load Image(参考脸) → IPAdapter 的 image
   IPAdapter Model Loader(选模型) → IPAdapter 的 model
   Load CLIP Vision(选模型) → IPAdapter 的 clip_vision
   IPAdapter 输出 → KSampler 的 positive（融入 conditioning）
   ```

2. **场景 A**：正向提示词 `a person in a business suit, office background, photo`，
   负向写质量词，weight=0.8，seed 固定。Queue Prompt，存图 A。

3. **场景 B（换场景/着装）**：只把提示词改成 `a person in a spacesuit, on mars, cinematic`，
   seed 不变，weight 不变。Queue Prompt，存图 B。
   → 对比 A/B：场景/穿着变了，但脸应还是同一个人。

4. **weight 对照**：把 weight 降到 0.3，再跑场景 B，存图 C。
   → 对比 B/C：weight 低时脸的相似度下降，提示词（场景）影响更大。

## 验收标准

- [ ] A/B 场景不同但脸可辨认是同一人
- [ ] weight 降低后相似度下降，理解权重作用

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| weight 设接近 1 | 连参考图背景/构图都带过来 | 权重太高抄死，见 ch14 14.3 |
| 不装 CLIP Vision | 报错或无效 | IP-Adapter 靠它编码参考图，见 ch14 14.2 |
| 想锁姿态而不是脸 | IP-Adapter 效果差 | 锁姿态该用 ControlNet，见 ch14 14.4 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 参考图 | （文件名，正脸）|
| ip-adapter 模型 / CLIP Vision | （填写）|
| 场景A提示词 | a person in a business suit, office background, photo |
| 场景B提示词 | a person in a spacesuit, on mars, cinematic |
| weight A/B / C | 0.8 / 0.8 / 0.3 |
| seed / steps / cfg | 固定 / 20 / 8 |

## 常见问题

- 找不到 IPAdapter 节点 → 装节点包 + 下模型，见 [ch24](../../06_ecosystem/docs/ch24_manager.md)
- 脸不像参考图 → 提高 weight，或用更清晰正脸参考图
- 想同时锁姿态 → 叠加 ControlNet，见 [ch14 14.4](../docs/ch14_reference.md#c14-04) / [ch13](ch13_controlnet.md)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 15 章 提示词进阶](../docs/ch15_prompt_advanced.md)，把提示词的权重语法写清楚。
