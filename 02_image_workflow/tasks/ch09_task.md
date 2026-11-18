---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/图生图"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 09：把一张图改成新图

> 对应章节：[第 9 章 图生图](../docs/ch09_img2img.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

拿一张已有图，用图生图把它改成新图；并跑一组 denoise 对照，直观看到「改动幅度」的变化。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 的文生图工作流已会搭
- [ ] 准备一张输入图（尺寸接近 512×512），放进 ComfyUI 的 `input/` 目录，或上传到 Load Image

## 步骤

1. **加载 ch03 工作流**，把 `Empty Latent Image` 删除。

2. **加图生图起点**：加 `Load Image` 和 `VAE Encode`，按 [ch09 9.2 接线图](../docs/ch09_img2img.md#c09-02) 连：
   ```
   Load Image(IMAGE) → VAE Encode(pixels)
   Checkpoint(VAE)   → VAE Encode(vae)
   VAE Encode(LATENT) → KSampler(latent_image)   ← 替代 Empty Latent Image
   Checkpoint(VAE)   → VAE Decode(vae)           ← 同一个 VAE 也接这里
   ```
   在 Load Image 里选你的输入图。

3. **写提示词**：正向写你想要的新效果（如 `a cat in cyberpunk style, neon lights`），负向写质量词。

4. **denoise 对照**（固定 seed，只改 denoise）：
   - denoise=0.3 → 存图 A（轻微改动）
   - denoise=0.6 → 存图 B（中等）
   - denoise=0.85 → 存图 C（大幅重画）

5. **观察**：三张图与原图对比，看主体的保留程度随 denoise 怎么变。

## 验收标准

- [ ] 出图成功，能看到基于原图改出的新图
- [ ] A/B/C 三张呈现「越改越多」的趋势
- [ ] 确认 VAE 同时接了 Encode 和 Decode 两处

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| denoise 设成 1 | 几乎不看原图，接近文生图 | 起点信息被完全重新去噪，见 ch09 9.3 |
| 喂一张超大图（2000px） | 很慢 / OOM / 畸形 | latent 尺寸跟随原图，见 ch09 9.4 |
| 换输入图但不 Queue Prompt | 图没变 | 换图要重新执行，见 ch09 9.2 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 输入图 | （文件名）|
| 输入图尺寸 | （填写，建议 ~512×512）|
| 正向提示词 | a cat in cyberpunk style, neon lights |
| seed | 固定 |
| denoise A/B/C | 0.3 / 0.6 / 0.85 |
| steps / cfg / sampler | 20 / 8 / euler |

## 常见问题

- 找不到尺寸设置 → 图生图尺寸跟随原图，先把原图缩放好，见 [ch09 9.4](../docs/ch09_img2img.md#c09-04)
- 出图颜色怪 → VAE 没同时接 Encode/Decode
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 10 章 局部重绘与蒙版](../docs/ch10_inpainting.md)，只改图里选定的一小块。
