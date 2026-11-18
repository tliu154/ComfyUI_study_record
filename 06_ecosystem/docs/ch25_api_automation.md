---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/接口"
  - "#source/官方文档"
created: 2026-11-18
---
# 第 25 章 API 与自动化（API & Automation）

> 前置：[ch03 第一个工作流](../../00_getting_started/docs/ch03_first_workflow.md)（导出 JSON）· [ch24 Manager](ch24_manager.md) ｜ 对应实操：[`ch25_task.md`](../tasks/ch25_task.md)
> 状态：`[已完成]` ｜ 所属篇：`06_ecosystem/` ｜ 难度：`[选读]`

**一句话**：手动在画布上点「Queue Prompt」，本质是往 ComfyUI 的后端发了一个**任务描述（JSON）**；
API 就是把这一步用脚本代替——于是你能批量出图、改参数、接入自己的程序，
把「人肉点按钮」变成「程序自动跑」。

> 本篇一条线：[ch24 Manager](ch24_manager.md) → [ch25 API](ch25_api_automation.md) → [ch26 性能](ch26_performance.md)。
> 本章 `[选读]`：偏工程向，不写代码也要知道「两种 JSON 格式」的区别，能读懂别人的脚本。

## 本章子概念索引

| 概念 | 小节 |
|---|---|
| [两种 JSON 格式（UI vs API）](#c25-01) | 25.1 |
| [导出 API 格式工作流](#c25-02) | 25.2 |
| [用脚本提交任务（概念）](#c25-03) | 25.3 |
| [云端 Router 与 CLI](#c25-04) | 25.4 |

---

<a id="c25-01"></a>

### 25.1 两种 JSON 格式（UI Format vs API Format）

**概念定义**：同样一条工作流，能导出成两种 JSON——
- **UI 格式（工作流文件）**：记录画布上每个节点的**位置、尺寸、连线、控件值**，给 ComfyUI 界面「恢复现场」用。你平时保存的 `.json` 就是这种。
- **API 格式（Prompt 格式）**：只记录「要执行什么」——每个节点 id 及其输入参数，结构是 `{ "节点id": { "class_type": ..., "inputs": {...} } }`，直接发给 `/prompt` 接口执行。

**直觉类比**：
UI 格式像**一张设计图纸**——标了每个零件画在纸的哪个位置、长什么样、怎么连，给人看的；
API 格式像**一张施工单**——只写「用什么型号、装在哪、参数多少」，给机器执行用的。
同一条流，图纸（UI）能让人接着改，施工单（API）能让机器直接开工。

**界面 / 参数**：API 格式最小结构长这样（概念示意）——
```json
{
  "3": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 42,
      "steps": 20,
      "cfg": 8,
      "sampler_name": "euler",
      "scheduler": "normal",
      "model": ["4", 0],
      "positive": ["6", 0],
      "negative": ["7", 0],
      "latent_image": ["5", 0]
    }
  }
}
```
- `class_type`：节点类型名（对应画布上的节点）
- `inputs`：输入参数；值若写成 `["节点id", 输出槽]`，表示「这个输入来自另一个节点的输出」，即连线

**常见误区**：
- ❌「两种格式能互换着用」—— 不能。UI 格式直接发给 `/prompt` 会报错；API 格式拖进画布也不还原布局。
- ❌「API 格式里也有节点坐标」—— 没有。API 格式**不关心画布长什么样**，只关心执行逻辑。
- ❌「改了画布就要重新导出「两种」」—— 是的，改完工作流要重新导出 API 格式，旧的会过期。

> **够用边界**：记住「UI 格式给人看（带布局），API 格式给机器跑（只含参数+连线），两者不通用」即可。
> 具体字段含义看一眼就懂，不用背。
> **和已有认知的差异**：你之前保存工作流是「为了下次打开接着改」（UI 格式）；
> 自动化场景保存工作流是「为了发给程序执行」（API 格式）——**目的不同，格式就不同**。

---

<a id="c25-02"></a>

### 25.2 导出 API 格式工作流（Export API Format）

**概念定义**：默认是 UI 格式；要拿到 API 格式，需要在设置里打开「启用开发者模式」，
工作流菜单才会多出「Export (API)」选项。

**直觉类比**：像**打开手机的「开发者选项」**——
平时藏起来（因为普通用户用不到），开启后多出一些高级按钮。
API 格式导出就是这种「高级按钮」，默认隐藏，打开开发者模式才出现。

**界面 / 参数**：操作步骤——
1. `Settings`（齿轮）→ 找到 **Enable Dev mode Options**（启用开发者模式）→ 勾选
2. 回到工作流菜单，出现 **Export (API)** / `Save (API Format)` 选项
3. 点它，导出 `.json`（这类文件通常就是 API 格式）
4. 对照检查：用文本编辑器打开，看到的结构应是 `{"节点id": {"class_type": ..., "inputs": {...}}}`

**常见误区**：
- ❌「导出按钮和平时保存是同一个」—— 不是。默认 `Save` 是 UI 格式；API 要单独点 `Export (API)`。
- ❌「开了开发者模式会变慢/危险」—— 不会，只是多显示几个菜单项。
- ❌「API 文件能在画布里打开编辑」—— 不能当正常工作流用；它是给脚本/接口读的。

> **够用边界**：会「开开发者模式 → 导出 API 格式 → 认出它的结构」就够。
> **和已有认知的差异**：这是 ComfyUI 里少数「需要先进设置解锁」的功能——
> 因为官方默认你只是画画，不搞自动化。想要程序化，就自己把开关打开。

---

<a id="c25-03"></a>

### 25.3 用脚本提交任务（概念，Concept）

**概念定义**：ComfyUI 后端提供 HTTP 接口。最常用的是
`POST /prompt`：把 API 格式 JSON 作为 `prompt` 字段发过去，后端就把它排进队列执行；
还有 `/queue`（看队列状态）、`/history`（取结果）、`/upload/image`（传图）等。
你不需要懂 Web 开发，知道「有个地址能收任务、发过去就出图」即可。

**直觉类比**：像**餐厅点单**——
`/prompt` 是下单窗口：把点单（JSON）递进去；厨房（后端）按顺序做；
`/queue` 是「看还剩几单没做」，`/history` 是「取做好的菜」。
你写脚本，就是当那个自动下单的顾客，可以一口气下 100 单、每单换个要求。

**界面 / 参数**：核心流程（概念示意，Python 用 `requests`）——
```python
import requests, json, copy

prompt = json.load(open("workflow_api.json"))   # 读 API 格式工作流
for seed in range(10):
    p = copy.deepcopy(prompt)
    p["3"]["inputs"]["seed"] = seed             # 改 KSampler 的 seed（节点 id 按你自己的工作流）
    r = requests.post("http://127.0.0.1:8188/prompt", json={"prompt": p})
    # 返回 {"prompt_id": "..."} 表示提交成功，结果按 id 去 /history 取
```
- 关键点：**先找到「seed 在哪个节点 id」**（导出后看 JSON 里 `class_type` 是 `KSampler` 的那条）
- 改哪个参数就改对应节点的 `inputs` 字段；`["节点id", 槽]` 形式的连线一般不用动
- 出图结果默认存到 ComfyUI 的 `output/` 目录

**常见误区**：
- ❌「用 UI 格式 JSON 发 /prompt」—— 报错。必须是 API 格式（见 25.1）。
- ❌「脚本里节点 id 照抄教程」—— 不行。节点 id 是你自己那条工作流里的编号，要按自己的 JSON 找。
- ❌「发完就能立刻在返回里拿到图片」—— `/prompt` 只返回 `prompt_id`，图片要另去 `/history` 或 `output/` 取。

> **够用边界**：知道「`/prompt` 收 API 格式 JSON、改 `inputs` 里的值就能批量改参数、
> 结果在 `output/`」就够。异步取结果、WebSocket 监听进度等进阶用法用到再查。
> **和已有认知的差异**：手动出图时你改的是**界面上的框**；
> 脚本出图时你改的是 **JSON 里某个节点的 `inputs` 字段**——同一件事的两种操作方式。

---

<a id="c25-04"></a>

### 25.4 云端 Router 与 CLI（Cloud Router & CLI）

**概念定义**：除了自己机器上的 `localhost:8188`，ComfyUI 还有两条「工程化」路线——
- **Comfy CLI（`comfy`）**：官方命令行工具，管安装、启动、装节点、跑工作流，把前面手动做的事命令化
- **Comfy Cloud / API 节点**：官方云端服务，把工作流当 API 调用，本地没显卡也能跑（通常按量计费）

**直觉类比**：前面三节像**自己厨房做菜**（本地 ComfyUI）；
CLI 像**给厨房装了个语音/遥控器**（命令行一句话搞定，方便写进自动化脚本）；
Cloud 像**直接叫外卖**（不用自己有厨房，但要花钱、依赖网络）。

**界面 / 参数**：常见用途——
```
comfy-cli 常用：
  comfy launch              # 启动
  comfy node install XXX    # 装节点包（ch24 的安装方式之一）
  comfy model install XXX   # 装模型
  交付脚本里调 comfy run ... 跑工作流

云端路线：
  Comfy Cloud 网页版直接跑（零安装，见 ch02）
  平台提供的 API 端点：把工作流 JSON 发到云端执行（按量计费）
```
- comfy-cli 的安装见 [ch02](../../00_getting_started/docs/ch02_installation.md)，本章不重复

**常见误区**：
- ❌「CLI 是另一套 ComfyUI」—— 不是。它只是**管理/调用**同一个 ComfyUI 的工具。
- ❌「云端一定比本地好」—— 云端省显卡但花钱、依赖网、数据要上传；本地免费可控但要硬件。
- ❌「API 格式只在本地有用」—— 云端调用通常也用同一套 API 格式工作流，学一次两边通用。

> **够用边界**：知道「CLI 把安装/启动/跑流命令化，Cloud 把工作流当在线 API，二者都用 API 格式」即可。
> 云端计费、CLI 全部子命令查文档要用时再看。
> **和已有认知的差异**：到这里 ComfyUI 已经不只是「一个画图软件」——
> 它是**能被脚本和云端调用的图像生成服务**。这是从「工具」到「平台」的认知升级。

---

## 小结

- 两种 JSON：UI 格式带布局给人看（平时保存的），API 格式只含参数+连线给机器跑，二者不通用。
- 导出 API 格式：先开 `Enable Dev mode Options`，再用 `Export (API)`；认出 `{"id": {"class_type", "inputs"}}` 结构。
- 脚本提交：把 API 格式 POST 到 `/prompt`，改节点 `inputs`（如 seed）即可批量出图；节点 id 按自己工作流找，结果在 `output/`。
- CLI 命令化管理、Cloud 把工作流当在线 API，都复用 API 格式——ComfyUI 从工具变成可编程平台。

## 实操与下一步

- 导出 API 格式、用脚本改 seed 批量提交：[`ch25_task.md`](../tasks/ch25_task.md)
- 下一章：[第 26 章 性能与显存优化](ch26_performance.md)（选读）
