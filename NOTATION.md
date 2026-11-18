---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 术语与节点名约定（Notation and Terminology）

全仓库统一。**写新章节前扫一眼，避免同一个概念三种写法、节点名对不上界面。**

## 1. 书写约定

- **首次出现**：中文（English），如「潜空间（Latent Space）」「采样器（Sampler）」
- 之后再出现用中文；约定俗成缩写（CFG、LoRA、VAE、CLIP、IP-Adapter）直接用缩写
- 标题一律「中文（English）」，英文首字母实词大写
- **节点名 / 端口名 / 控件名保持界面原文**（英文），用反引号包裹，例：`KSampler`、`ckpt_name`、`denoise`
- 菜单路径用 `>` 连接，例：`model > loaders > Load Checkpoint`
- frontmatter 按标签规范打 tags（course/type/topic/source 四类）；章节间用相对超链

## 2. 核心术语表（中英对照 + 人话）

| 中文 | 英文 / 界面名 | 人话解释 |
|---|---|---|
| 工作流 | Workflow | 一堆节点用线连起来的图，就是你的「 recipes」 |
| 节点 | Node | 干一件活的方块：加载模型、编码提示词、采样…… |
| 连线 | Link | 把上一个节点的输出接到下一个节点的输入 |
| 输入 / 输出端口 | Input / Output | 节点左右两侧的小圆点；左侧收、右侧发 |
| 控件 / 部件 | Widget | 节点内部的文本框、数字框、下拉菜单 |
| 画布 | Canvas | 摆节点、连线的大区域 |
| 队列 / 排队执行 | Queue / Queue Prompt | 点一下把当前工作流扔进任务队列开跑 |
| 检查点 / 大模型 | Checkpoint（`ckpt`） | 一个文件打包了扩散模型 + CLIP + VAE |
| 扩散模型 / UNet | Diffusion Model / UNET | 真正「去噪画图」的那部分 |
| 文本编码器 | CLIP / Text Encoder | 把提示词文字变成模型能懂的数字条件 |
| 变分自编码器 | VAE | 负责「压缩成潜空间」和「解码回像素」 |
| 潜空间 / 潜变量 | Latent Space / Latent | 图像被压缩后的低维表示，采样在这上面做 |
| 条件 | Conditioning | 提示词编码后的产物，指导模型画什么 |
| 采样器 | Sampler | 从噪声一步步去噪的算法（euler、dpmpp_2m…） |
| 调度器 | Scheduler | 控制每步噪声明怎么降（normal、karras…） |
| 采样步数 | steps | 去噪迭代多少次，越多越慢、不一定越好 |
| 无分类器引导 | CFG（Classifier-Free Guidance） | 提示词「管得多紧」，越大越听话、太大易过饱和 |
| 随机种子 | seed | 决定初始噪声；相同 seed + 相同参数 = 可复现同一张图 |
| 重绘幅度 | denoise | 在已有图上改多少：0 几乎不变，1 几乎重画 |
| 局部重绘 | Inpainting | 只改蒙圈选的区域，其余保持原图 |
| 蒙版 | Mask | 标记「哪里要重画」的黑白图 |
| 放大 / 高清修复 | Upscale / Hires-fix | 先出小图再放大并二次采样补细节 |
| 控制网络 | ControlNet | 用参考图（姿态/深度/边缘）精确控制构图 |
| 预处理器 | Preprocessor | 从参考图提取姿态骨架/深度图/边缘图的节点 |
| 图生图 | Image-to-Image（img2img） | 以一张图为基础生成新图 |
| 批处理大小 | batch_size | 一次排队生成几张 |
| LoRA | LoRA | 小体积的微调文件，加载后改变风格/角色 |
| 触发词 | Trigger Word | 训练 LoRA 时绑定、用的时候要写进提示词的词 |

## 3. 易混词（写错会误导，重点核对）

| 词 | 别写成 / 别混 | 说明 |
|---|---|---|
| 检查点（Checkpoint） | 模型（model）泛称 | Checkpoint 是打包文件；「模型」是泛称，不确定时写具体是哪个 |
| CLIP | VAE | CLIP 管文字条件，VAE 管图像压缩/解码，别混 |
| 采样器（Sampler） | 调度器（Scheduler） | 采样器是去噪算法，调度器是噪声衰减节奏；是两类参数 |
| steps | CFG | steps 是步数，CFG 是引导强度，别写成一回事 |
| denoise（重绘幅度） | 图生图专有 | 文生图里 KSampler 也有 denoise，通常留 1；图生图才调它 |
| Latent | 像素图像 | 采样发生在潜空间，`VAE Decode` 解码后才是能看的图 |
| LoRA | Checkpoint | LoRA 不能单独出图，要叠在 checkpoint 上 |
| 强度（strength） | 权重（weight） | LoraLoader 里区分 model strength 与 clip strength，写全称 |

## 4. 缩写表

`SD` Stable Diffusion ｜ `SDXL` Stable Diffusion XL ｜ `CFG` 无分类器引导 ｜
`CLIP` 对比语言-图像预训练（文本编码器）｜ `VAE` 变分自编码器 ｜
`UNET` 扩散骨干网络 ｜ `LoRA` 低秩适配 ｜ `IP-Adapter` 图像提示适配器 ｜
`ControlNet` 控制网络 ｜ `ckpt` checkpoint 模型文件 ｜ `DAG` 有向无环图 ｜
`OOM` 显存溢出 ｜ `API` 应用程序接口 ｜ `MCP` 模型上下文协议

## 5. 节点名速查（界面原文，写文档时用反引号）

**加载器**：`Load Checkpoint` · `Load Diffusion Model (UNET)` · `Load CLIP` · `Load VAE` · `LoraLoader`
**条件**：`CLIP Text Encode (Prompt)` · `CLIP Text Encode (SDXL)` · `Conditioning Combine`
**潜空间**：`EmptyLatentImage` · `VAE Encode` · `VAE Decode` · `LatentUpscale` · `SetLatentNoiseMask`
**采样**：`KSampler` · `KSamplerAdvanced`
**图像**：`Load Image` · `Save Image` · `Upscale Image` · `ImageComposite`
**控制**：`ControlNetLoader` · `ControlNetApplyAdvanced` · `IPAdapter`
**工具**：`Reroute` · `Primitive` · `Note` · `Node Group`

> 节点名随 ComfyUI 版本可能变化。以界面实际显示为准，发现不符时更新本表并说明版本。

## 6. 参考资料

- ComfyUI 官方文档：https://docs.comfy.org/zh
- 官方仓库：https://github.com/Comfy-Org/ComfyUI
- 命名以官方文档与界面为准；本表只做全仓库写法统一，不替代官方文档
