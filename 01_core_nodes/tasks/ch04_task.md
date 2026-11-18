---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/节点"
created: 2026-11-18
---
# 实操 04：读懂一条工作流的每条线

> 对应章节：[第 4 章 工作流心智模型](../docs/ch04_mental_model.md) ｜ 预计耗时：20 分钟
> 状态：`[已完成]`

## 目标

看着 ch03 搭好的工作流，能逐条说出「这根线传的是什么类型的数据」，并亲眼验证执行顺序是按依赖不是按位置。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 已完成，`my_first_txt2img.json` 已保存
- [ ] ComfyUI 已打开

## 步骤

1. **加载工作流**：Menu → Load，打开 `my_first_txt2img.json`。

2. **给每条线标类型**：对照 [ch04 4.2 类型表](../docs/ch04_mental_model.md#c04-02)，逐条连线说出类型，填进下面的记录表。至少覆盖这 7 条：
   - Checkpoint → KSampler（MODEL）
   - Checkpoint → 正向/负向 CLIP Text Encode（CLIP）
   - CLIP Text Encode → KSampler positive/negative（CONDITIONING）
   - Empty Latent Image → KSampler（LATENT）
   - KSampler → VAE Decode（LATENT）
   - VAE Decode → Save Image（IMAGE）

3. **验证「按依赖不按位置」**：把 `KSampler` 节点拖到画布最左边（摆得比 Checkpoint 还靠左），
   点 Queue Prompt，观察——出图结果和之前**完全一样**（seed 没变的话），说明位置不影响执行。

4. **观察执行顺序**：点 Queue Prompt 时，留意节点边框高亮的先后，验证「源头 → KSampler → VAE Decode → Save Image」的依赖顺序。

5. **验证分流规则**：从 `Load Checkpoint` 的同一个 CLIP 输出，确认它已经连了两条线（正向、负向各一条）——这就是「一输出接多输入」。

## 验收标准

- [ ] 7 条线的类型都能说出来，填进记录表
- [ ] 拖动节点位置后出图不变，理解了「按依赖执行」
- [ ] 能在图上指出一处「一输出接多输入」的分流

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 断开 `VAE Decode → Save Image` 的线 | Save Image 缺输入飘红，无法执行 | 输入端口必须有数据（规则2/依赖）|
| 试图把 `MODEL`(蓝) 连到 `positive`(绿口) | 连不上，圆点不亮 | 类型不匹配（规则3）|

（实验后 Load 工作流还原，或按撤销）

## 可复现参数记录

| 连线 | 数据类型 | 颜色（目测）|
|---|---|---|
| Checkpoint → KSampler.model | MODEL | |
| Checkpoint → CLIP Text Encode.clip | CLIP | |
| CLIP Text Encode → KSampler.positive | CONDITIONING | |
| Empty Latent Image → KSampler.latent_image | LATENT | |
| KSampler → VAE Decode.samples | LATENT | |
| VAE Decode → Save Image.images | IMAGE | |

## 常见问题

- 端口悬停看不到类型名 → 可能是旧版本，靠颜色判断即可
- 连线飘红 → 缺输入或类型错，对照 [ch04 4.4](../docs/ch04_mental_model.md#c04-04)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 5 章 加载器：模型从哪来](../docs/ch05_loaders.md)，搞清 `Load Checkpoint` 那一体三输出到底是什么。
