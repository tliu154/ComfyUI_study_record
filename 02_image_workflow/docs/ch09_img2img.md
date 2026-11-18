---
tags:
  - "#course/计算机"
  - "#type/笔记"
  - "#statu/等待复习"
  - "#topic/图生图"
  - "#source/官方文档"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 第 9 章 图生图（Image-to-Image）

> 前置：[ch07 潜空间](../../01_core_nodes/docs/ch07_latent.md)（VAE Encode）· [ch08 denoise](../../01_core_nodes/docs/ch08_ksampler.md) ｜ 对应实操：[`ch09_task.md`](../tasks/ch09_task.md)
> 状态：`[已完成]` ｜ 所属篇：`02_image_workflow/`

**一句话**：文生图是从空白底开始画，图生图是**拿一张已有图当起点**——
把原图用 `VAE Encode` 编成 latent，再用 `denoise` 控制「改多少」，让模型在原图基础上改出新图。

> 本篇一条线：[ch09 图生图](ch09_img2img.md) → [ch10 局部重绘](ch10_inpainting.md) → [ch11 放大](ch11_upscale.md) → [ch12 批处理](ch12_batch_seed.md)。
> 四章都建立在同一个认知上：一切生成都在 latent 上做，换「起点 latent」就换玩法。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [从一张已有图出发](#c09-01) | 9.1 |
| [VAE Encode 替换 Empty Latent Image](#c09-02) | 9.2 |
| [denoise 决定改动幅度](#c09-03) | 9.3 |
| [常见坑：尺寸不匹配](#c09-04) | 9.4 |

---

<a id="c09-01"></a>

### 9.1 从一张已有图出发

**概念定义**：图生图（Img2Img）指**以一张已有的图片为起点**，结合提示词生成新图。
它和文生图唯一的核心差别是「起点 latent 从哪来」：
- 文生图：起点是 `Empty Latent Image` 造的**空白（随机噪声）latent**
- 图生图：起点是 `Load Image + VAE Encode` 把**原图编码成的 latent**

起点不一样，后面的 KSampler → VAE Decode → Save Image 完全一样。

**直觉类比**：文生图是**在一张白纸上作画**；图生图是**拿一张现成的画来改**——
你可以只改个颜色（少改），也可以大改构图（多改），但笔下的起点是那张已有的画。
「改多少」就是 denoise（[ch08 8.4](../../01_core_nodes/docs/ch08_ksampler.md#c08-04)）。

**界面 / 参数**：图生图新增/改动的两个节点——
- `Load Image`：选一张本地图（控件 `image` 上传；也可从 `input/` 目录读）
- `VAE Encode`：输入 `pixels`（接 Load Image 的 IMAGE）+ `vae`（接 Checkpoint 的 VAE），输出 LATENT

**常见误区**：
- ❌「图生图要换一整套节点」—— 不用。只把工作流的 `Empty Latent Image` 换成 `Load Image + VAE Encode`，其余不动。
- ❌「图生图 = 局部重绘」—— 不同。图生图改**整张图**（只是幅度可控）；局部重绘只改**蒙版圈选的区域**（[ch10](ch10_inpainting.md)）。

> **够用边界**：记住「图生图 = 把原图编码成 latent 当起点，其余和文生图一样」就够了。
> VAE Encode 的数学不用懂，会连线即可。
> **和已有认知的差异**：你用 PS「滤镜」是在像素上直接操作；这里的改动发生在**压缩的 latent 空间**，
> 经 KSampler 去噪 + VAE Decode 后才变回像素。所以结果往往有「重新诠释」的味道，不是像素级微调。

---

<a id="c09-02"></a>

### 9.2 VAE Encode 替换 Empty Latent Image

**概念定义**：`VAE Encode` 是把真实图片（IMAGE）**压缩编码成 latent** 的节点，是 `VAE Decode` 的逆过程。
在图生图里，它把原图变成「带内容的起点 latent」。

**直觉类比**：`VAE Decode` 是「把底片洗成照片」，`VAE Encode` 是「把照片翻拍回底片」——
一正一反。你把现有照片翻拍成底片，再拿这张底片去暗房重新处理，出的就是「基于原照片的新照片」。

**界面 / 参数**：完整接线（对比文生图，只换起点部分）——
```
【图生图起点】
Load Image(IMAGE) ──→ VAE Encode(pixels)
Load Checkpoint(VAE) ──→ VAE Encode(vae)
VAE Encode(LATENT) ──→ KSampler(latent_image)      ← 替换掉 Empty Latent Image

【其余不变】
Load Checkpoint(MODEL) ──→ KSampler(model)
CLIP Text Encode 正向/负向 ──→ KSampler(positive/negative)
KSampler(latent) ──→ VAE Decode(samples)
Load Checkpoint(VAE) ──→ VAE Decode(vae)           ← 同一个 VAE 也供这里
VAE Decode(IMAGE) ──→ Save Image(images)
```
注意 `Load Checkpoint` 的 VAE **同时供 VAE Encode 和 VAE Decode** 两个节点（一输出接多输入，[ch04](../../01_core_nodes/docs/ch04_mental_model.md#c04-04)）。

**常见误区**：
- ❌「VAE Encode 和 Decode 接反」—— Encode 吃 IMAGE 吐 LATENT（进 KSampler 前）；Decode 吃 LATENT 吐 IMAGE（出图）。别弄反。
- ❌「Load Image 上传后换图，latent 没更新」—— 换图会重新编码，但要重新 Queue Prompt 才生效。

> **够用边界**：会照上面接好 VAE Encode、知道它替代了 Empty Latent Image 就够了。
> **和已有认知的差异**：Encode/Decode 是一对**有损**变换（压缩），所以图生图即使 denoise=0，
> 出来的图也可能与原图略有差异——因为经历了一次「编码再解码」的往返，不是无损复制。

---

<a id="c09-03"></a>

### 9.3 denoise 决定改动幅度

**概念定义**：在图生图里，`denoise` 是**最关键**的参数（0~1）。它决定在原图 latent 基础上「重新去噪多少」：
- 越低：保留越多原图信息，改动小
- 越高：原图影响越弱，越接近文生图从零生成

**直觉类比**：像**改画的力度**——
denoise=0.3 是「轻轻调个色」，0.6 是「换个主体但保留构图」，0.9 是「几乎重画，只隐约像原图」。
（完整经验值表见 [ch08 8.4](../../01_core_nodes/docs/ch08_ksampler.md#c08-04)）

**界面 / 参数**：调 denoise 的实操建议——
- **换风格/上色**：0.3~0.5
- **改主体、保构图**：0.5~0.7
- **大幅重画**：0.75~0.85
- 图生图里 KSampler 的 denoise 不再是 1，这是和文生图**唯一必须改**的采样参数

配合提示词：denoise 低时，提示词主要影响「细节/风格」；denoise 高时，提示词能大幅改变内容。

**常见误区**：
- ❌「图生图 denoise 留 1」—— 那就等于丢弃原图、接近文生图了，失去图生图意义。
- ❌「denoise 越低越像原图就越好」—— 取决于目的。想改东西却设太低，等于没改。

> **够用边界**：记住「**图生图要把 denoise 从 1 降下来，0.5~0.7 起步**」。具体值按目的试。
> denoise 影响的数学（在去噪第几步注入原图 latent）跳过。
> **和已有认知的差异**：文生图里我们说「denoise 保持 1 别动」，图生图里它是**主旋钮**——
> 同一个参数在两个场景地位完全不同，因为起点 latent 的性质变了（纯噪声 vs 带内容的图）。

---

<a id="c09-04"></a>

### 9.4 常见坑：尺寸不匹配

**概念定义**：图生图里原图尺寸、VAE Encode 的输出 latent 尺寸、模型推荐尺寸三者要协调，否则出图异常。
`VAE Encode` 出来的 latent 尺寸直接等于「原图尺寸 ÷ 8」，没有单独设置项。

**直觉类比**：像**照片冲印**——原图的比例已经定了，你没法在不裁剪/拉伸的情况下印成任意尺寸。
图生图的起点尺寸由原图决定，不像文生图能在 Empty Latent Image 里随便填。

**界面 / 参数**：处理办法——
- 原图尽量**先裁到模型推荐尺寸附近**（SD1.5 约 512×512、SDXL 约 1024×1024，见 [ch07 7.4](../../01_core_nodes/docs/ch07_latent.md#c07-04)）
- 想改尺寸：在 `VAE Encode` 前加 `Resize Image` / `ImageScale` 节点把原图缩放到合适尺寸
- 比例不一致时用裁剪（crop）而非拉伸，避免变形

**常见误区**：
- ❌「把 2000×2000 的图直接丢进来出图」—— latent 巨大，显存爆或出图畸形。先缩放。
- ❌「图生图能靠改 latent 尺寸参数放大」—— 图生图没有独立尺寸参数，尺寸来自原图；要放大走 [ch11](ch11_upscale.md)。

> **够用边界**：记住「原图先缩放到模型推荐尺寸、别直接喂超大图」。
> 裁剪/缩放节点的细节用到再查。
> **和已有认知的差异**：文生图的尺寸是「声明式」的（填数字就有）；图生图的尺寸是「继承式」的（跟随原图）。
> 这个差别常让新手困惑——图生图里找不到 width/height 输入框，因为它在原图里。

---

## 小结

- 图生图 = 把原图 `VAE Encode` 成 latent 当起点，其余和文生图一样。
- 用 `Load Image + VAE Encode` 替换 `Empty Latent Image`；VAE 同时供 Encode 和 Decode。
- `denoise` 是主旋钮：0.5~0.7 起步，越低越像原图，越高越接近重画。
- 原图先缩放到模型推荐尺寸，别喂超大图；尺寸跟随原图，没有独立设置项。

## 实操与下一步

- 做一张图生图、跑 denoise 对照：[`ch09_task.md`](../tasks/ch09_task.md)
- 下一章：[第 10 章 局部重绘与蒙版](ch10_inpainting.md)
