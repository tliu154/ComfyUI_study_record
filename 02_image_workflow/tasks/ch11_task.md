---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/放大"
created: 2026-11-18
---
# 实操 11：把小图放大到高清

> 对应章节：[第 11 章 放大与高清修复](../docs/ch11_upscale.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

用「两段式 Hires-fix」把一张 512 图放大到 1024/2048，构图不变、细节增加；对比直接出大图的效果。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 工作流会搭
- [ ] 有一张 512×512 的好底图（或工作流第一段出的图）

## 步骤

1. **第一段（出底图）**：用你的文生图工作流，Empty Latent Image 设 512×512，出一张构图好的图（记下 seed）。

2. **搭第二段（Hires-fix）**，照 [ch11 11.2 骨架](../docs/ch11_upscale.md#c11-02)：
   ```
   KSampler #1(latent) → LatentUpscale(samples)
     upscale_method = nearest-exact，scale_by = 2
   LatentUpscale(latent) → KSampler #2(latent_image)
     第二个 KSampler：denoise = 0.5，steps = 20，seed 固定
   KSampler #2(latent) → VAE Decode → Save Image
   ```
   两个 KSampler 共用 MODEL 和正负提示词。

3. **执行**：Queue Prompt，得到 1024×1024 的放大图，保存为 A。

4. **对比直接出大图**：另开一条工作流，Empty Latent Image 直接填 1024×1024，同样 seed/提示词，出图保存为 B。
   → 对比 A（两段）和 B（直接）：A 通常构图更稳、细节更自然；B 可能出现重复/崩坏。

5. **（可选）再放一倍**：把 scale_by 再乘 2，试试 2048；显存不够就停。

## 验收标准

- [ ] 成功出 1024 放大图，构图与底图一致、细节更丰富
- [ ] 对比过 A（两段）vs B（直接），理解为何两段更稳
- [ ] 第二个 KSampler 的 denoise 设了低值

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 第二个 KSampler denoise 设 1 | 构图被重画、可能变样 | 高位去噪丢弃底图构图，见 ch11 11.2 |
| 直接 2048×2048 一段出图 | 重复头/畸形 | 超出训练分辨率，见 ch11 11.1 |
| scale_by 一次填 8 | OOM 或崩 | 放太大，应小步多次，见 ch11 11.4 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 底图尺寸 / seed | 512×512 / 固定 |
| 放大方式 | LatentUpscale + 二次 KSampler |
| scale_by / upscale_method | 2 / nearest-exact |
| 二次 denoise / steps | 0.5 / 20 |
| 最终尺寸 | 1024×1024 |

## 常见问题

- 放大的图构图变了 → 二次 denoise 太高，调低到 0.4~0.6
- OOM → 减小 scale_by、分小步、开低显存模式（[ch26](../../06_ecosystem/docs/ch26_performance.md)）
- 想更锐利 → 加像素放大模型（[ch11 11.3](../docs/ch11_upscale.md#c11-03)，模型放 `models/upscale_models/`）
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 12 章 批处理与种子](../docs/ch12_batch_seed.md)，一次出多张、学会管理种子。
