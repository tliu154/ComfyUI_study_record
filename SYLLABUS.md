# 教学大纲（Syllabus）· 完整骨架

**本文件是整个仓库唯一的章节清单与状态源。** 各篇 README 只写定位和实践方向，
章节增删、状态更新一律改这里，避免多处重复维护。

- 学习依赖顺序：**入门 → 核心节点 → 图像工作流 → 控制与精修 → 模型与 LoRA → 视频与进阶 → 生态与工程**
- 章号 01~26 保持稳定，作为跨文件引用的唯一标识；篇只是分组，不参与编号
- 每章只有真正开写时才建 `.md` 文件；本文件里的「文件」列是**预定路径**，不是现存文件
- 本仓库是 **Obsidian 库**：笔记一律 `.md`，frontmatter 不写 tags（tag 由自己手动加），章节之间用相对超链互引

状态：`[已完成]` 教学 + 实操 + 自测通过 ｜ `[部分完成]` 只有部分节 ｜
`[待写]` 仅规划 ｜ `[选读]` 低优先级，按需跳读

---

## 第 1 篇 入门 → `00_getting_started/`

前置：无。目标：从零装好 ComfyUI，亲手搭出第一条文生图工作流并跑通。

### 第 0 章 前言与使用说明（Preface） · [已落地]

> 不单独建章文件，拆到三处：[README.md](README.md)（定位/读者/路径图）、[CONTRIBUTING.md](CONTRIBUTING.md)（模板与规范）、[NOTATION.md](NOTATION.md)（术语与节点名约定）

**本章子概念索引：** 文档结构（Document Structure）· 学习路径（Learning Path）· 笔记模板（Note Template）· 术语约定（Terminology）

### 第 1 章 ComfyUI 是什么（What is ComfyUI） · [已完成]

> [教学](00_getting_started/docs/ch01_what_is_comfyui.md) · [实操](00_getting_started/tasks/ch01_task.md)

**本章子概念索引：** 节点式生成界面（Node-based Interface）· 与 WebUI 的区别（vs. Automatic1111）· 为什么学 ComfyUI（Why ComfyUI）· 适用人群与硬件门槛（Who & Hardware）

**节骨架：** 1.1 一句话认识 ComfyUI ｜ 1.2 节点式 vs 一条表单 ｜ 1.3 为什么值得学 ｜ 1.4 硬件与运行环境

### 第 2 章 安装与启动（Installation & Launch） · [已完成]

> [教学](00_getting_started/docs/ch02_installation.md) · [实操](00_getting_started/tasks/ch02_task.md)

**本章子概念索引：** 桌面版（Comfy Desktop）· Windows 便携包（Portable）· 源码安装（Manual / git）· 云端（Comfy Cloud）· comfy-cli · 首次启动与 `localhost:8188`

**节骨架：** 2.1 四种安装方式对比 ｜ 2.2 Windows 便携包实战 ｜ 2.3 comfy-cli 捷径 ｜ 2.4 云端零安装方案 ｜ 2.5 启动、更新与目录结构

### 第 3 章 第一个工作流：文生图（First Workflow: Text-to-Image） · [已完成]

> [教学](00_getting_started/docs/ch03_first_workflow.md) · [实操](00_getting_started/tasks/ch03_task.md)

**本章子概念索引：** 七个节点（Seven Nodes）· 连线规则（Links）· 加载 checkpoint ｜ 队列执行（Queue Prompt）· 保存与导出 JSON（Save / Export）

**节骨架：** 3.1 从空画布开始 ｜ 3.2 逐个加节点并连线 ｜ 3.3 放入模型并出图 ｜ 3.4 保存、加载与导出工作流

---

## 第 2 篇 核心节点 → `01_core_nodes/`

前置：第 1 篇。目标：把每条线的「为什么」搞懂，从照抄工作流变成能自己改。

### 第 4 章 工作流心智模型（Workflow Mental Model） · [待写]

> 文件：`01_core_nodes/docs/ch04_mental_model.md` ｜ 实操：`01_core_nodes/tasks/ch04_task.md`

**本章子概念索引：** 节点/输入/输出/控件（Node / Input / Output / Widget）· 数据类型与颜色（Data Types & Colors）· 有向图执行（DAG Execution）· 一输出多连接规则

