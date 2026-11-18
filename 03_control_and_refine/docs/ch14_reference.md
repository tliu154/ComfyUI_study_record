---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/参考图"
  - "#source/官方文档"
created: 2026-11-18
---
# 第 14 章 参考图与一致性（IP-Adapter & Reference）

> 前置：[ch13 ControlNet](ch13_controlnet.md) ｜ 对应实操：[`ch14_task.md`](../tasks/ch14_task.md)
> 状态：`[已完成]` ｜ 所属篇：`03_control_and_refine/`

**一句话**：ControlNet 锁的是**姿态结构**，IP-Adapter 锁的是**长相/风格**——
给它一张参考图，它让生成的角色「还是那张脸/那个风格」，换场景、换动作也认得出来。

> 本篇一条线：[ch13 ControlNet](ch13_controlnet.md) → [ch14 参考图一致性](ch14_reference.md) → [ch15 提示词进阶](ch15_prompt_advanced.md)。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [一致性问题是什么](#c14-01) | 14.1 |
| [IP-Adapter 加载与接线](#c14-02) | 14.2 |
| [权重与风格/身份的取舍](#c14-03) | 14.3 |
| [和 ControlNet 怎么配合](#c14-04) | 14.4 |

---

<a id="c14-01"></a>

### 14.1 一致性问题是什么

**概念定义**：「一致性（Consistency）」指**同一个角色/风格在多张图里保持可辨认**。
普通文生图每次生成都是独立的，即使提示词写同一个人物描述，换 seed/场景后长相也完全不同——
因为模型没有「记住」参考图里那张脸长什么样。
参考图一致性技术就是把一张参考图的**身份特征或风格**注入生成，让新图保留它。

**直觉类比**：像**请一个演员拍不同戏**——
不用参考图：每次换导演换戏，演员都像换了个新人（长相随机）。
用参考图（IP-Adapter）：拿着演员的定妆照去拍新戏，无论什么场景，你都认得出是同一个人。

**界面 / 参数**：一致性常见需求——
- **角色一致性**：同一张脸，换发型/衣服/场景/动作
- **风格一致性**：同一画风，套用到新主体
- **产品/物体一致性**：同一个产品，换背景

实现路线：IP-Adapter（本章）、Reference-only、以及专门的身份 LoRA（[ch19](../../04_models_and_lora/docs/ch19_lora.md)）等。

**常见误区**：
- ❌「把参考图丢进 img2img 就能保持脸」—— img2img 改的是整张图（[ch09](../../02_image_workflow/docs/ch09_img2img.md)），
  换个场景时连背景一起带过去了，不是「提取身份再去新场景」。
- ❌「一致性靠提示词反复描述」—— 纯文字描述很难锁定长相细节，参考图技术更有效。

> **够用边界**：记住「一致性 = 参考图提供身份/风格，让新图还能认出是同一个」。
> **和已有认知的差异**：普通 conditioning 是「文字语义」；参考图一致性注入的是「图像特征」——
> 相当于多了一条「看图」的通道。和 ControlNet 一样是「加一路条件」，但 ControlNet 提取结构，IP-Adapter 提取外观特征，分工不同。

---

<a id="c14-02"></a>

### 14.2 IP-Adapter 加载与接线

**概念定义**：IP-Adapter 是一个通过**参考图**提供额外条件的模块。它有一个模型文件（ip-adapter），
配合一个「图像编码器」（CLIP Vision）把参考图编码成特征，再融入 conditioning。

**直觉类比**：像**给厨师看一张样板菜的照片**——
ControlNet 给的是「摆盘结构图」，IP-Adapter 给的是「这道菜长什么样/什么风格」的视觉样板。
厨师照着样板做出「神似」的新菜。

**界面 / 参数**：接线骨架（在文生图基础上加 IP-Adapter 分支）——
```
【IP-Adapter 分支】
Load Image(参考图) → IPAdapter(或 IPAdapterapply 节点 的 image 输入)
Load CLIP Vision 模型 → IPAdapter 的 clip_vision
IPAdapter Model Loader → IPAdapter 的 model
IPAdapter(IMAGE 特征) → 融入提示词 conditioning（节点输出 conditioning 给 KSampler）

【高级版】
IPAdapter Advanced 可分别设 positive/negative、权重、起止步数
```
IP-Adapter 及其节点通常来自自定义节点包（如 ComfyUI_IPAdapter_plus），装法见 [ch24](../../06_ecosystem/docs/ch24_manager.md)。
模型文件放 `models/ipadapter/`，CLIP Vision 放 `models/clip_vision/`，按 `R` 刷新。

**常见误区**：
- ❌「IP-Adapter 模型 = checkpoint」—— 不是，它是附加模块，要叠在普通 checkpoint 上用。
- ❌「忘了装 CLIP Vision」—— IP-Adapter 靠它编码参考图，缺了报错或无效。
- ❌「节点名对不上」—— IP-Adapter 有多个社区实现，节点名略有差异（IPAdapter / IPAdapterApply / IPAdapterAdvanced），按你装的包为准。

> **够用边界**：会照骨架接出一条 IP-Adapter、让生成图「像参考图」就够了。
> 内部注意力注入机制跳过。
> **和已有认知的差异**：这是「以图条件化（image conditioning）」——传统 conditioning 是文本，
> 这里直接把图像特征作为条件。这也是为什么它能锁住「只可意会」的长相和风格。

---

<a id="c14-03"></a>

### 14.3 权重与风格/身份的取舍

**概念定义**：IP-Adapter 的关键旋钮是**权重（weight）**——控制参考图影响多强。
不同模式侧重点不同：有的更保身份（脸），有的更保风格（画风）。

**直觉类比**：像**相似度滑块**——
权重高 = 越像参考图（连脸带风格都抄），权重低 = 只取一点意思、给提示词更多自由。
太高会「抄得太死」（新场景也带着参考图的背景/姿势），太低则「认不出来」。

**界面 / 参数**：调权经验——
| 目标 | weight 建议 | 说明 |
|---|---|---|
| 锁身份（同一张脸）| 0.6~0.9 | 换场景仍认得出 |
| 锁风格（同画风）| 0.4~0.7 | 让主体也能变 |
| 完全照搬 | 接近 1 | 可能连背景/构图都带过来 |

取舍：
- **身份 vs 自由**：权重越高越像参考图，但提示词改变构图/动作的能力越弱
- **风格 vs 内容**：有些模式（如 `style` 预设）偏风格，有些偏身份，按模式选

**常见误区**：
- ❌「权重一定要高」—— 太高会把参考图的背景/姿势也带进来，失去「换场景」的意义。
- ❌「IP-Adapter 能锁姿态」—— 那不是它的强项（它锁外观特征）；要锁姿态用 ControlNet（[ch13](ch13_controlnet.md)）。

> **够用边界**：记住「weight 0.6~0.9 锁身份、0.4~0.7 锁风格，太高会抄死」。
> 各模式的内部差异跳过，多用几次就有手感。
> **和已有认知的差异**：这是**连续可调的软约束**，不是「开/关」。像调音量的推子，不是一个开关——
> 需要你在「像不像」和「自由度」之间找平衡，这是经验活。

---

<a id="c14-04"></a>

### 14.4 和 ControlNet 怎么配合

**概念定义**：ControlNet 和 IP-Adapter 管的是**不同维度**，可以叠加使用：
- **ControlNet**：管**结构/几何**（姿态、深度、边缘）
- **IP-Adapter**：管**外观/身份**（长相、风格）

两者一起用 = 让「同一个人（IP-Adapter）摆出指定姿势（ControlNet）在新的场景里（提示词）」。

**直觉类比**：像**拍电影选角**——
- ControlNet = 分镜/走位脚本（站哪、什么姿势）
- IP-Adapter = 演员定妆照（长什么样）
- 提示词 = 剧本/场景说明（在什么环境、穿什么）
三者合起来，才能「同一个演员、按指定走位、在新场景」拍出来。

**界面 / 参数**：配合接线思路——
```
参考图A(姿态) → OpenPose 预处理 → Apply ControlNet → conditioning
参考图B(脸)   → IP-Adapter → conditioning
两路 conditioning 都汇入 KSampler 的 positive（或先合并）
提示词写场景/服装
```
注意两路条件都可能改 conditioning，接线顺序和节点实现有关，按实际节点调整。

**常见误区**：
- ❌「两者功能重复，二选一」—— 不重复，一个管结构一个管外观，是互补的。
- ❌「一起用会把画面搞得很僵」—— 权重调合适就不僵；各管一摊，反而更可控。
- ❌「身份一致性只能靠 IP-Adapter」—— 还有专门训练的身份 LoRA（[ch19](../../04_models_and_lora/docs/ch19_lora.md)），对特定人物效果更强，但要从头训练。

> **够用边界**：知道「ControlNet 管姿势、IP-Adapter 管长相、提示词管场景，能叠加」就够了。
> 多路 conditioning 的精确合并顺序按需查具体节点说明。
> **和已有认知的差异**：这是**多条件融合**的进阶形态——三种不同类型的信息（几何/外观/语义）
> 同时约束一个生成过程。理解每层「各管一摊」，就不会觉得节点多得无从下手。

---

## 小结

- 一致性 = 让新图还认得出是同一个人/风格；纯提示词难锁长相，靠参考图技术。
- IP-Adapter 用参考图提供外观特征（需配 CLIP Vision + ip-adapter 模型，来自自定义节点）。
- weight：0.6~0.9 锁身份、0.4~0.7 锁风格；太高会抄死参考图。
- 分工：ControlNet 管结构、IP-Adapter 管外观、提示词管场景，三者可叠加。

## 实操与下一步

- 用 IP-Adapter 固定一张脸换场景：[`ch14_task.md`](../tasks/ch14_task.md)
- 下一章：[第 15 章 提示词进阶](ch15_prompt_advanced.md)
