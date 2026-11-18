---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/工作流"
created: 2026-11-18
---
# 实操 03：从空画布出第一张图

> 对应章节：[第 3 章 第一个工作流](../docs/ch03_first_workflow.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

从**空画布**亲手搭出文生图工作流，出一张 512×512 的图并保存到 `output\`。
不复制预置工作流。

## 前提

- [ ] [`ch02_task.md`](ch02_task.md) 已完成：ComfyUI 能打开，`ckpt_name` 列表里有模型
- [ ] 建议先把浏览器缩放调到合适，方便看全画布

## 步骤

1. **新建空画布**：Menu（左上图标）→ New。确认画布清空。

2. **按零件清单加 7 个节点**（按 `N` 搜索最快）：
   - `Load Checkpoint` ×1
   - `CLIP Text Encode (Prompt)` ×2（分别做正向、负向）
   - `Empty Latent Image` ×1
   - `KSampler` ×1
   - `VAE Decode` ×1
   - `Save Image` ×1

3. **按连线图连线**（照 [ch03 3.2 节](../docs/ch03_first_workflow.md#c03-02) 的图）：
   ```
   Load Checkpoint(MODEL) → KSampler(model)
   Load Checkpoint(CLIP)  → CLIP Text Encode 正向 → KSampler(positive)
   Load Checkpoint(CLIP)  → CLIP Text Encode 负向 → KSampler(negative)
   Load Checkpoint(VAE)   → VAE Decode(vae)
   Empty Latent Image     → KSampler(latent_image)
   KSampler(latent)       → VAE Decode(samples)
   VAE Decode(IMAGE)      → Save Image(images)
   ```

4. **填参数**：
   - `Load Checkpoint`：`ckpt_name` = 你的 SD1.5 模型
   - 正向提示词：`a cute cat sitting on a windowsill, sunlight, high detail`
   - 负向提示词：`blurry, low quality, watermark, extra limbs`
   - `Empty Latent Image`：512 × 512，batch_size 1
   - `KSampler`：保持默认（steps 20 / cfg 8 / euler / normal / denoise 1）

5. **执行**：点 **Queue Prompt**，等节点执行完。

6. **保存工作流**：Menu → Save，命名为 `my_first_txt2img.json`。

## 验收标准

- [ ] `Save Image` 节点显示出一张 512×512 的猫图
- [ ] `output\` 目录里能找到这张图文件
- [ ] 工作流已存成 `my_first_txt2img.json`，重新 Load 能还原节点和连线

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 把正向提示词里的 `cat` 改成 `dog` | 出图主体变成狗 | 提示词通过 CLIP 条件指导采样内容（ch06 讲）|
| 点 `KSampler` 的 seed 旁的小骰子（随机化）| 两次出图细节不同 | seed 决定初始噪声（ch08 讲）|
| 断开 VAE→VAE Decode 的线再跑 | 图颜色异常或报错 | 没解码条件，见 ch07 |

（实验完连回来，或重新 Load 刚存的工作流）

## 可复现参数记录

| 项 | 值 |
|---|---|
| 模型 | `v1-5-pruned-emaonly-fp16.safetensors` |
| 正向提示词 | a cute cat sitting on a windowsill, sunlight, high detail |
| 负向提示词 | blurry, low quality, watermark, extra limbs |
| 尺寸 | 512 × 512 |
| seed / steps / cfg | 默认 / 20 / 8 |
| sampler / scheduler | euler / normal |

## 常见问题

- 节点飘红 / 连不上线 / 不出图 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)
- 记不清连线 → 回看 [ch03 3.2 连线图](../docs/ch03_first_workflow.md#c03-02)
- 节点名对不上（版本差异）→ 查 [NOTATION 节点名速查](../../NOTATION.md#5-节点名速查界面原文写文档时用反引号)

## 下一步

**入门篇完成！** 你已经能独立搭出并复现文生图。
接下来进入 [第 2 篇 核心节点](../../01_core_nodes/README.md)，从 [ch04 心智模型](../../01_core_nodes/docs/ch04_mental_model.md) 开始，
把每条线「为什么这么连」搞懂——从照抄升级到自己改。
