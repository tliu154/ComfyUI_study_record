---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/提示词"
  - "#source/官方文档"
created: 2026-11-18
---
# 第 6 章 提示词与条件（Prompt & Conditioning）

> 前置：[ch05 加载器](ch05_loaders.md)（CLIP 从哪来） ｜ 对应实操：[`ch06_task.md`](../tasks/ch06_task.md)
> 状态：`[已完成]` ｜ 所属篇：`01_core_nodes/`

**一句话**：你写的中文/英文提示词，模型看不懂；`CLIP Text Encode` 把文字**翻译成模型能懂的数字条件（CONDITIONING）**，
再通过绿色的线喂给 `KSampler`，告诉它「画什么、别画什么」。

> 本篇一条线：[ch05 加载器](ch05_loaders.md) → [ch06 条件](ch06_conditioning.md) → [ch07 潜空间](ch07_latent.md)。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [文字怎么变成条件（Text → Conditioning）](#c06-01) | 6.1 |
| [正向与负向（Positive / Negative）](#c06-02) | 6.2 |
| [Conditioning 这条线](#c06-03) | 6.3 |
| [双 CLIP 与 SDXL 编码器](#c06-04) | 6.4 |

---

<a id="c06-01"></a>

### 6.1 文字怎么变成条件（Text → Conditioning）

**概念定义**：`CLIP Text Encode (Prompt)` 节点干一件事：把你输入的**文字提示词**，
用 CLIP 文本编码器转成一组**数字向量**（术语叫 conditioning，条件）。
这组数字才可以被 diffusion 模型用作「画什么」的指导。

**直觉类比**：像**翻译官 + 点菜单**——
你对着母语说「画一只戴帽子的猫」，翻译官（CLIP）把它翻成厨房听得懂的 standardized 订单（数字条件），
厨师（diffusion 模型）照着订单做。没有翻译这一步，厨师听不懂你的话。

**界面 / 参数**：
- 输入端口：`clip`（黄，接 `Load Checkpoint` 的 CLIP 输出）
- 控件：一个多行文本框，写提示词
- 输出端口：`CONDITIONING`（绿）
- 菜单路径：`model > conditioning > CLIP Text Encode (Prompt)`

在 ch03 里你加了**两个**这样的节点：一个写「想要的」（正向），一个写「不想要的」（负向）。

**常见误区**：
- ❌「提示词必须用英文」—— SD1.5/SDXL 主要靠英文训练，**英文效果更稳**；中文也能用，
  但可能要用专门的中文 CLIP 或翻译节点。新手先用英文。
- ❌「CLIP Text Encode 直接出图」—— 不。它只出条件（绿线），出图还得靠 KSampler + VAE Decode。
- ❌「文字越长越好」—— 不是。提示词讲究**关键词 + 权重 + 顺序**，堆长句反而稀释重点。进阶见 [ch15](../../03_control_and_refine/docs/ch15_prompt_advanced.md)。

> **够用边界**：知道「CLIP Text Encode = 把提示词翻译成 CONDITIONING」就够了。
> CLIP 的训练原理（对比学习、图像文本对齐）**完全可跳过**，不影响你用好它。
> **和已有认知的差异**：你写程序时字符串就是字符串，传参即用的；这里文字要经过一个**神经网络编码**
> 变成高维向量才有意义。这不是「文本处理」，是「把语义映射到模型空间」。

---

<a id="c06-02"></a>

### 6.2 正向与负向（Positive / Negative）

**概念定义**：
- **正向提示词（Positive）**：你想要画面里**有什么**——主体、风格、光线、细节
- **负向提示词（Negative）**：你想要画面里**没什么**——模糊、水印、多余肢体、低质量

两个 `CLIP Text Encode` 各自编码，输出两路 CONDITIONING，分别接到 `KSampler` 的 `positive` 和 `negative` 输入。

**直觉类比**：像点菜时**同时说「要什么」和「不要什么」**——
「要一份牛排，七分熟」（正向）+「不要香菜，不要辣」（负向）。
负向提示是 diffusion 生态特别好用的一个设计，等于直接告诉模型「避开这些坑」。

**界面 / 参数**：ch03 用的模板——
```
正向：a cute cat sitting on a windowsill, sunlight, high detail
负向：blurry, low quality, watermark, extra limbs
```

常见的负向词（SD1.5 通用）：
```
low quality, worst quality, blurry, watermark, text, signature,
extra fingers, mutated hands, bad anatomy, deformed
```

**常见误区**：
- ❌「负向提示词可写可不写」—— SD1.5 强烈建议写，能明显改善质量；FLUX 模型通常**不用**负向提示词（机制不同）。
- ❌「正向/负向接反了会怎样」—— 会出反效果（越想要越不出现），检查 `positive`/`negative` 端口别接反。
- ❌「负向里写 'cat' 就能不画猫」—— 负向是抑制，但力度有限，不如直接改正向提示。

> **够用边界**：会写「正向描述主体、负向堆通用质量词」这个套路，就能上手。
> 更复杂的权重语法 `(word:1.2)` 见 [ch15](../../03_control_and_refine/docs/ch15_prompt_advanced.md)。
> **和已有认知的差异**：普通搜索/程序里你只能说「要什么」；diffusion 让你**同时约束反面**，
> 这是 CFG（[ch08](ch08_ksampler.md)）在背后做的对比——它算「有多想要正向、多想避开负向」的差。

---

<a id="c06-03"></a>

### 6.3 Conditioning 这条线

**概念定义**：`CONDITIONING`（绿色线）是提示词编码后的产物，是从 `CLIP Text Encode` 流向 `KSampler` 的绿色数据。
它承载了「引导信息」——告诉采样过程往哪个方向去噪。

**直觉类比**：如果说 LATENT（橙线）是「一块待雕的石头」，CONDITIONING（绿线）就是「雕刻的图纸」。
采样（KSampler）拿着石头、照着图纸，一点点雕出你要的样子。

**界面 / 参数**：一条完整的「提示词通路」——
```
Load Checkpoint(CLIP) ──→ CLIP Text Encode(正向) ──CONDITIONING(绿)──→ KSampler(positive)
                       └→ CLIP Text Encode(负向) ──CONDITIONING(绿)──→ KSampler(negative)
```

关于 CONDITIONING 你能做的事（节点）：
- `Conditioning Combine`：把两路条件合并（进阶用）
- `Conditioning Average`：给两路条件加权平均（进阶用）
- 这些在基础工作流里用不到，知道有这回事即可。

**常见误区**：
- ❌「绿线能连到 VAE Decode」—— 不能。CONDITIONING 只进 `KSampler` 这类需要引导的节点，类型不匹配连不上。
- ❌「改了提示词，但 KSampler 没重跑」—— 提示词变了，条件就变了，KSampler 必须重算。你点 Queue Prompt 整图重跑，所以没问题。

> **够用边界**：知道「绿线 = 提示词条件，从编码器流向采样器」就够了。
> Conditioning 的内部结构（张量形状、注意力掩码）可跳过。
> **和已有认知的差异**：在普通程序里，「配置」和「数据」是分开的；这里提示词被**编码成和数据同类型的数据流**，
> 和图像数据在图上一起流动。这种「一切皆数据」的设计是节点式系统的特点。

---

<a id="c06-04"></a>

### 6.4 双 CLIP 与 SDXL 编码器

**概念定义**：SD1.5 只有**一个**文本编码器（CLIP-L）。
SDXL 和 FLUX 不一样——它们用**两个**文本编码器（如 CLIP-L + CLIP-G，或 CLIP + T5），
理解能力更强。所以新模型需要 `CLIP Text Encode (SDXL)` 这类**双编码器节点**，
或者先 `Conditioning Combine` 合并两路编码。

**直觉类比**：SD1.5 是**一个翻译官**给你翻菜单；SDXL 是**两个翻译官**（一个懂语法、一个懂细节）
一起翻，理解更准。所以点菜流程多了几步——要请两位翻译，再把两份译文合起来给厨师。

**界面 / 参数**：
- SDXL 常用：`CLIP Text Encode (SDXL)` 节点，内部处理双 CLIP
- 或分开：两个编码器节点 + `Conditioning Combine` 合并成一路 CONDITIONING
- FLUX 还要加 T5 编码器，节点更多（见 [ch20](../../04_models_and_lora/docs/ch20_workflow_variants.md)）

**常见误区**：
- ❌「SDXL 用 SD1.5 的编码器节点就行」—— 不行，效果差或报错。模型要和编码器节点配套。
- ❌「双编码器一定要手动合并」—— 用 `CLIP Text Encode (SDXL)` 这个集成节点就不用手动合并，新手用这个。

> **够用边界**：现在只需知道「**SD1.5 用单编码器节点，SDXL/FLUX 要双编码器/专门节点**」这个对应关係。
> SDXL/FLUX 工作流第 5 篇 ch20 才正式搭，这里不要求你会。
> **和已有认知的差异**：这是模型架构差异带来的**工作流分叉**——同一个「文生图」目标，
> 不同模型要连不同的节点。这也是 ComfyUI 让人又爱又恨的地方：灵活，但换个模型要重新学一套连线。

---

## 小结

- `CLIP Text Encode` 把提示词翻译成 CONDITIONING（绿线），喂给 KSampler 指导画什么。
- 正向 = 想要什么，负向 = 不要什么；SD1.5 两个都写，FLUX 通常只写正向。
- 绿线（条件）+ 橙线（潜空间图）一起进 KSampler，一个当图纸一个当石头。
- SD1.5 用单编码器，SDXL/FLUX 要双编码器节点（第 5 篇细讲）。

## 实操与下一步

- 改提示词、试正负向、观察绿线：[`ch06_task.md`](../tasks/ch06_task.md)
- 下一章：[第 7 章 潜空间](ch07_latent.md)
