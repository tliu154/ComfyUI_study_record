---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/控制"
created: 2026-11-18
---
# 实操 13：用 OpenPose 控制人物姿态

> 对应章节：[第 13 章 ControlNet](../docs/ch13_controlnet.md) ｜ 预计耗时：40 分钟
> 状态：`[已完成]`

## 目标

给一张人物参考图，用 OpenPose ControlNet 让生成的人物摆出**相同姿态**，但穿不同衣服/风格（验证结构由 ControlNet、外观由提示词）。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 文生图会搭
- [ ] 已装 ControlNet 模型 `control_v11p_sd15_openpose.pth`，放 `models/controlnet/`，按 `R` 刷新
- [ ] 已装 OpenPose 预处理器（内置或 ControlNet Auxiliary 节点包，见 [ch24](../../06_ecosystem/docs/ch24_manager.md)）
- [ ] 一张人物姿态参考图（放 `input/`）

## 步骤

1. **搭 ControlNet 分支**（照 [ch13 13.3 骨架](../docs/ch13_controlnet.md#c13-03)）：
   ```
   Load Image(参考图) → OpenPose 预处理器 → 骨架图 IMAGE → Apply ControlNet(image)
   ControlNetLoader(选 openpose 模型) → CONTROL_NET → Apply ControlNet(control_net)
   ```
   预览一下预处理器输出的骨架图，确认火柴人正确。

2. **合流进主链**：
   ```
   CLIP Text Encode(正向) → Apply ControlNet(positive)
   Apply ControlNet(CONDITIONING) → KSampler(positive)
   ```
   负向仍直接接 KSampler(negative)，其余不变。

3. **写提示词**：正向写外观（如 `a person in a red dress, photo, detailed`）——注意**不要写姿态**，姿态交给参考图。

4. **设参数**：strength=1.0，start=0，end=1.0，seed 固定，steps 20，cfg 8。

5. **执行与验证**：Queue Prompt，看生成人物的姿态是否与参考图火柴人一致，而穿着/风格按你的提示词。

6. **对照实验**：把 strength 降到 0.4 再跑一次，姿态约束应变弱——印证 strength 的作用。

## 验收标准

- [ ] 预处理输出的骨架图正确（火柴人）
- [ ] 生成人物姿态与参考图一致、外观按提示词
- [ ] strength 降低后控制变弱

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 预处理器用 Canny 但模型还是 openpose | 控制失效/乱 | 预处理类型要和模型匹配，见 ch13 13.2 |
| 忘了把 Apply ControlNet 输出接 positive | 姿态完全不受控 | 合并后的 conditioning 没进采样，见 ch13 13.3 |
| strength 设 0 | 等同没加 ControlNet | 控制强度为零，见 ch13 13.4 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 参考图 | （文件名）|
| 预处理器 / ControlNet 模型 | OpenPose / control_v11p_sd15_openpose |
| 正向提示词 | a person in a red dress, photo, detailed |
| strength / start / end | 1.0 / 0 / 1.0 |
| seed / steps / cfg | 固定 / 20 / 8 |

## 常见问题

- 找不到预处理器/模型 → 装 ControlNet Auxiliary + 下模型，见 [ch24](../../06_ecosystem/docs/ch24_manager.md)
- 姿态不受控 → 检查 Apply ControlNet 输出是否接了 KSampler positive
- 脸部/手部畸形 → 常见 ControlNet 副作用，可加 detailer 节点或调 strength
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 14 章 参考图与一致性](../docs/ch14_reference.md)，用 IP-Adapter 保持角色长相一致。
