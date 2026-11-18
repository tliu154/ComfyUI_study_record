---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/节点"
  - "#source/官方文档"
created: 2026-11-18
---
# 附录 A 节点速查表（Node Cheatsheet）

> 前置：无，按需查阅 ｜ 状态：`[已完成]` ｜ 所属：`90_appendix/`

**一句话**：把全主线用到的节点按**用途分组**列在一起，每个节点一句话作用 + 典型接线，
忘了某个节点干嘛、接哪里时回来扫一眼。节点名保留界面英文原文（约定见 [NOTATION](../../NOTATION.md)）。

> 用法：这不是教程，是**字典**。找节点按分组扫；想学原理点每类后面的章节链接。
> 节点名和端口以你当前 ComfyUI 版本为准——社区节点尤其多变（见 [ch24](../../06_ecosystem/docs/ch24_manager.md)）。

## 分组目录

| 分组 | 涵盖 | 深入章节 |
|---|---|---|
| [A.1 加载类](#appA-01) | Checkpoint / UNET / CLIP / VAE / LoRA | [ch05](../../01_core_nodes/docs/ch05_loaders.md) · [ch19](../../04_models_and_lora/docs/ch19_lora.md) |
| [A.2 条件类](#appA-02) | 文本编码 / Conditioning 合并 | [ch06](../../01_core_nodes/docs/ch06_conditioning.md) |
| [A.3 潜空间类](#appA-03) | 空白 latent / 编解码 / 放大 | [ch07](../../01_core_nodes/docs/ch07_latent.md) · [ch11](../../02_image_workflow/docs/ch11_upscale.md) |
| [A.4 采样类](#appA-04) | KSampler 系列 | [ch08](../../01_core_nodes/docs/ch08_ksampler.md) |
| [A.5 图像类](#appA-05) | 读图 / 存图 / 缩放 / 合成 | [ch09](../../02_image_workflow/docs/ch09_img2img.md) |
| [A.6 控制类](#appA-06) | ControlNet / IP-Adapter / 预处理器 | [ch13](../../03_control_and_refine/docs/ch13_controlnet.md) · [ch14](../../03_control_and_refine/docs/ch14_reference.md) |
| [A.7 批处理类](#appA-07) | Primitive / batch | [ch12](../../02_image_workflow/docs/ch12_batch_seed.md) |
| [A.8 工具类](#appA-08) | Reroute / Group / Note / Mute | [ch16](../../03_control_and_refine/docs/ch16_node_skills.md) |

---

<a id="appA-01"></a>

### A.1 加载类（Loaders）

| 节点 | 一句话作用 | 关键输出 | 典型接线 |
|---|---|---|---|
| `Load Checkpoint` | 一体加载 SD1.5 模型，出 MODEL/CLIP/VAE 三路 | MODEL / CLIP / VAE | MODEL→KSampler；CLIP→CLIP Text Encode×2；VAE→VAE Decode |
| `UNET Loader` | 只加载扩散主干（FLUX 等拆分模型用） | MODEL | MODEL→KSampler / Apply IP-Adapter |
| `DualCLIPLoader` | 加载双文本编码器（SDXL/FLUX） | CLIP | CLIP→CLIP Text Encode (SDXL) |
| `CLIPLoader` | 单编码器加载（T5 / CLIP 指定类型） | CLIP | CLIP→文本编码节点 |
| `VAELoader` | 单独加载 VAE | VAE | VAE→VAE Decode / VAE Encode |
| `LoraLoader` | 给模型/CLIP 叠加 LoRA，调强度 | MODEL / CLIP | 串在加载器与下游之间：Checkpoint.MODEL→Lora.model→KSampler |

**够用边界**：SD1.5 用 `Load Checkpoint` 一把梭；FLUX 才需要 UNET+CLIP+VAE 拆分（见 [ch20](../../04_models_and_lora/docs/ch20_workflow_variants.md)）。
模型放 `models/` 对应子目录，按 `R` 刷新（[ch05](../../01_core_nodes/docs/ch05_loaders.md)）。

---

<a id="appA-02"></a>

### A.2 条件类（Conditioning）

| 节点 | 一句话作用 | 关键输入/输出 | 典型接线 |
|---|---|---|---|
| `CLIP Text Encode (Prompt)` | 把正向/负向文字变成 Conditioning | 输入 text / clip；输出 CONDITIONING | clip←Load Checkpoint.CLIP；输出→KSampler.positive/negative |
| `CLIP Text Encode (SDXL)` | SDXL 双编码器版本，带 size 条件 | 同上 + 宽高 | 配合 DualCLIPLoader |
| `Conditioning (Concat)` | 拼接多段条件（如多个 ControlNet / 区域提示） | 多路 CONDITIONING→一路 | 多条件合并后→KSampler |
| `ConditioningAverage` | 按比例混合两段条件 | 两路 + strength | 风格混合场景 |

**够用边界**：90% 场景就是两个 `CLIP Text Encode`（正+负）；合并类是进阶（[ch14](../../03_control_and_refine/docs/ch14_reference.md)、[ch15](../../03_control_and_refine/docs/ch15_prompt_advanced.md)）。

---

<a id="appA-03"></a>

### A.3 潜空间类（Latent）

| 节点 | 一句话作用 | 关键参数 | 典型接线 |
|---|---|---|---|
| `EmptyLatentImage` | 造一张指定尺寸的空白 latent（文生图起点） | width / height / batch_size | 输出→KSampler.latent_image |
| `VAE Encode` | 把像素图编码成 latent（图生图起点） | pixels + vae | Load Image→VAE Encode→KSampler |
| `VAE Decode` | 把 latent 解码成可见图像 | samples + vae | KSampler.LATENT→VAE Decode→Save Image |
| `LatentUpscale` | 在潜空间放大尺寸（Hires-fix 第一步） | upscale_by / method | KSampler→LatentUpscale→二次 KSampler |
| `LatentUpscaleBy` | 按倍数放大 latent | scale_by | 同上 |

**够用边界**：文生图从 `EmptyLatentImage` 起，图生图从 `VAE Encode` 起（[ch09](../../02_image_workflow/docs/ch09_img2img.md)）；解码永远用 `VAE Decode` 收尾。

---

<a id="appA-04"></a>

### A.4 采样类（Sampling）

| 节点 | 一句话作用 | 关键参数 | 典型接线 |
|---|---|---|---|
| `KSampler` | 核心采样器：从噪声一步步去噪出 latent | seed / steps / cfg / sampler_name / scheduler / denoise | model+positive+negative+latent_image 四路进；LATENT 出 |
| `KSampler (Advanced)` | 可控制起止步数（add_noise / start_at_step / end_at_step） | 同上 + start/end | 高阶：分两段采样、Hires-fix、局部重绘 |
| `SamplerCustom` | 自定义采样器/调度器组合，进阶调参 | 自定义 sigmas | 研究/实验用途 |

**参数详解**：见 [ch08](../../01_core_nodes/docs/ch08_ksampler.md)；选择表见 [附录 B](appB_parameter_cheatsheet.md)。
**够用边界**：先只会 `KSampler`；`start_at_step/end_at_step` 到做 Hires-fix（[ch11](../../02_image_workflow/docs/ch11_upscale.md)）再学。

---

<a id="appA-05"></a>

### A.5 图像类（Image）

| 节点 | 一句话作用 | 关键参数 | 典型接线 |
|---|---|---|---|
| `Load Image` | 读取一张本地图片 | image（上传） | 输出 IMAGE→VAE Encode / IP-Adapter |
| `Save Image` | 把图像存到 `output/` | filename_prefix | VAE Decode.IMAGE→Save Image |
| `Preview Image` | 在界面预览不落盘 | — | 接 IMAGE 看你中间结果 |
| `Upscale Image (using Model)` | 用 ESRGAN 放大模型补细节 | upscale_model | VAE Decode→Upscale→Save（[ch11](../../02_image_workflow/docs/ch11_upscale.md)） |
| `ImageScale` / `ImageScaleBy` | 简单插值缩放（不补细节） | width/height / scale | 快速改尺寸 |
| `ImageComposite` / `ImageBlend` | 图像叠加/混合（局部重绘合成用） | 位置/透明度 | 进阶合成 |

**够用边界**：出图收尾就是 `VAE Decode → Save Image`；放大分"潜空间放大"和"图像放大模型"两条路，见 [ch11](../../02_image_workflow/docs/ch11_upscale.md)。

---

<a id="appA-06"></a>

### A.6 控制类（Control）

| 节点 | 一句话作用 | 关键参数 | 典型接线 |
|---|---|---|---|
| `Apply ControlNet` | 把结构条件施加到模型 | strength / start_percent / end_percent | conditioning+control_net+image→输出改后的 conditioning |
| `<Model>OpenPose/Depth/Canny Preprocessor` | 从参考图提取骨架/深度/边缘 | resolution | Load Image→Preprocessor→Apply ControlNet.image |
| `IP-Adapter` / `Apply IPAdapter` | 用参考图控制风格/身份一致性 | weight / weight_type | 加载器→Apply IPAdapter→接 MODEL/conditioning（[ch14](../../03_control_and_refine/docs/ch14_reference.md)） |
| `SetLatentNoiseMask` | 给 latent 加蒙版做局部重绘 | mask | 配合局部重绘（[ch10](../../02_image_workflow/docs/ch10_inpainting.md)） |

**分工记法**：ControlNet 管**结构/姿态**（怎么摆），IP-Adapter 管**风格/身份**（像谁），详见 [ch13](../../03_control_and_refine/docs/ch13_controlnet.md) / [ch14](../../03_control_and_refine/docs/ch14_reference.md)。

---

<a id="appA-07"></a>

### A.7 批处理类（Batch）

| 节点 | 一句话作用 | 典型用法 |
|---|---|---|
| `Primitive` | 一个值驱动多处（seed / 尺寸联动） | 转成 seed 类型连到多个 KSampler，或转换类型（[ch12](../../02_image_workflow/docs/ch12_batch_seed.md)） |
| `EmptyLatentImage.batch_size` | 一次生成多张 | 设 batch_size=4 一次出 4 张 |
| `ImageBatch` | 把多张图合成一个 batch | 批量后处理 |

**够用边界**：锁 seed 复现 vs 换 seed 探索、Primitive 一处改多处，具体见 [ch12](../../02_image_workflow/docs/ch12_batch_seed.md)。

---

<a id="appA-08"></a>

### A.8 工具类（Utility）

| 节点/操作 | 一句话作用 | 场景 |
|---|---|---|
| `Reroute` | 中转连线，整理走线不打分叉 | 工作流变大后理线（[ch16](../../03_control_and_refine/docs/ch16_node_skills.md)） |
| `Node Group` | 把多个节点打包成一组（`Ctrl+G`） | 折叠/复用/标注 |
| `Note` | 画布上加文字便签 | 记录参数说明 |
| `Mute` / `Bypass`（`Ctrl+M` / `Ctrl+B`） | 临时禁用/绕过某节点 | A/B 对比不改线 |
| 右键搜索 / 拖框多选 / 空格拖画布 | 画布操作 | 见 [ch16](../../03_control_and_refine/docs/ch16_node_skills.md) |

---

## 小结

- 主线节点按 8 类归档：加载 / 条件 / 潜空间 / 采样 / 图像 / 控制 / 批处理 / 工具。
- 一条文生图主链：`Load Checkpoint → CLIP Text Encode ×2 + EmptyLatentImage → KSampler → VAE Decode → Save Image`。
- 记住"每类挑一个代表节点会用"，剩下的遇到再查；节点名随版本变，以界面为准。

> 下一附录：[附录 B 参数速查](appB_parameter_cheatsheet.md) ｜ 回 [附录首页](../README.md)