**节骨架：** 4.1 节点的四个部件 ｜ 4.2 数据类型与颜色编码 ｜ 4.3 图是怎么被执行的 ｜ 4.4 连线的三条硬规则

### 第 5 章 加载器：模型从哪来（Loaders: Checkpoint / UNET / CLIP / VAE） · [待写]

> 文件：`01_core_nodes/docs/ch05_loaders.md` ｜ 实操：`01_core_nodes/tasks/ch05_task.md`

**本章子概念索引：** Load Checkpoint 三输出 ｜ UNET / Diffusion Model Loader ｜ CLIP / Text Encoder Loader ｜ VAE Loader ｜ 模型存放目录

**节骨架：** 5.1 Load Checkpoint：一体三输出 ｜ 5.2 拆分加载：UNET + CLIP + VAE ｜ 5.3 模型目录与刷新（R 键）｜ 5.4 该用哪种加载方式

### 第 6 章 提示词与条件（Prompt & Conditioning） · [待写]

> 文件：`01_core_nodes/docs/ch06_conditioning.md` ｜ 实操：`01_core_nodes/tasks/ch06_task.md`

**本章子概念索引：** CLIP Text Encode ｜ 正向/负向提示词（Positive / Negative）· Conditioning 数据类型 ｜ CLIP 双编码器（SDXL/FLUX 双 CLIP）

**节骨架：** 6.1 文字怎么变成模型能懂的条件 ｜ 6.2 正向与负向 ｜ 6.3 Conditioning 这条线 ｜ 6.4 双 CLIP 与 CLIP Text Encode (SDXL)

### 第 7 章 潜空间：图像在没解码前长什么样（Latent Space） · [待写]

> 文件：`01_core_nodes/docs/ch07_latent.md` ｜ 实操：`01_core_nodes/tasks/ch07_task.md`

**本章子概念索引：** 潜变量（Latent）· EmptyLatentImage ｜ VAE Encode / Decode ｜ 尺寸与显存的关系 ｜ 为什么不在像素空间生成

**节骨架：** 7.1 什么是潜空间（够用直觉）｜ 7.2 EmptyLatentImage：造一张空白底 ｜ 7.3 VAE Decode：从噪声到像素 ｜ 7.4 尺寸、宽高比与显存

### 第 8 章 采样引擎：KSampler 参数全解（Sampling & KSampler） · [待写]

> 文件：`01_core_nodes/docs/ch08_ksampler.md` ｜ 实操：`01_core_nodes/tasks/ch08_task.md`

**本章子概念索引：** 采样器（Sampler）· 调度器（Scheduler）· steps · CFG · seed · denoise · 降噪循环直觉

**节骨架：** 8.1 采样在干什么（从噪声一步步去噪）｜ 8.2 seed / steps / CFG 三兄弟 ｜ 8.3 sampler 与 scheduler 怎么选 ｜ 8.4 denoise 的两种语境 ｜ 8.5 常见参数组合速查（链到 [appB](90_appendix/docs/appB_parameter_cheatsheet.md)）

---

## 第 3 篇 图像工作流 → `02_image_workflow/`

前置：第 2 篇。目标：把「文生图一个套路」扩展成图生图、局部重绘、放大这三类高频工作流。

### 第 9 章 图生图（Image-to-Image） · [待写]

> 文件：`02_image_workflow/docs/ch09_img2img.md` ｜ 实操：`02_image_workflow/tasks/ch09_task.md`

**本章子概念索引：** Load Image ｜ VAE Encode ｜ denoise 强度 ｜ 参考图 vs 重绘

**节骨架：** 9.1 从一张已有图出发 ｜ 9.2 Load Image → VAE Encode 替换 EmptyLatentImage ｜ 9.3 denoise 决定改动幅度 ｜ 9.4 常见坑：尺寸不匹配

### 第 10 章 局部重绘与蒙版（Inpainting & Mask） · [待写]

> 文件：`02_image_workflow/docs/ch10_inpainting.md` ｜ 实操：`02_image_workflow/tasks/ch10_task.md`

**本章子概念索引：** 蒙版（Mask）· 绘制蒙版（Paint Mask）· SetLatentNoiseMask ｜ Inpaint Model Conditioning ｜ 只改选定区域

