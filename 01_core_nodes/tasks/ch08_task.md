---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/采样"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 08：seed / steps / CFG 三参数对照

> 对应章节：[第 8 章 KSampler 参数全解](../docs/ch08_ksampler.md) ｜ 预计耗时：35 分钟
> 状态：`[已完成]`

## 目标

用「一次只动一个变量、锁住其它」的方法，亲眼验证 seed / steps / CFG 各自的作用，学会科学调参。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 工作流已保存
- [ ] 提示词固定，模型固定

## 步骤

1. **基线 A**：seed=42, steps=20, cfg=8, sampler=euler, scheduler=normal。Queue Prompt，存图 A。

2. **验证 seed**：只把 seed 改成 43，其它不动。存图 B。
   → 对比 A/B：应为「同提示词、不同构图/细节」。再把 seed 改回 42，Queue Prompt——应与 A **完全一致**（验证复现）。

3. **验证 steps**：seed 回到 42 锁定，只把 steps 改成 5。存图 C。
   → 对比 A/C：steps=5 应明显没画完（糊/残缺）。再试 steps=30，看是否比 20 好一点或无明显变化。

4. **验证 CFG**：steps 回 20，seed 42，只把 cfg 改成 2，存图 D；再改成 14，存图 E。
   → 对比：cfg=2 应偏题/发散；cfg=14 应过饱和/僵硬。A(cfg=8) 居中较自然。

5. **（可选）换 sampler**：cfg 回 8，只把 sampler 换 `dpmpp_2m`、scheduler 换 `karras`。存图 F，对比细节。

## 验收标准

- [ ] seed=42 两次出图完全一致（理解复现）
- [ ] steps=5 明显没画完（理解步数作用）
- [ ] cfg 2 / 8 / 14 三档看出「发散—自然—僵硬」的趋势
- [ ] 全程一次只动一个变量

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 五个参数一起改 | 无法判断哪个起作用 | 对照实验要单变量，见 ch08 8.5 |
| steps 拉到 100 | 耗时大增但提升有限 | 步数会饱和，见 ch08 8.1 |
| CFG 拉到 30 | 严重过曝/畸变 | 引导过强，见 ch08 8.2 |

## 可复现参数记录

| 轮次 | seed | steps | cfg | sampler/scheduler | 观察 |
|---|---|---|---|---|---|
| A 基线 | 42 | 20 | 8 | euler/normal | |
| B 换 seed | 43 | 20 | 8 | 同 | |
| C 低步数 | 42 | 5 | 8 | 同 | |
| D 低 CFG | 42 | 20 | 2 | 同 | |
| E 高 CFG | 42 | 20 | 14 | 同 | |
| F 换采样 | 42 | 20 | 8 | dpmpp_2m/karras | |

## 常见问题

- seed 改了图没变 → 检查 seed 框是否被锁，或是否真的重新 Queue Prompt
- 出图过曝 → CFG 太高，回 7~8
- 不确定选什么组合 → 用默认 euler + normal + steps20 + cfg8，见 [ch08 速查表](../docs/ch08_ksampler.md#c08-05) / [appB](../../90_appendix/docs/appB_parameter_cheatsheet.md)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

**第 2 篇核心节点完成！** 你已经能解释默认工作流里每条线、每个旋钮。
进入 [第 3 篇 图像工作流](../../02_image_workflow/README.md)，从 [ch09 图生图](../../02_image_workflow/docs/ch09_img2img.md) 开始，
把 denoise 真正用起来，解锁图生图 / 局部重绘 / 放大。
