# 第 3 章 第一个工作流：文生图（First Workflow: Text-to-Image）

> 前置：[ch02 安装](ch02_installation.md)（ComfyUI 已能打开、已放入 checkpoint） ｜ 对应实操：[`ch03_task.md`](../tasks/ch03_task.md)
> 状态：`[已完成]` ｜ 所属篇：`00_getting_started/`

**一句话**：从空画布亲手加 **6 类 7 个节点**、按颜色连起来，点一下 Queue Prompt，
你就出出了第一张 AI 图——这一步走通，后面所有工作流都是它的变体。

> 本篇一条线：[ch01 是什么](ch01_what_is_comfyui.md) → [ch02 安装](ch02_installation.md) → [ch03 第一条工作流](ch03_first_workflow.md)。
> 这是入门篇的收口：前面准备的都在这里兑现。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [从空画布开始（Blank Canvas）](#c03-01) | 3.1 |
| [逐个加节点并连线（Add & Connect Nodes）](#c03-02) | 3.2 |
| [放入模型并出图（Load Model & Generate）](#c03-03) | 3.3 |
| [保存、加载与导出（Save / Load / Export）](#c03-04) | 3.4 |

---

<a id="c03-01"></a>

### 3.1 从空画布开始

**概念定义**：画布（Canvas）就是你搭工作流的桌面。ComfyUI 默认会加载一张预置的文生图工作流，
但我们要**从空画布自己搭一遍**——只有亲手连过，才知道每条线在传什么。

**直觉类比**：像先把桌子擦干净，再一样样摆上食材。别人摆好的成品看着好，但你不知道盐放哪了。

**界面 / 参数**：新建空画布——
- 点左上角 **ComfyUI 图标（Menu）→ New**，画布清空
- 或者工作流标签页旁边的 **+** 号，新建一张空白工作流

认识三种添加节点的方式（后面会混着用）：
1. **右键菜单**：画布空白处右键 → `Add Node` → 按分类找
2. **节点库搜索**：按 `N` 键（或点左侧 Nodes）打开节点库，搜名字，点一下加到画布
3. **拖线生成**：从某个输出圆点拖到空白处松开，直接搜节点并自动连上

**常见误区**：
- ❌「必须从预置工作流改」—— 不用。从空画布搭一遍最有价值，虽然慢一点。
- ❌「画布上的节点被我拖乱了，坏了」—— 随便拖，布局不影响功能；滚轮缩放、`Shift + 拖空白` 平移视野。

> **够用边界**：会「新建空画布 + 用 `N` 搜节点加进来」就够了。
> 三种加节点方式不用全记，先熟练第二种（搜索）。
> **和已有认知的差异**：画布是一张**有向图**的节点编辑器，和 Blender 的节点编辑器、Unreal 蓝图是同一类东西。
> 如果你见过它们，这里的交互会很熟悉。

---

<a id="c03-02"></a>

### 3.2 逐个加节点并连线

**概念定义**：文生图工作流由 **6 类 7 个节点**组成。先记住这张「零件清单」，再按连线图拼起来。

**直觉类比**：像照着菜谱摆产线——先认清每样工具，再按流程把传送带接上。

**界面 / 参数**：零件清单（节点名 + 作用 + 在菜单哪找）——

| 节点 | 作用 | 加节点菜单路径 |
|---|---|---|
| `Load Checkpoint` | 加载模型，吐出 MODEL / CLIP / VAE 三样 | `model > loaders > Load Checkpoint` |
| `CLIP Text Encode (Prompt)` ×2 | 把提示词变成条件（一个正向、一个负向）| `model > conditioning` |
| `Empty Latent Image` | 造一张指定尺寸的「空白底」（潜空间）| `model > latent` |
| `KSampler` | 核心：用模型和提示词把空白底去噪成图 | `model > sampling` |
| `VAE Decode` | 把 KSampler 的结果从潜空间解码成能看的图 | `model > latent` |
| `Save Image` | 显示并保存图片到 `output\` | `image` |

**连线图**（这是全篇最重要的一张图，照着连）：

```
Load Checkpoint
  ├─ MODEL ───────────────────────────────→ KSampler(model)
  ├─ CLIP ──→ CLIP Text Encode (正向) ──→ KSampler(positive)
  ├─ CLIP ──→ CLIP Text Encode (负向) ──→ KSampler(negative)
  └─ VAE ─────────────────────────────────→ VAE Decode(vae)

Empty Latent Image ──────────────────────→ KSampler(latent_image)

KSampler(latent) ────────────────────────→ VAE Decode(samples)
VAE Decode(IMAGE) ───────────────────────→ Save Image(images)
```

**连线的三条硬规则**（记牢，能避开绝大多数困惑）：
1. **一个输出可以接多个输入**（所以 CLIP 能同时喂给正、负两个编码器）。
2. **一个输入只能接一根线**（新线会顶掉旧线）。
3. **只能同类型相连**——颜色会提示你：蓝=MODEL、绿=CONDITIONING、橙=LATENT、紫=IMAGE、黄=CLIP/VAE。
   拖线时颜色不对就接不上，这是 ComfyUI 帮你防错。

**常见误区**：
- ❌「正向和负向提示词接反了」—— 正向（想要什么）接 `positive`，负向（不想要什么）接 `negative`，别接反。
- ❌「VAE 忘了连，图发绿/发灰」—— `VAE Decode` 的 `vae` 输入要接 `Load Checkpoint` 的 VAE 输出；漏了会出异常颜色的图。
- ❌「线太多看不清」—— 用 `Reroute` 节点分线、把节点拖开，第 16 章会专门讲整理技巧。

> **够用边界**：这一节能照着连线图连对、知道三条连线规则，就够了。
> 每条线传的是什么数据类型，第 4 章细讲；CLIP / VAE 是什么，第 5~7 章讲。
> 现在**先连出来、跑通**，不求全懂。
> **和已有认知的差异**：这和你写函数传参不同——这里连线的**类型检查是强制的**（颜色不匹配接不上），
> 相当于编译器在帮你检查类型，非常适合新手防错。

---

<a id="c03-03"></a>

### 3.3 放入模型并出图（Load Model & Generate）

**概念定义**：节点连好后，填提示词、选模型、点执行，工作流就从右往左跑一遍，产出图片。

**直觉类比**：产线搭好了，现在按下启动按钮，等它把产品做出来。

**界面 / 参数**：按顺序做——

1. **选模型**：`Load Checkpoint` 节点里，`ckpt_name` 下拉选你放进 `models\checkpoints\` 的模型（ch02 已放好）
2. **填提示词**：
   - 正向 `CLIP Text Encode`：`a cute cat sitting on a windowsill, sunlight, high detail`
   - 负向 `CLIP Text Encode`：`blurry, low quality, watermark, extra limbs`
3. **设空白底**：`Empty Latent Image` 里 `width=512, height=512, batch_size=1`
4. **设采样器**：`KSampler` 保持默认即可（`steps=20, cfg=8, sampler=euler, scheduler=normal, denoise=1`），
   seed 先用默认（参数含义第 8 章讲，现在照抄）
5. **执行**：点右上角 **Queue Prompt** 按钮
6. **看结果**：画布上节点边框会跑马灯式闪动表示在执行；跑完在 `Save Image` 节点看到图，
   文件也在 `output\` 目录里

**验收信号**：`Save Image` 显示出一张 512×512 的猫图 → 成功。

**常见误区**：
- ❌「点 Queue Prompt 没反应」—— 检查有没有红色报错节点；或某节点输入没接全（缺输入会飘红）。
- ❌「出图很慢」—— 第一次会慢（加载模型），之后快；512×512 + 20 步是比较轻的配置。
- ❌「出图是噪声/全黑」—— 多半 VAE 没接对，或模型文件损坏。见 [附录 C](../../90_appendix/docs/appC_troubleshooting.md)。

> **够用边界**：能填提示词、选模型、点 Queue Prompt 出图，入门目标就达成了。
> `KSampler` 那些参数到底怎么调，第 8 章专门讲；现在照抄默认值。
> **和已有认知的差异**：点一次 Queue Prompt = 把整张图**重新执行一遍**（不是只改动的节点）。
> 想只算某个分支，要用 Mute/Bypass 或工具节点，第 16 章讲。

---

<a id="c03-04"></a>

### 3.4 保存、加载与导出（Save / Load / Export）

**概念定义**：工作流是**可以存成文件的**——这就是 ComfyUI 的「可复现」核心。
一个 JSON 文件记录了所有节点、连线、参数，发给别人加载就能出一样的图。

**直觉类比**：工作流 JSON = 一张**写满配方的卡片**。存下来，下次照着做，或者抄给别人。

**界面 / 参数**：三种操作要分清——

| 操作 | 得到什么 | 用途 |
|---|---|---|
| **Save**（保存工作流）| UI 格式 JSON | 自己下次打开接着改，保留节点位置/布局 |
| **Load**（加载）| 恢复一张存好的工作流 | 接着上次做 |
| **Export (API Format)** | API 格式 JSON | 给程序调用 / 批量出图用（[ch25](../../06_ecosystem/docs/ch25_api_automation.md)）|

- 入口：Menu（左上角图标）里有 `Save` / `Load` / `Export`
- 新版本里工作流默认会存到 `workflows\` 目录
- **导出 API 格式前**，需要在设置里开启 `Enable Dev mode Options`，才能看到 `Export (API Format)`

**常见误区**：
- ❌「Save 和 Export 是一回事」—— 不是。Save 是 UI 格式（带布局，给人看、接着改），
  Export API 是 API 格式（扁平、给程序读），两者**不能互换**。第 25 章细讲。
- ❌「导出的 JSON 里没保存模型文件」—— JSON 只记模型**文件名**，不打包模型本体。
  别人加载后要有同名的模型才能出图，见 [ch18](../../04_models_and_lora/docs/ch18_model_files.md)。

> **够用边界**：会 Save / Load（UI 格式）就够日常用；API 格式知道「是给程序用的」即可，第 7 篇再碰。
> **和已有认知的差异**：UI 格式 JSON 里带坐标、尺寸、颜色这些**纯界面信息**，
> 因为它要还原你看到的画布；API 格式把这些全去掉，只留「算什么」。这是两种完全不同的序列化目标。

---

## 小结

- 文生图 = 6 类 7 个节点：`Load Checkpoint` + 2×`CLIP Text Encode` + `Empty Latent Image` + `KSampler` + `VAE Decode` + `Save Image`。
- 照连线图连：同类型相连（看颜色），一输出可接多输入，一输入只接一根线。
- 填词选模型点 Queue Prompt 出图；Save/Load 存 UI 格式，API 格式留给程序。

## 实操与下一步

- 亲手搭出并出图：[`ch03_task.md`](../tasks/ch03_task.md)
- **入门篇完成**！下一站：[第 2 篇 核心节点 · ch04 心智模型](../../01_core_nodes/docs/ch04_mental_model.md)，
  把每条线「为什么」搞懂。
