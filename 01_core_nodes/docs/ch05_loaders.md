---
tags:
  - "#course/计算机"
  - "#type/笔记"
  - "#statu/等待复习"
  - "#topic/模型"
  - "#source/官方文档"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 第 5 章 加载器：模型从哪来（Loaders: Checkpoint / UNET / CLIP / VAE）

> 前置：[ch04 心智模型](ch04_mental_model.md) ｜ 对应实操：[`ch05_task.md`](../tasks/ch05_task.md)
> 状态：`[已完成]` ｜ 所属篇：`01_core_nodes/`

**一句话**：`Load Checkpoint` 把大模型文件里的**三样东西一次拆出来**（MODEL / CLIP / VAE），
你也可以用三个独立加载器分开装——本质都是把磁盘上的模型文件送进画布。

> 本篇一条线：[ch04 心智模型](ch04_mental_model.md) → [ch05 加载器](ch05_loaders.md) → [ch06 条件](ch06_conditioning.md)。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [Load Checkpoint：一体三输出](#c05-01) | 5.1 |
| [拆分加载：UNET + CLIP + VAE](#c05-02) | 5.2 |
| [模型目录与刷新（R 键）](#c05-03) | 5.3 |
| [该用哪种加载方式](#c05-04) | 5.4 |

---

<a id="c05-01"></a>

### 5.1 Load Checkpoint：一体三输出

**概念定义**：一个 checkpoint（检查点，`.safetensors` / `.ckpt`）文件，通常打包了三个部件：
- **MODEL / UNET**：真正去噪画图的扩散模型主干（大脑）
- **CLIP**：把文字提示词编码成条件的文本编码器（翻译官）
- **VAE**：把潜空间图像解码成像素图的编解码器（显影师）

`Load Checkpoint` 节点的作用就是：**读这一个文件，把三样东西分别从三个输出端口吐出来**，
你接哪样就用哪样。

**直觉类比**：像一个**组合套餐**——一份文件里含「大脑 + 翻译官 + 显影师」三个人。
`Load Checkpoint` 一口气泡好这三人，你要谁就派谁出场（接谁的输出）。

**界面 / 参数**：
- 控件：`ckpt_name`（下拉选模型文件）
- 输出：`MODEL`（蓝）、`CLIP`（黄）、`VAE`（紫）
- 菜单路径：`model > loaders > Load Checkpoint`

三个输出在 ch03 工作流里的去向：
```
MODEL → KSampler(model)          —— 去噪要用大脑
CLIP  → CLIP Text Encode ×2     —— 编码提示词要用翻译官
VAE   → VAE Decode(vae)         —— 出图要用显影师
```

**常见误区**：
- ❌「checkpoint 就是模型，模型就是 checkpoint」—— 严格说 checkpoint 是**打包文件**，
  里面含三个部件。日常说「下个模型」指的就是这个文件，但心里要清楚它是三合一。
- ❌「三个输出必须全用上」—— 不用。有些工作流只用 MODEL，CLIP/VAE 用别的节点单独加载（见 5.2）。
  没接的输出空着就行，不报错。

> **够用边界**：记住「checkpoint = MODEL + CLIP + VAE 三合一，Load Checkpoint 一次拆出」就够了。
> 三个部件各自的原理分别在本篇 ch06（CLIP）、ch07（VAE）、ch08（MODEL/采样）讲。
> **和已有认知的差异**：如果你以为「模型 = 一个神经网络」，会发现这里是**多个网络打包**。
> 这是 diffusion 生态的历史习惯（方便分发），不是技术必需——所以才有了 5.2 的拆分加载。

---

<a id="c05-02"></a>

### 5.2 拆分加载：UNET + CLIP + VAE

**概念定义**：除了三合一的 `Load Checkpoint`，ComfyUI 还提供**分开加载**的节点：
- `Load Diffusion Model`（或 `UNET Loader`）：只加载扩散主干
- `Load CLIP`（`CLIPLoader`）：只加载文本编码器
- `Load VAE`（`VAELoader`）：只加载 VAE

各自吐出对应类型的输出，接线和三合一版一样。

**直觉类比**：三合一 checkpoint 是**套餐**，拆分加载是**单点**——
你想换翻译官但保留大脑？单点更灵活，不用为了换一样重下整个套餐。

**界面 / 参数**：什么时候需要拆开？
- **FLUX / SDXL 这类新模型**：UNET、CLIP、VAE 常是**分开的文件**，本来就没打包成一个 checkpoint，
  只能分开加载（见 [ch20](../../04_models_and_lora/docs/ch20_workflow_variants.md)）
- **只想换 VAE**：SD1.5 出图颜色发灰时，换个 VAE 文件单独加载，不必换整个模型
- **量化模型**：UNET 用 fp8 版省显存，CLIP/VAE 用原版，混搭（见 [ch18](../../04_models_and_lora/docs/ch18_model_files.md)）

接线对比（三合一 vs 拆分）：
```
三合一：  Load Checkpoint ──→ MODEL / CLIP / VAE（一个节点三根线）
拆分：    Load Diffusion Model ──→ MODEL
          Load CLIP ──→ CLIP
          Load VAE ──→ VAE
```

**常见误区**：
- ❌「拆分加载出的图一定更好」—— 不会。拆分的目的是**灵活和兼容**，不提升画质。
  SD1.5 用三合一最省事。
- ❌「CLIP 文件也能当 checkpoint 用」—— 不能。CLIP 只是文本编码器，没有去噪大脑，单独出不了图。

> **够用边界**：SD1.5 阶段用 `Load Checkpoint` 即可，**这一节先知道有拆分加载这回事**。
> 等学 FLUX 或要换 VAE 时（第 5 篇）再回来细用。
> **和已有认知的差异**：这是**解耦**思想——把打包好的东西拆成独立部件，
> 换一个不影响其它。和写代码时「高内聚低耦合」是一个道理，用配置文件组装而非写死。

---

<a id="c05-03"></a>

### 5.3 模型目录与刷新（R 键）

**概念定义**：ComfyUI 只会列出它**认得的目录**里的模型文件。文件放错地方，下拉列表里就看不到。
放好文件后，需要让 ComfyUI 重新扫描目录（按 `R` 或重启），新模型才出现。

**直觉类比**：像**书架**——书（模型文件）必须放到指定的书架格子里，图书馆系统才登记得到；
临时放桌上的书，系统查不到。放好后要「重新盘点」（刷新）才录入系统。

**界面 / 参数**：常用模型目录（`ComfyUI\models\` 下）——

| 子目录 | 放什么 | 对应加载器 |
|---|---|---|
| `checkpoints\` | SD1.5 / SDXL 三合一 checkpoint | `Load Checkpoint` |
| `diffusion_models\`（或 `unet\`）| 单独的 UNET / diffusion 模型 | `Load Diffusion Model` |
| `clip\` | 单独的文本编码器 | `Load CLIP` |
| `vae\` | 单独的 VAE | `Load VAE` |
| `loras\` | LoRA | `LoraLoader`（[ch19](../../04_models_and_lora/docs/ch19_lora.md)）|
| `controlnet\` | ControlNet 模型 | `ControlNetLoader`（[ch13](../../03_control_and_refine/docs/ch13_controlnet.md)）|

刷新方法：
- 界面里按 **`R`** 键（重新扫描模型目录）
- 或重启 ComfyUI
- 便携包用户注意路径是 `ComfyUI_windows_portable\ComfyUI\models\...`

**常见误区**：
- ❌「下载的模型放桌面/下载文件夹就行」—— 不行，必须放进对应子目录。
- ❌「放了文件列表里就有」—— 要按 `R` 刷新；已在运行的实例不会自动发现新文件。
- ❌「文件名带 `.safetensors.tensor` 之类奇怪后缀」—— 有的下载会带多余后缀，改成正确的 `.safetensors` 再放进去。

> **够用边界**：记住「模型放 `models\` 对应子目录 + 按 R 刷新」这条排查口诀就够了。
> 各格式（safetensors/gguf）、精度（fp16/fp8）的选择是 [ch18](../../04_models_and_lora/docs/ch18_model_files.md) 的事。
> **和已有认知的差异**：ComfyUI 不监视文件系统变化——它启动/按 R 时**拍一次快照**。
> 这和你习惯的「保存文件立刻生效」不同，新增模型要主动刷新。

---

<a id="c05-04"></a>

### 5.4 该用哪种加载方式

**概念定义**：三合一还是拆分？给一个够用的决策规则。

**直觉类比**：出门带装备——**日常通勤一个双肩包全装了**（三合一，省事）；
**专业拍摄按需要挑镜头**（拆分，灵活）。看你干啥。

**界面 / 参数**：决策表——

| 你的情况 | 用哪种 |
|---|---|
| SD1.5 / SDXL 常规文生图、刚入门 | `Load Checkpoint`（三合一，首选）|
| 出图颜色发灰，想单独换 VAE | `Load Checkpoint` 供 MODEL/CLIP + `Load VAE` 单独供 VAE |
| 玩 FLUX / 新模型（文件本就分开）| 拆分加载（UNET + CLIP + VAE）|
| 显存紧张，想 UNET 用低精度 | 拆分加载 + 量化 UNET（见 [ch18](../../04_models_and_lora/docs/ch18_model_files.md)）|

**常见误区**：
- ❌「高级用户都用拆分加载」—— 不是，够用就好。SD1.5 三合一完全够，别为了「看起来专业」折腾。
- ❌「一个工作流里不能混用两种加载方式」—— 可以混。比如 Checkpoint 供 MODEL，CLIP 单独加载，只要类型对得上。

> **够用边界**：入门阶段**无脑用 `Load Checkpoint`**；遇到 FLUX 或要换 VAE 时再拆。这一条就够。
> **和已有认知的差异**：技术选型没有「更高级的就用」，只有「更适合的」。这和工程里避免过度设计的原则一致。

---

## 小结

- `Load Checkpoint` = 一个 checkpoint 文件拆出 MODEL + CLIP + VAE 三输出。
- 拆分加载（UNET/CLIP/VAE 独立节点）用于新模型、换 VAE、量化混搭；SD1.5 不必。
- 模型放 `models\` 对应子目录，按 `R` 刷新才出现在下拉列表。

## 实操与下一步

- 拆开 checkpoint、验证三输出、练习换 VAE：[`ch05_task.md`](../tasks/ch05_task.md)
- 下一章：[第 6 章 提示词与条件](ch06_conditioning.md)