**节骨架：** 10.1 局部重绘解决什么问题 ｜ 10.2 制作蒙版 ｜ 10.3 两条路线：SetLatentNoiseMask vs Inpaint 专用模型 ｜ 10.4 边缘融合与参数

### 第 11 章 放大与高清修复（Upscaling & Hires-fix） · [待写]

> 文件：`02_image_workflow/docs/ch11_upscale.md` ｜ 实操：`02_image_workflow/tasks/ch11_task.md`

**本章子概念索引：** 潜空间放大（LatentUpscale）· 图像放大节点（Upscale Image / ESRGAN）· 二次采样（Hires-fix）· Ultimate SD Upscale

**节骨架：** 11.1 为什么要分两段生成 ｜ 11.2 LatentUpscale + 二次 KSampler ｜ 11.3 用放大模型补细节 ｜ 11.4 显存与耗时权衡

### 第 12 章 批处理与种子（Batch & Seed） · [待写]

> 文件：`02_image_workflow/docs/ch12_batch_seed.md` ｜ 实操：`02_image_workflow/tasks/ch12_task.md`

**本章子概念索引：** batch_size ｜ 固定种子 vs 随机ize ｜ 种子遍历（Seed Travel）· Primitive 节点 ｜ 批量产出管理

**节骨架：** 12.1 一次出多张：batch_size ｜ 12.2 锁种子复现 vs 换种子探索 ｜ 12.3 Primitive 让一个参数驱动多处 ｜ 12.4 给产出做记录

---

## 第 4 篇 控制与精修 → `03_control_and_refine/`

前置：第 3 篇。目标：从「靠提示词碰运气」到「精确控制构图、姿态、角色一致性」。

### 第 13 章 ControlNet：构图与姿态控制（ControlNet） · [待写]

> 文件：`03_control_and_refine/docs/ch13_controlnet.md` ｜ 实操：`03_control_and_refine/tasks/ch13_task.md`

**本章子概念索引：** ControlNet 原理（够用）· 预处理器（Preprocessor：OpenPose / Depth / Canny / LineArt）· Apply ControlNet ｜ 强度与起止步数

**节骨架：** 13.1 用一张参考图「框住」构图 ｜ 13.2 预处理器：从图提取骨架/深度/边缘 ｜ 13.3 连线与 ControlNet apply ｜ 13.4 strength / start / end 怎么调

### 第 14 章 参考图与一致性（IP-Adapter & Reference） · [待写]

> 文件：`03_control_and_refine/docs/ch14_reference.md` ｜ 实操：`03_control_and_refine/tasks/ch14_task.md`

**本章子概念索引：** IP-Adapter ｜ Reference-Only ｜ 角色一致性（Character Consistency）· 与 ControlNet 的分工

**节骨架：** 14.1 一致性问题是什么 ｜ 14.2 IP-Adapter 加载与接线 ｜ 14.3 权重与风格/身份的取舍 ｜ 14.4 和 ControlNet 怎么配合

### 第 15 章 提示词进阶（Advanced Prompting） · [待写]

> 文件：`03_control_and_refine/docs/ch15_prompt_advanced.md` ｜ 实操：`03_control_and_refine/tasks/ch15_task.md`

**本章子概念索引：** 权重语法（`(word:1.2)`）· 强调/弱化 ｜ 提示词顺序 ｜ 转义与标点 ｜ 常见写法误区

**节骨架：** 15.1 为什么要给词加权 ｜ 15.2 权重语法与读法 ｜ 15.3 顺序与组合的影响 ｜ 15.4 易错点与可复现记录

### 第 16 章 节点操作进阶（Node Skills） · [待写]

> 文件：`03_control_and_refine/docs/ch16_node_skills.md` ｜ 实操：`03_control_and_refine/tasks/ch16_task.md`

**本章子概念索引：** Reroute 连线整理 ｜ Node Group 分组 ｜ Mute / Bypass ｜ Primitive ｜ Note 备注 ｜ 快捷键与画布操作

**节骨架：** 16.1 工作流变大后的整理需求 ｜ 16.2 Reroute 与 Group ｜ 16.3 Mute / Bypass 做 A/B 对比 ｜ 16.4 画布操作与快捷键

---

