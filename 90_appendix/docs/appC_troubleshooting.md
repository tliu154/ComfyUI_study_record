---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/排错"
  - "#source/官方文档"
created: 2026-11-18
---
# 附录 C 故障排查（Troubleshooting）

> 前置：无，报错时按现象查 ｜ 状态：`[已完成]` ｜ 所属：`90_appendix/`

**一句话**：ComfyUI 常见毛病按「**现象 → 原因 → 处理**」列成速查条，报错时先对现象、再按原因试处理，
从最常见、最容易的开头，一步步排除。

> 用法：Ctrl+F 搜报错关键词（如 `out of memory`、`node`、全黑）。
> 排查心法：**一次只改一处**，改完重试，才能定位真因（和 [ch26 26.4](../../06_ecosystem/docs/ch26_performance.md#c26-04) 一个道理）。

## 目录

| 现象 | 去哪条 |
|---|---|
| 显存爆了 / CUDA out of memory | [C.1](#appC-01) |
| 红色节点 / Node type not found / 节点缺失 | [C.2](#appC-02) |
| 模型不识别 / 下拉列表里没有模型 | [C.3](#appC-03) |
| 连线颜色不对 / 类型不匹配 | [C.4](#appC-04) |
| 出图全黑 / 全噪声 / 全灰 | [C.5](#appC-05) |
| 打不开网页 / 连不上 localhost | [C.6](#appC-06) |
| 队列卡住 / 一直排队不出图 | [C.7](#appC-07) |
| 图糊 / 画质差 / 不像提示词 | [C.8](#appC-08) |

---

<a id="appC-01"></a>

### C.1 显存爆了（CUDA out of memory / OOM）

- **现象**：队列报错 `CUDA out of memory`、`Out of memory`，或程序崩溃退出。
- **原因**：显存被模型权重 + latent + 中间结果占满。常见诱因：尺寸开太大、batch 太多、视频帧数太多、模型精度太高。
- **处理**（按性价比依次试，命中即停）：
  1. 降出图尺寸（1024→768→512）
  2. 降 `batch_size` / 视频帧数（[ch21](../../05_video_and_advanced/docs/ch21_video_basics.md)）
  3. 换 fp8 / 量化模型（[ch18](../../04_models_and_lora/docs/ch18_model_files.md)）
  4. 加启动参数 `--lowvram`；最后手段 `--cpu`（[ch26 26.2](../../06_ecosystem/docs/ch26_performance.md#c26-02)）
  5. 关掉其它占显存的程序（游戏、另一个 AI 应用）
- 详见 [ch26 性能与显存](../../06_ecosystem/docs/ch26_performance.md)。

---

<a id="appC-02"></a>

### C.2 节点缺失（红色节点 / Node type not found）

- **现象**：打开工作流画布上有红色高亮节点，或报错 `Node type not found`。
- **原因**：那条工作流用到的**自定义节点包**你没装（不是缺模型！）。
- **处理**：
  1. `Manager → Install Missing Custom Nodes` → 勾选 → 安装 → **重启 ComfyUI**
  2. 一键失败：看缺失节点对应的**包名**（节点类名≠包名），去 Manager 搜或查 GitHub 手动装
  3. 重启后按 `R` / 强刷浏览器（`Ctrl+F5`）确认节点出现
- 详见 [ch24 24.3](../../06_ecosystem/docs/ch24_manager.md#c24-03)。

---

<a id="appC-03"></a>

### C.3 模型不识别（下拉列表里没有 / 找不到模型）

- **现象**：`Load Checkpoint` 下拉里空的、或报错找不到某个 `.safetensors`。
- **原因**：模型文件放错目录，或刚放进去没刷新，或下载的文件损坏/不完整。
- **处理**：
  1. 确认放对目录：checkpoint → `models/checkpoints/`；LoRA → `models/loras/`；VAE → `models/vae/`（[ch18](../../04_models_and_lora/docs/ch18_model_files.md)）
  2. 界面按 `R` 刷新模型列表；不行就**重启 ComfyUI**
  3. 检查文件是否完整（下载中断会留残缺文件）；确认不是把压缩包当成模型放进去
  4. 文件名带中文/特殊字符偶尔出问题，可试改英文名

---

<a id="appC-04"></a>

### C.4 连线类型不匹配（连线颜色不对 / 连不上）

- **现象**：拖动连线时端口不亮、连不上，或连上后报错类型不对。
- **原因**：ComfyUI 端口有**数据类型**，只有同类型能连（见颜色表）。
- **处理**：对颜色——
  | 数据 | 常见颜色 | 说明 |
  |---|---|---|
  | MODEL | 黄 | 扩散模型 |
  | CLIP | 棕/紫 | 文本编码器 |
  | VAE | 浅蓝 | 编解码器 |
  | CONDITIONING | 红/粉 | 提示词条件 |
  | LATENT | 绿/紫 | 潜空间 |
  | IMAGE | 深蓝 | 像素图 |
  | MASK | 灰/黑 | 蒙版 |
  - 想连的两个东西颜色不同 = 中间缺了转换节点（如像素图要进 latent，得先 `VAE Encode`）。
  - 详见 [ch04 4.2](../../01_core_nodes/docs/ch04_mental_model.md#c04-02)。

---

<a id="appC-05"></a>

### C.5 出图全黑 / 全噪声 / 全灰

- **现象**：出图是一张纯黑、纯噪声、纯灰或花屏，完全不是想要的内容。
- **原因与处理**：
  | 现象 | 可能原因 | 处理 |
  |---|---|---|
  | 全噪声 | steps 太少 / KSampler 没接好 | 加 steps 到 20；检查 model/positive/negative/latent 四路都接了 |
  | 全黑 | VAE 与模型不匹配 / VAE 损坏 | 换匹配 VAE；SD1.5 用自带 VAE 试试 |
  | 全灰/低对比 | 模型或 CFG 异常 | 恢复默认 CFG=8；换一个已知能用的 checkpoint |
  | 局部花屏 | 显存不足导致计算错误 | 降尺寸/精度（见 C.1） |
- 排查法：先跑一条**已知能用的最小文生图**（[ch03](../../00_getting_started/docs/ch03_first_workflow.md)），逐个把自己工作流的节点换进去，定位是哪一步坏的。

---

<a id="appC-06"></a>

### C.6 打不开网页 / 连不上 localhost:8188

- **现象**：浏览器打不开 `http://127.0.0.1:8188`，或提示连接被拒绝。
- **原因与处理**：
  1. **ComfyUI 没启动 / 崩了**：看启动终端有没有报错窗口，重启
  2. **端口被占**：另一个 ComfyUI 正开着占用 8188；关掉它或用 `--port 8189` 换端口
  3. **地址写错**：用 `127.0.0.1` 而非 `localhost`（个别环境 DNS 解析问题）
  4. **浏览器缓存**：`Ctrl+F5` 强刷，或换无痕窗口
  5. **远程访问**：默认只监听本机，局域网访问需 `--listen 0.0.0.0`（注意安全）
- 安装与启动见 [ch02](../../00_getting_started/docs/ch02_installation.md)。

---

<a id="appC-07"></a>

### C.7 队列卡住 / 一直排队不出图

- **现象**：任务进队列但不动、进度条卡住、或前面任务失败后全堵住。
- **原因与处理**：
  1. **某个任务报错卡住**：看终端报错信息，按对应条目修；点队列里的 `Clear` 清掉坏任务
  2. **模型加载慢**：首次加载大模型要等几十秒，耐心看终端日志
  3. **显存不够在反复卸载**：见 C.1 / [ch26](../../06_ecosystem/docs/ch26_performance.md)
  4. **浏览器与后端失联**：刷新页面（不影响后端队列）

---

<a id="appC-08"></a>

### C.8 图糊 / 画质差 / 不像提示词

- **现象**：出图能看，但细节糊、构图不对、跟提示词关系不大。
- **原因与处理**：
  | 问题 | 先查 | 参考 |
  |---|---|---|
  | 细节糊 | steps 太低、尺寸太小、没放大 | 加 steps、用 [ch11](../../02_image_workflow/docs/ch11_upscale.md) 放大 |
  | 不听提示词 | CFG 太低、提示词写法 | 调 CFG、优化提示词（[ch15](../../03_control_and_refine/docs/ch15_prompt_advanced.md)）|
  | 构图不受控 | 没用控制手段 | 上 ControlNet（[ch13](../../03_control_and_refine/docs/ch13_controlnet.md)）|
  | 参数乱 | 没锁 seed 乱调 | 按 [附录 B](appB_parameter_cheatsheet.md#appB-06) 起点 + 单变量调整 |
  | 模型本身弱 | 模型能力上限 | 换更强模型（[ch17](../../04_models_and_lora/docs/ch17_model_families.md)）|

---

## 小结

- 排查顺序：先对**现象**→看**原因**→按**从易到难**试处理，一次只改一处。
- 高频三件套：OOM（降尺寸/精度）、节点缺失（Manager 一键装+重启）、模型不识别（放对目录+R 刷新）。
- 终极兜底：回到一条**已知能用的最小工作流**（[ch03](../../00_getting_started/docs/ch03_first_workflow.md)），逐个替换节点定位问题。

> 下一附录：[附录 D 资源与社区](appD_resources.md) ｜ 回 [附录首页](../README.md)
