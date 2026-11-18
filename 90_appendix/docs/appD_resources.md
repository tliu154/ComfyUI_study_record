---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/资源"
  - "#source/官方文档"
created: 2026-11-18
---
# 附录 D 资源与社区（Resources）

> 前置：无 ｜ 状态：`[已完成]` ｜ 所属：`90_appendix/`

**一句话**：把学 ComfyUI 用得上的**官方入口、模型站、社区、节点仓库**分类列出来，
需要找东西时来这里挑入口。这里只给**稳定的站点首页/主仓库**，不写易失效的深层链接；
具体资源迭代快，以站点当下内容为准。

> 说明：本仓库**不托管任何大模型/视频文件**（见 [.gitignore](../../.gitignore)），只记路径与来源。
> 下载模型请到正规来源、注意许可与商用条款（[ch17 17.4](../../04_models_and_lora/docs/ch17_model_families.md#c17-04)）。

## 目录

| 类别 | 用途 |
|---|---|
| [D.1 官方入口](#appD-01) | 文档、GitHub、Comfy Cloud |
| [D.2 模型下载站](#appD-02) | checkpoint / LoRA / 放大模型 |
| [D.3 工作流与社区](#appD-03) | 现成工作流、教程、问答 |
| [D.4 自定义节点仓库](#appD-04) | Manager 之外的节点生态 |
| [D.5 本项目参考来源](#appD-05) | 本笔记依据与延伸 |

---

<a id="appD-01"></a>

### D.1 官方入口（Official）

| 资源 | 地址 | 用途 |
|---|---|---|
| ComfyUI 官网 | https://www.comfy.org/ | 产品、云版、动态 |
| ComfyUI GitHub | https://github.com/comfyanonymous/ComfyUI | 源码、安装说明、更新日志（[ch02](../../00_getting_started/docs/ch02_installation.md)）|
| 官方文档 | https://docs.comfy.org/ | 官方教程与概念说明 |
| Comfy Cloud | https://www.comfy.org/cloud | 零安装云端运行（[ch02](../../00_getting_started/docs/ch02_installation.md)）|
| Comfy Registry | https://www.comfy.org/registry | 自定义节点/模型的官方登记处（[ch24](../../06_ecosystem/docs/ch24_manager.md)）|

---

<a id="appD-02"></a>

### D.2 模型下载站（Model Sources）

| 站点 | 地址 | 主要下什么 |
|---|---|---|
| Hugging Face | https://huggingface.co/ | 最大的模型/数据集社区，SD/FLUX/Wan 各版本基本都在这 |
| Civitai | https://civitai.com/ | SD 系 checkpoint / LoRA 丰富，带预览图与评测 |
| ModelScope（魔搭） | https://www.modelscope.cn/ | 国内访问快，国产模型（含 Z-Image、Wan 等）多 |

**选模型注意**（详见 [ch17](../../04_models_and_lora/docs/ch17_model_families.md) / [ch18](../../04_models_and_lora/docs/ch18_model_files.md)）：
- 认准**架构**（SD1.5 / SDXL / FLUX），别下错
- 看**精度版本**（fp16 / fp8 / gguf），按显存选（[ch26](../../06_ecosystem/docs/ch26_performance.md)）
- 看**许可**（License），商用前务必确认

---

<a id="appD-03"></a>

### D.3 工作流与社区（Community）

| 类型 | 去处 | 用途 |
|---|---|---|
| 官方示例工作流 | ComfyUI 界面 `Workflow > Browse Templates`；官方文档 examples | 学各种模型的标准搭法（[ch20](../../04_models_and_lora/docs/ch20_workflow_variants.md)）|
| OpenArt | https://openart.ai/workflows | 大量现成工作流可导入 |
| Reddit | https://www.reddit.com/r/comfyui/ | 问答、经验、新模型讨论 |
| GitHub Issues / Discussions | ComfyUI 及各节点仓库的 Issues | 报错时搜/问（配合 [附录 C](appC_troubleshooting.md)）|
| 中文社区 | B 站搜「ComfyUI 教程」、各 AI 绘画社群 | 视频教程、国内玩法 |

---

<a id="appD-04"></a>

### D.4 自定义节点仓库（Custom Nodes）

大多数节点通过 [ch24 Manager](../../06_ecosystem/docs/ch24_manager.md) 搜索安装即可，
以下是常见节点生态的**主仓库/组织入口**（装法见 Manager，别手动乱 clone）：

| 生态 | 去处 | 相关章节 |
|---|---|---|
| ComfyUI-Manager | https://github.com/ltdrdata/ComfyUI-Manager | [ch24](../../06_ecosystem/docs/ch24_manager.md) |
| 官方控制节点 | ComfyUI 内置 + 官方文档 | [ch13](../../03_control_and_refine/docs/ch13_controlnet.md) |
| ControlNet 辅助节点 | github.com/comfyanonymous/ComfyUI_controlnet_aux | 预处理器（[ch13](../../03_control_and_refine/docs/ch13_controlnet.md)）|
| IP-Adapter 节点 | ComfyUI_IPAdapter_plus（GitHub 搜索） | [ch14](../../03_control_and_refine/docs/ch14_reference.md) |
| AnimateDiff / 视频节点 | ComfyUI-AnimateDiff-Evolved 等（GitHub 搜索） | [ch21](../../05_video_and_advanced/docs/ch21_video_basics.md) |
| Comfy Registry | https://www.comfy.org/registry | 搜节点包（[ch24](../../06_ecosystem/docs/ch24_manager.md)）|

> 装节点包 = 运行别人的代码，注意来源可信（[ch24 24.4](../../06_ecosystem/docs/ch24_manager.md#c24-04)）。

---

<a id="appD-05"></a>

### D.5 本项目参考来源（This Repo）

本笔记的知识主要来自：
- **ComfyUI 官方文档与 GitHub**：概念、节点、安装（D.1）
- **各模型/节点官方仓库与文档**：模型特性、节点用法（D.2 / D.4）
- **社区教程与经验**：工作流套路、调参技巧（D.3）

**本项目本身**：
- 大纲与状态：[SYLLABUS.md](../../SYLLABUS.md)
- GitHub：https://github.com/tliu154/ComfyUI_study_record
- 写作规范：[CONTRIBUTING.md](../../CONTRIBUTING.md) ｜ 术语：[NOTATION.md](../../NOTATION.md)

> 资源链接会随时间变化，发现失效可按名称到对应站点搜索最新版本，或提 issue 反馈。

---

## 小结

- 找**官方信息**去 comfy.org / docs.comfy.org / GitHub；找**模型**去 Hugging Face / Civitai / ModelScope；找**节点**用 Manager 或 Comfy Registry。
- 下载模型认准架构、精度、许可；装节点看来源。
- 本仓库不存大模型，只记路径与来源。

> 回 [附录首页](../README.md) ｜ 回 [仓库首页](../../README.md) ｜ 主线完整大纲 [SYLLABUS](../../SYLLABUS.md)