## 第 5 篇 模型与 LoRA → `04_models_and_lora/`

前置：第 2、3 篇。目标：认识主流模型家族，理解 FLUX/SDXL 工作流差异，用好 LoRA。

### 第 17 章 模型家族（Model Families） · [待写]

> 文件：`04_models_and_lora/docs/ch17_model_families.md` ｜ 实操：`04_models_and_lora/tasks/ch17_task.md`

**本章子概念索引：** SD 1.5 ｜ SDXL ｜ FLUX ｜ Z-Image / 国产新模型 ｜ 各自的最佳分辨率与版权/许可

**节骨架：** 17.1 一张表看清主流模型 ｜ 17.2 SD1.5 与 SDXL ｜ 17.3 FLUX 的特点 ｜ 17.4 许可与商用注意

### 第 18 章 模型文件与目录（Model Files & Paths） · [待写]

> 文件：`04_models_and_lora/docs/ch18_model_files.md` ｜ 实操：`04_models_and_lora/tasks/ch18_task.md`

**本章子概念索引：** safetensors / ckpt / gguf ｜ fp16 / fp8 / 量化 ｜ `models/` 子目录分工 ｜ 下载来源与校验 ｜ 版本管理

**节骨架：** 18.1 常见模型文件格式 ｜ 18.2 精度与量化怎么选（显存权衡）｜ 18.3 目录结构与放错位置的排查 ｜ 18.4 下载来源与命名规范

### 第 19 章 LoRA：风格与角色（LoRA） · [待写]

> 文件：`04_models_and_lora/docs/ch19_lora.md` ｜ 实操：`04_models_and_lora/tasks/ch19_task.md`

**本章子概念索引：** LoRA 是什么（够用）· LoraLoader ｜ 强度（model / clip strength）· 触发词 ｜ 多个 LoRA 叠加

**节骨架：** 19.1 LoRA 解决什么问题 ｜ 19.2 LoraLoader 接线与强度 ｜ 19.3 触发词与权重配合 ｜ 19.4 多 LoRA 叠加与冲突

### 第 20 章 多模型工作流对照（Workflow Variants） · [待写]

> 文件：`04_models_and_lora/docs/ch20_workflow_variants.md` ｜ 实操：`04_models_and_lora/tasks/ch20_task.md`

**本章子概念索引：** SDXL 工作流 ｜ FLUX 工作流（双 CLIP + UNET）· Z-Image 模板 ｜ 模板工作流导入

**节骨架：** 20.1 为什么 FLUX 节点不一样 ｜ 20.2 SDXL 文生图差异点 ｜ 20.3 FLUX 从零搭一条 ｜ 20.4 用官方模板快速起步

---

## 第 6 篇 视频与进阶 → `05_video_and_advanced/`

前置：第 2、5 篇。目标：从静态图迈向动态视频，了解多模态扩展。本节多数为 `[选读]`，按需深入。

### 第 21 章 视频生成入门（Video Generation Basics） · [待写]

> 文件：`05_video_and_advanced/docs/ch21_video_basics.md` ｜ 实操：`05_video_and_advanced/tasks/ch21_task.md`

**本章子概念索引：** 视频模型家族（AnimateDiff / Wan / HunyuanVideo）· 帧数与时长 ｜ 视频 Latent ｜ 显存挑战

**节骨架：** 21.1 视频生成与图像的差别 ｜ 21.2 主流视频模型对比 ｜ 21.3 一段最小视频工作流 ｜ 21.4 帧数、尺寸与显存

### 第 22 章 图生视频与运动控制（Image-to-Video） · [选读]

> 文件：`05_video_and_advanced/docs/ch22_img2video.md` ｜ 实操：`05_video_and_advanced/tasks/ch22_task.md`

**本章子概念索引：** 首帧/首尾帧控制 ｜ 运动提示词 ｜ 相机控制 ｜ 时长与循环

**节骨架：** 22.1 用一张图当视频起点 ｜ 22.2 首帧/尾帧条件 ｜ 22.3 运动描述与稳定性 ｜ 22.4 常见伪影与缓解

### 第 23 章 多模态扩展概览：音频 / 3D / MCP · [选读]

> 文件：`05_video_and_advanced/docs/ch23_multimodal.md`

