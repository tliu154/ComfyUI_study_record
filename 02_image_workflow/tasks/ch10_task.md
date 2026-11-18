---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/局部重绘"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 10：局部替换一个物体

> 对应章节：[第 10 章 局部重绘与蒙版](../docs/ch10_inpainting.md) ｜ 预计耗时：35 分钟
> 状态：`[已完成]`

## 目标

用路线 A（`SetLatentNoiseMask`）只改图里的一小块，圈外保持原样；体验蒙版「白改黑留」。

## 前提

- [ ] [`ch09_task.md`](ch09_task.md) 的图生图工作流会搭
- [ ] 一张有明显主体/背景的图（如 ch03 出的猫图）

## 步骤

1. **搭路线 A 骨架**（照 [ch10 10.3](../docs/ch10_inpainting.md#c10-03)）：
   - `Load Image` 上传图，点开 Mask Editor，用画笔**涂白你想改的区域**（如猫旁边的空地），涂完保存
   - `VAE Encode`：pixels 接 Load Image 的 IMAGE，vae 接 Checkpoint 的 VAE
   - `SetLatentNoiseMask`：latent 接 VAE Encode 输出，mask 接 Load Image 的 MASK 输出
   - `SetLatentNoiseMask` 输出 → KSampler(latent_image)
   - 其余（MODEL、正负提示词、VAE Decode、Save Image）同图生图

2. **写提示词**：正向写你要在该区域生成的物体（如 `a red flower bouquet, natural light`），
   负向写质量词；**提示词里也描述背景**，帮助边缘融合。

3. **设参数**：denoise 设 0.9（局部重绘常用高值），seed 固定，steps 20，cfg 8。

4. **执行**：Queue Prompt，观察只有涂白区域被改，涂黑区域保持原图。

5. **验证白改黑留**：故意把蒙版反过来（涂白整图、涂黑要改区），看是不是改了别处——印证方向。

## 验收标准

- [ ] 只有蒙版涂白区被改，其余区域与原图一致
- [ ] 改出的内容符合提示词
- [ ] 理解了「白=重画、黑=保留」

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 蒙版黑白颠倒 | 改了原本想保留的区域 | 白=重画，见 ch10 10.2 |
| denoise 降到 0.3 | 蒙版区重画不充分、拼接感强 | 局部重绘要高位去噪，见 ch10 10.4 |
| 蒙版边缘画很硬 | 交界处可能有接缝 | 软边更自然，见 ch10 10.4 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 输入图 | （文件名）|
| 蒙版方式 | Load Image + Mask Editor（路线 A）|
| 重绘区域 | （描述，如猫旁空地）|
| 正向提示词 | a red flower bouquet, natural light |
| denoise / steps / cfg | 0.9 / 20 / 8 |

## 常见问题

- 改了整张图 → 蒙版方向反了或涂满白了，见 [ch10 10.2](../docs/ch10_inpainting.md#c10-02)
- 边缘有明显接缝 → 用软边、蒙版略涂大、提示词描述环境，见 [ch10 10.4](../docs/ch10_inpainting.md#c10-04)
- 想用 inpaint 专用模型 → 看路线 B，见 [ch10 10.3](../docs/ch10_inpainting.md#c10-03)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 11 章 放大与高清修复](../docs/ch11_upscale.md)，把小图放大到高分辨率。
