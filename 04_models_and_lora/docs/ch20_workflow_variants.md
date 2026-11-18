---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/工作流"
  - "#source/官方文档"
created: 2026-11-18
---
# 第 20 章 多模型工作流对照（Workflow Variants）

> 前置：[ch05 拆分加载](../../01_core_nodes/docs/ch05_loaders.md#c05-02) · [ch06 双 CLIP](../../01_core_nodes/docs/ch06_conditioning.md#c06-04) · [ch17 模型家族](ch17_model_families.md) ｜ 对应实操：[`ch20_task.md`](../tasks/ch20_task.md)
> 状态：`[已完成]` ｜ 所属篇：`04_models_and_lora/`

**一句话**：前面搭的都是 SD1.5 工作流；换到 SDXL/FLUX，**骨架还是那条链**，
只是「加载器」和「文本编码」这两处节点变了——抓住差异点，换模型就不慌。

> 本篇一条线：[ch17 模型家族](ch17_model_families.md) → [ch18 模型文件](ch18_model_files.md) → [ch19 LoRA](ch19_lora.md) → [ch20 工作流对照](ch20_workflow_variants.md)（第 5 篇收口）。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [为什么 FLUX 节点不一样](#c20-01) | 20.1 |
| [SDXL 工作流差异点](#c20-02) | 20.2 |
| [FLUX 从零搭一条](#c20-03) | 20.3 |
| [用官方模板快速起步](#c20-04) | 20.4 |

---

<a id="c20-01"></a>

### 20.1 为什么 FLUX 节点不一样

**概念定义**：所有文生图工作流的核心链都是：
**加载模型 → 编码提示词 → 采样（KSampler）→ 解码（VAE Decode）→ 保存**。
变的是「加载」和「编码」两处的具体实现，因为不同模型的**组件构成不同**：
- SD1.5：`Load Checkpoint` 三合一 + 单 `CLIP Text Encode`
- SDXL：双 CLIP 编码
- FLUX：UNET + CLIP-L + T5 分开加载 + 多编码器合并

KSampler 之后的部分（latent → VAE Decode → Save Image）三家基本一样。

**直觉类比**：像**不同品牌的车**——
发动机舱布局（加载/编码）不同，但方向盘、油门刹车、四个轮子（采样/解码/保存）是通用操作。
你学会了开车（核心链），换品牌只要熟悉一下发动机舱（前两个环节）。

**界面 / 参数**：一张差异对照表——
| 环节 | SD1.5 | SDXL | FLUX |
|---|---|---|---|
| 加载 | Load Checkpoint | Load Checkpoint 或拆分 | 拆分：UNET+CLIP+T5+VAE |
| 文本编码 | 单个 CLIP Text Encode | SDXL 版双 CLIP 编码 | CLIP-L + T5 两路再合并 |
| 采样 KSampler | euler/normal, cfg 7~8 | 类似 SD1.5 | cfg≈1, steps~20, simple/beta |
| 负向词 | 常用 | 常用 | 一般不用 |
| 解码/保存 | VAE Decode → Save Image | 同 | 同 |

**常见误区**：
- ❌「每个模型都要从零学一套」—— 不用，核心链不变，只学前两环节的变体。
- ❌「把 SD1.5 的节点原样搬给 FLUX」—— 加载器和编码节点对不上，跑不起来。

> **够用边界**：记住「**核心链通用，变的是加载器 + 文本编码两处**」这个骨架认知。
> **和已有认知的差异**：这是「接口稳定、实现可变」的架构思想——
> 就像同一个插件系统里换不同实现，只要接口（KSampler 需要的 MODEL/CONDITIONING/LATENT）一致，
> 前面的「 producer」怎么变都行。理解了类型接口（[ch04](../../01_core_nodes/docs/ch04_mental_model.md#c04-02)），换模型就是拼积木。

---

<a id="c20-02"></a>

### 20.2 SDXL 工作流差异点

**概念定义**：SDXL 工作流和 SD1.5 的主要差异在**双文本编码器**（[ch06 6.4](../../01_core_nodes/docs/ch06_conditioning.md#c06-04)）。
有两种接法：
- **简单**：用 `CLIP Text Encode (SDXL)` 节点（内部处理双 CLIP，一个节点搞定）
- **手动**：两个 CLIP Text Encode（CLIP-L + CLIP-G）各出一路 conditioning，用 `Conditioning Combine` 合并

其余（Load Checkpoint、Empty Latent 1024×1024、KSampler、VAE Decode）和 SD1.5 一样。

**直觉类比**：SDXL 请了**两个翻译官**，你可以用一个「翻译主管」节点（`CLIP Text Encode (SDXL)`）一次性协调两人，
也可以自己分别请两人再把译文合并——结果相同，前者省事，后者灵活。

**界面 / 参数**：SDXL 工作流骨架——
```
Load Checkpoint(SDXL 模型) → MODEL / CLIP / VAE
CLIP Text Encode (SDXL) ×2（正/负）→ conditioning
  （或双 CLIP 两路 + Conditioning Combine）
Empty Latent Image 1024×1024 → latent
KSampler(euler/normal, steps~30, cfg~7) → VAE Decode → Save Image
```
可选：SDXL Refiner 二次精修（另接一条小链，进阶）。

**常见误区**：
- ❌「SDXL 用普通 CLIP Text Encode 就行」—— 效果打折或报错，要用 SDXL 版或双 CLIP 合并。
- ❌「SDXL 分辨率还填 512」—— 浪费，SDXL 最佳 1024（[ch17](ch17_model_families.md#c17-02)）。

> **够用边界**：知道「SDXL = 用 `CLIP Text Encode (SDXL)` + 1024 尺寸，其余同 SD1.5」。
> Refiner 进阶按需。
> **和已有认知的差异**：从「一个编码器」到「两个编码器」是量变到质变——它让 SDXL 理解提示词更强，
> 但代价就是工作流多几个节点。这是「能力增强反映为结构复杂」的典型。

---

<a id="c20-03"></a>

### 20.3 FLUX 从零搭一条

**概念定义**：FLUX 工作流是差异最大的，主要因为它是**多文件分开加载 + 多编码器**。
（前提：已下好 FLUX UNET、CLIP-L、T5、VAE 文件并放对目录，[ch18](ch18_model_files.md)）

**直觉类比**：像**组装一台分体式音响**——
SD1.5 是一体机（一个文件全包），FLUX 是功放+音箱+播放器分开（四个文件），
你得一根根线接起来，但每部分可以单独选最好的。

**界面 / 参数**：FLUX 文生图骨架——
```
【分开加载】
Load Diffusion Model(UNET, 常用 fp8) → MODEL
Load CLIP(CLIP-L, clip_l.safetensors) → CLIP-L
Load CLIP(T5, t5xxl_fp8.safetensors) → T5
Load VAE(ae.safetensors) → VAE

【双编码合并】
CLIP Text Encode(用 CLIP-L) → conditioning #1
CLIP Text Encode(用 T5) → conditioning #2
Conditioning Combine(#1, #2) → 合并 conditioning → KSampler(positive)

【采样】
Empty Latent Image(1024 附近) → KSampler
KSampler: cfg≈1, steps≈20, sampler euler / scheduler simple

【解码】
KSampler(latent) → VAE Decode(VAE) → Save Image
```
要点：**cfg≈1、一般不写负向词**（distilled 模型特性，[ch17 17.3](ch17_model_families.md#c17-03)）。

**常见误区**：
- ❌「FLUX 也 cfg=8、写满负向词」—— 错，distilled FLUX 要 cfg≈1、负向留空，否则画面异常。
- ❌「少装一个编码器」—— CLIP-L 和 T5 通常都要，缺一个理解能力下降或报错。
- ❌「FP8 UNET 配 FP16 CLIP 一定不兼容」—— 混搭精度和常见，能跑；不稳定时统一精度排查。

> **够用边界**：能照骨架接出一条 FLUX 文生图、知道 cfg≈1 和不写负向词即可。
> T5 的作用、rectified flow 数学跳过。
> **和已有认知的差异**：这是从「一体机」到「分体机」的思维转换——文件更多、接线更多，
> 但每块可独立替换（换 VAE、换精度），灵活性更高。工程上「解耦」的代价与收益在这里很直观。

---

<a id="c20-04"></a>

### 20.4 用官方模板快速起步

**概念定义**：ComfyUI 官方和社区提供**现成的工作流模板**（尤其对新模型如 FLUX/Z-Image），
不用从空画布一个个加节点——直接导入模板，改提示词就能跑，还能对照学习节点结构。

**直觉类比**：像**用现成菜谱**——
你学会了做菜原理（前面的章节），现在直接用大厨的配方（模板）起步，
先做出成品，再研究配方为什么这么搭。比自己从零试错快得多。

**界面 / 参数**：怎么用模板——
- ComfyUI 界面里通常有 `Workflow > Browse Templates`（或模板标签页），按模型分类
- 官方 Cloud 也提供模板（[ch02 2.4](../../00_getting_started/docs/ch02_installation.md#c02-04)）
- 导入后：按提示放好所需模型文件 → 改提示词 → Queue Prompt
- **学习用法**：导入后逐个节点看连线，对照本章骨架理解每块作用

**常见误区**：
- ❌「模板导入就能跑，不用管模型」—— 模板只含节点和参数，模型文件要你自己下（[ch18](ch18_model_files.md)），缺失会报错。
- ❌「用模板就学不到东西」—— 相反，好模板是最佳教材：跑通后逐节点研究，比抽象讲解直观。

> **够用边界**：知道「新模型先找官方模板起步，导入后对照骨架学节点，模型文件自己放」。
> **和已有认知的差异**：这像**用脚手架/模板项目起步**——工程师不会每次从空项目写起，
> 而是拿成熟模板改。ComfyUI 的模板工作流就是它的「项目脚手架」，是学习新模型的高效路径。

---

## 小结

- 核心链通用（加载→编码→采样→解码→保存），换模型只变「加载器 + 文本编码」两处。
- SDXL：用 `CLIP Text Encode (SDXL)`（或双 CLIP 合并）+ 1024 尺寸，其余同 SD1.5。
- FLUX：UNET+CLIP-L+T5+VAE 分开加载，双编码合并，cfg≈1，不写负向词。
- 新模型先用官方模板起步（模板不含模型文件，模型自己下），再逐节点对照学习。

## 实操与下一步

- 导入一条模板工作流、标出与 SD1.5 的节点差异：[`ch20_task.md`](../tasks/ch20_task.md)
- **第 5 篇模型与 LoRA 完成**！下一篇 [第 6 篇 视频与进阶](../../05_video_and_advanced/README.md)，
  从 [ch21 视频生成入门](../../05_video_and_advanced/docs/ch21_video_basics.md) 开始。
