---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/控制"
  - "#source/官方文档"
created: 2026-11-18
---
# 第 13 章 ControlNet：构图与姿态控制（ControlNet）

> 前置：[ch09 图生图](../../02_image_workflow/docs/ch09_img2img.md)（图像输入思路）· [ch06 条件](../../01_core_nodes/docs/ch06_conditioning.md) ｜ 对应实操：[`ch13_task.md`](../tasks/ch13_task.md)
> 状态：`[已完成]` ｜ 所属篇：`03_control_and_refine/`

**一句话**：ControlNet 让你用一张**参考图**去「框住」生成——
把参考图的姿态骨架、深度、边缘线提取出来，作为额外的条件喂给模型，
于是你能精确控制人物摆什么姿势、画面是什么构图，而不只靠提示词碰运气。

> 本篇一条线：[ch13 ControlNet](ch13_controlnet.md) → [ch14 参考图一致性](ch14_reference.md) → [ch15 提示词进阶](ch15_prompt_advanced.md) → [ch16 节点技巧](ch16_node_skills.md)。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [用参考图框住构图](#c13-01) | 13.1 |
| [预处理器：提取骨架/深度/边缘](#c13-02) | 13.2 |
| [连线与 ControlNet Apply](#c13-03) | 13.3 |
| [strength / start / end 怎么调](#c13-04) | 13.4 |

---

<a id="c13-01"></a>

### 13.1 用参考图框住构图

**概念定义**：ControlNet 是一种**额外的条件控制**机制。
普通文生图只有「提示词」这一个引导（[ch06 的 CONDITIONING](../../01_core_nodes/docs/ch06_conditioning.md)）；
ControlNet 让你再加一路「结构引导」——来自一张参考图的**姿态、深度或边缘**。
模型生成时会同时听提示词（画什么内容）和 ControlNet（按什么结构画）。

**直觉类比**：像**临摹**——
- 只给提示词 = 闭着眼凭描述画（内容对，但构图/姿势随机）
- 加 ControlNet = 给你一张**线稿/火柴人**让你照着画（姿势、构图被框住，但穿什么衣服、什么风格由提示词决定）

所以 ControlNet 管「骨架结构」，提示词管「外观内容」，两者分工。

**界面 / 参数**：ControlNet 能控制的常见类型——
- **姿态（OpenPose）**：火柴人骨架，控制人物动作、手的位置
- **深度（Depth）**：近大远小的深度图，控制空间层次和构图
- **边缘（Canny / LineArt）**：轮廓线，控制物体的形状边界
- **法线 / 分割 / 涂鸦**等其它类型

**常见误区**：
- ❌「ControlNet 直接输出图」—— 不。它输出的是**额外的 conditioning**，要接进 KSampler 才起作用。
- ❌「ControlNet 会照搬参考图的风格和颜色」—— 不会，它只提取**结构**（骨架/深度/边缘），风格和内容是你的提示词决定的。
- ❌「提示词可以不要了」—— 要。ControlNet 只管结构，画成什么还得靠提示词。

> **够用边界**：记住「**ControlNet 用参考图的结构（姿态/深度/边缘）当额外条件，提示词管外观**」。
> 它的神经网络训练原理完全跳过，当黑盒用。
> **和已有认知的差异**：普通条件（提示词）是「语义层」的引导；ControlNet 是「几何/结构层」的引导——
> 相当于给 diffusion 加了一条新的输入通道。这是「多条件融合」思想，和 ch06 的 conditioning 是一路的，只是多了一路。

---

<a id="c13-02"></a>

### 13.2 预处理器：提取骨架/深度/边缘

**概念定义**：参考图是普通彩色照片，模型看不懂「姿态」「深度」这些结构。
**预处理器（Preprocessor）**负责把参考图**转换成**对应的结构图：
- OpenPose 预处理器：照片 → 火柴人骨架图
- Depth 预处理器：照片 → 深度图（近亮远暗的灰度）
- Canny 预处理器：照片 → 边缘轮廓线图

处理后的结构图再喂给 ControlNet 模型。

**直觉类比**：像**把照片翻译成建筑图纸**——
你给的是一张成品照片（参考图），预处理器把它「翻译」成骨架图/深度图/线稿（图纸），
ControlNet 拿着图纸要求模型「按这个结构盖」。

**界面 / 参数**：两类节点配合——
1. **预处理器节点**（如 `OpenPose Preprocessor` / `Depth Preprocessor` / `Canny Edge`）：
   输入参考图 IMAGE，输出处理好的结构图 IMAGE。控件可调灵敏度/阈值。
2. **ControlNet 模型加载**：`ControlNetLoader` 选对应的 ControlNet 模型文件（如 `control_v11p_sd15_openpose`）
   ——**预处理器类型要和 ControlNet 模型类型匹配**（姿态图配 openpose 模型，深度图配 depth 模型）。

预处理器有的 ComfyUI 内置，有的来自自定义节点包（如 ControlNet Auxiliary，见 [ch24](../../06_ecosystem/docs/ch24_manager.md)）。

**常见误区**：
- ❌「预处理器和 ControlNet 模型随便配」—— 不行。姿态图必须配 openpose 模型，错配等于让模型看不懂的图，控制失效。
- ❌「参考图必须和出图同款」—— 不用，只要结构（姿势/构图）是你想要的，风格内容由提示词定。
- ❌「预处理结果不用看」—— 建议预览一下预处理图，确认骨架/边缘提取正确，否则控制会跑偏。

> **够用边界**：知道「预处理器把参考图转成结构图，类型要和 ControlNet 模型匹配」即可。
> 各预处理算法的参数细节用到再查。
> **和已有认知的差异**：这是**两条独立的模型链**——预处理器（通常是传统 CV 或小模型）只做「提取结构」，
> ControlNet（神经网络）负责「把结构融入生成」。新手容易混成一个东西，其实是接力关系。

---

<a id="c13-03"></a>

### 13.3 连线与 ControlNet Apply

**概念定义**：把 ControlNet 接入主工作流，核心是 `Apply ControlNet`（或 `ControlNetApplyAdvanced`）节点——
它把「提示词 conditioning」和「ControlNet 结构条件」**合并成一路新的 conditioning**，再送进 KSampler。

**直觉类比**：像**把两张订单合成一张交给厨师**——
一张订单写「做什么菜」（提示词 conditioning），一张写「必须摆成这个造型」（ControlNet 结构）。
`Apply ControlNet` 就是把两张订合并成一张完整的，厨师（KSampler）照着执行。

**界面 / 参数**：接线骨架（在文生图基础上加 ControlNet 分支）——
```
【ControlNet 分支】
Load Image(参考图) → 预处理器 → 结构图 IMAGE → Apply ControlNet(image)
ControlNetLoader → CONTROL_NET → Apply ControlNet(control_net)

【合流进主链】
CLIP Text Encode(正向 conditioning) → Apply ControlNet(positive)
Apply ControlNet(CONDITIONING) → KSampler(positive)     ← 替换原来的正向 conditioning

【其余不变】
KSampler(negative) 仍接负向 CLIP Text Encode
MODEL / latent_image / VAE Decode 照旧
```
Advanced 版本还能分别控制正/负向 conditioning、设 strength/起止步数。

**常见误区**：
- ❌「ControlNet 接到 image 输入口（KSampler 没有 image 口）」—— 不。ControlNet 是通过**合并 conditioning** 起作用的，不是直接喂图给 KSampler。
- ❌「正向 conditioning 忘了替换」—— 要让 Apply ControlNet 的输出接 KSampler 的 positive，否则控制不生效。
- ❌「只加 ControlNetLoader 不做预处理」—— 要有参考图→预处理→结构图这一步，否则没有结构信息。

> **够用边界**：会照骨架接出一条 OpenPose ControlNet、让控制生效就够了。
> Advanced 节点的双 conditioning 等进阶用法按需再学。
> **和已有认知的差异**：这是第一次出现「两路条件合并」——ch06 只有提示词一路 conditioning，
> 这里多一路结构。理解 `Apply ControlNet` 是「conditioning 的合并器」，整个结构就清晰了。

---

<a id="c13-04"></a>

### 13.4 strength / start / end 怎么调

**概念定义**：`Apply ControlNet`（尤其 Advanced 版）有三个关键旋钮：
- **strength（控制强度）**：0~1，ControlNet 管得多紧。越高越严格贴合参考结构，越低越自由。
- **start（开始步数）**：从第几步开始生效
- **end（结束步数）**：到第几步为止生效

**直觉类比**：像**临摹时的"照着程度"和"时间"**——
- strength = 你多严格照着线稿（1=一笔画都不能偏，0.5=大致参考）
- start/end = 你在作画的哪个阶段参考线稿（一开始就用 vs 快画完才用）

**界面 / 参数**：经验值——
| 参数 | 常用值 | 说明 |
|---|---|---|
| strength | 0.8~1.0 | 姿态/边缘控制通常要强；想自由点调低 |
| start | 0 | 从头就控制，最常见 |
| end | 1.0（或 steps）| 全程控制；调低可让后半程自由发挥细节 |

调参思路：
- 控制不明显 → 调高 strength
- 构图太死板、细节僵 → 略降 strength，或让 end 早一点结束（后半程自由补细节）
- 只在特定阶段要结构 → 用 start/end 限定

**常见误区**：
- ❌「strength 越高越好」—— 太高（接近 1）可能让画面僵硬、提示词影响被压过。0.8~1.0 通常是甜区。
- ❌「start/end 是像素尺寸」—— 不是，是**采样步数比例**（0~1，对应 steps 的进度）。
- ❌「end 设很小能省时间」—— 不影响速度，只影响控制生效的时段。

> **够用边界**：记住「strength 控制贴合度（0.8~1 起步）、start 0 / end 1 是默认全程控制」。
> start/end 的数学（在去噪第几步注入控制）跳过。
> **和已有认知的差异**：这些是**过程性参数**——它们不控制"生成什么"，而是控制"在生成的哪个阶段、以多大力气施加约束"。
> 这是 diffusion 迭代特性带来的独特旋钮，一次成型的模型没有这种概念。

---

## 小结

- ControlNet = 用参考图的结构（姿态/深度/边缘）当额外条件，提示词仍管外观内容。
- 预处理器把参考图转成结构图，类型必须和 ControlNet 模型匹配（openpose 图配 openpose 模型）。
- `Apply ControlNet` 把提示词 conditioning 和结构条件**合并**，输出接 KSampler 的 positive。
- strength 管贴合度（0.8~1 起步），start/end 管生效时段（默认 0~1 全程）。

## 实操与下一步

- 用 OpenPose 控制人物姿态：[`ch13_task.md`](../tasks/ch13_task.md)
- 下一章：[第 14 章 参考图与一致性](ch14_reference.md)