**本章子概念索引：** 音频生成 ｜ 3D 生成 ｜ AI 智能体与 MCP ｜ Comfy CLI

**节骨架：** 23.1 生成式 AI 的其它模态 ｜ 23.2 3D / 音频节点生态 ｜ 23.3 用 MCP 让智能体跑工作流 ｜ 23.4 命令行调用（链接到 [ch25](06_ecosystem/docs/ch25_api_automation.md)）

---

## 第 7 篇 生态与工程 → `06_ecosystem/`

前置：第 1~3 篇。目标：把 ComfyUI 从「能玩」变成「稳定高效、可编程、可协作」。

### 第 24 章 ComfyUI Manager 与自定义节点（Manager & Custom Nodes） · [待写]

> 文件：`06_ecosystem/docs/ch24_manager.md` ｜ 实操：`06_ecosystem/tasks/ch24_task.md`

**本章子概念索引：** Manager 安装与面板 ｜ 自定义节点安装/更新/卸载 ｜ 缺失节点报错 ｜ Comfy Registry

**节骨架：** 24.1 为什么需要 Manager ｜ 24.2 安装、搜索、更新节点包 ｜ 24.3 「节点缺失」排查 ｜ 24.4 安全与版本锁定

### 第 25 章 API 与自动化（API & Automation） · [选读]

> 文件：`06_ecosystem/docs/ch25_api_automation.md` ｜ 实操：`06_ecosystem/tasks/ch25_task.md`

**本章子概念索引：** 工作流 API 格式 vs UI 格式 ｜ `/prompt` 接口 ｜ 用脚本批量出图 ｜ comfy-cli / Comfy Router

**节骨架：** 25.1 两种 JSON 格式的区别 ｜ 25.2 导出 API 格式工作流 ｜ 25.3 用 Python 提交任务（概念）｜ 25.4 云端 Router 与 CLI

### 第 26 章 性能与显存优化（Performance & VRAM） · [选读]

> 文件：`06_ecosystem/docs/ch26_performance.md` ｜ 实操：`06_ecosystem/tasks/ch26_task.md`

**本章子概念索引：** 显存不足（OOM）· 低显存模式 ｜ 精度 / 量化 ｜ attention 后端 ｜ 分块与卸载

**节骨架：** 26.1 显存花在哪 ｜ 26.2 低显存与 CPU 卸载 ｜ 26.3 精度与 attention 选择 ｜ 26.4 定位瓶颈与取舍

---

## 附录 → `90_appendix/`

### 附录 A 节点速查表（Node Cheatsheet） · [待写]

> 文件：`90_appendix/docs/appA_node_cheatsheet.md`
> 按用途分组：加载 / 条件 / 潜空间 / 采样 / 图像 / 控制 / 批处理 / 工具，每个节点一句话 + 典型接线。

### 附录 B 参数速查（Parameter Cheatsheet） · [待写]

> 文件：`90_appendix/docs/appB_parameter_cheatsheet.md`
> sampler / scheduler / steps / CFG / denoise / seed 的选择表与常见组合，链回 [ch08](01_core_nodes/docs/ch08_ksampler.md)。

### 附录 C 故障排查（Troubleshooting） · [待写]

> 文件：`90_appendix/docs/appC_troubleshooting.md`
> OOM、节点缺失、模型不识别、连线类型不匹配、出图全黑/全噪声、打不开网页等，按「现象 → 原因 → 处理」列。

### 附录 D 资源与社区（Resources） · [待写]

> 文件：`90_appendix/docs/appD_resources.md`
> 官方文档、Comfy Cloud、模型站、工作流社区、自定义节点仓库、本项目参考来源。

---

## 写作与实操约定（速览）

- **每章两份文件**：`docs/chNN_*.md`（教学）+ `tasks/chNN_task.md`（实操任务），同号
- **节锚点**：`<a id="cNN-MM"></a>` + `### 8.2 ...（English）`，索引链 `#cNN-MM`
- **单节结构**：概念定义 → 直觉类比 → 界面/参数 → 常见误区 → 对应实操链接
- **不打 tags**：frontmatter 留空或省略；章节间用相对超链
- 详细规则见 [CONTRIBUTING.md](CONTRIBUTING.md)，术语见 [NOTATION.md](NOTATION.md)
