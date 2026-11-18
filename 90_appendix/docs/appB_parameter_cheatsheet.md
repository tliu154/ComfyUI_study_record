---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/参数"
  - "#source/官方文档"
created: 2026-11-18
---
# 附录 B 参数速查（Parameter Cheatsheet）

> 前置：[ch08 KSampler](../../01_core_nodes/docs/ch08_ksampler.md) ｜ 状态：`[已完成]` ｜ 所属：`90_appendix/`

**一句话**：把 KSampler 那堆旋钮（sampler / scheduler / steps / CFG / denoise / seed）的
**怎么选、常见组合、调了会怎样**压成几张表，忘了就回来查。参数含义详解看 [ch08](../../01_core_nodes/docs/ch08_ksampler.md)。

> 用法：这是**速查表不是教程**。调参没思路时按「常见组合」抄一个起点，再单变量微调（配合 [ch26](../../06_ecosystem/docs/ch26_performance.md) 的记录法）。

## 目录

| 参数 | 一句话 | 深入 |
|---|---|---|
| [B.1 seed](#appB-01) | 随机种子，锁住可复现，换它探索 | [ch08 8.2](../../01_core_nodes/docs/ch08_ksampler.md#c08-02) |
| [B.2 steps](#appB-02) | 去噪步数，质量/速度权衡 | 同上 |
| [B.3 CFG](#appB-03) | 提示词跟随强度 | 同上 |
| [B.4 sampler / scheduler](#appB-04) | 去噪算法与调度策略 | [ch08 8.3](../../01_core_nodes/docs/ch08_ksampler.md#c08-03) |
| [B.5 denoise](#appB-05) | 改动幅度（图生图关键） | [ch09](../../02_image_workflow/docs/ch09_img2img.md) |
| [B.6 常见组合速查](#appB-06) | 直接抄的起点参数 | — |

---

<a id="appB-01"></a>

### B.1 seed（随机种子）

| 值 | 效果 |
|---|---|
| 固定（如 42） | 其它参数不变时**每次出同一张图**，用于复现/对比 |
| -1 / randomize | 每次随机，用于探索不同构图 |
| 逐帧/逐张递增 | 批处理、seed travel 做变体（[ch12](../../02_image_workflow/docs/ch12_batch_seed.md)） |

**记法**：改图先锁 seed，一次只动一个参数，才能看清那个参数的作用。

---

<a id="appB-02"></a>

### B.2 steps（去噪步数）

| 范围 | 含义 | 场景 |
|---|---|---|
| 4~8 | 少步（配合 turbo/distill 模型） | 快速预览、(torch) 少步模型 |
| 20~30 | 常规甜点区 | SD1.5 / SDXL 默认质量 |
| 30~50 | 偏高 | 想榨细节，收益递减、变慢 |

**调了会怎样**：↑更精细但更慢、到一定程度不再变好；↓变快但可能细节糊/结构崩。

---

<a id="appB-03"></a>

### B.3 CFG（Classifier-Free Guidance）

| 模型/场景 | 常用 CFG | 说明 |
|---|---|---|
| SD1.5 常规 | 7~9 | 经典默认 8 |
| SDXL | 5~8 | 比 SD1.5 略低 |
| FLUX（distilled） | ≈1（1.0~3.5） | **关键差异**：用 SD1.5 的 8 会崩（[ch20](../../04_models_and_lora/docs/ch20_workflow_variants.md)） |
| 创意/发散 | 低（<5） | 模型自由度大 |
| 严格跟随提示词 | 高（>10） | 过高会过饱和、僵硬 |

**记法**：CFG = 「听提示词的话程度」。FLUX 是最大的坑——** distilled 版 CFG≈1**。

---

<a id="appB-04"></a>

### B.4 sampler / scheduler（采样器与调度器）

**sampler（去噪算法）** 常见选择——
| sampler | 特点 |
|---|---|
| `euler` | 快、稳，入门首选 |
| `euler_ancestral` | 带随机性，每步略不同 |
| `dpmpp_2m` | 质量好、速度与质量平衡，常用 |
| `dpmpp_2m_sde` | 更细节，配 Karras 常见 |
| `uni_pc` | 少步也能出好图 |

**scheduler（噪声调度）** 常见选择——
| scheduler | 特点 |
|---|---|
| `normal` | 默认 |
| `karras` | 常配 dpmpp，细节更好，推荐尝试 |
| `exponential` / `sgm_uniform` | 进阶调度 |

**记法**：sampler = 怎么走每一步，scheduler = 每一步噪声多大。
不知道选啥：`dpmpp_2m + karras` 或 `euler + normal` 起步（[ch08 8.3](../../01_core_nodes/docs/ch08_ksampler.md#c08-03)）。

---

<a id="appB-05"></a>

### B.5 denoise（降噪强度）

| 场景 | denoise | 效果 |
|---|---|---|
| 文生图 | 1.0 | 从纯噪声生成，完全自由 |
| 图生图-轻改 | 0.3~0.5 | 保留原图结构，只微调风格/细节 |
| 图生图-中改 | 0.5~0.75 | 原图当参考，构图可变 |
| 图生图-重画 | 0.85~1.0 | 几乎重新生成 |

**记法**：denoise = 「把原图打碎多少重来」。低=保守，高=放飞。详见 [ch09](../../02_image_workflow/docs/ch09_img2img.md)。

---

<a id="appB-06"></a>

### B.6 常见组合速查（可直接抄的起点）

| 场景 | 模型 | steps | CFG | sampler | scheduler | denoise |
|---|---|---|---|---|---|---|
| **SD1.5 通用** | SD1.5 | 20 | 8 | euler | normal | 1.0 |
| **SD1.5 质量** | SD1.5 | 30 | 7 | dpmpp_2m | karras | 1.0 |
| **SDXL 通用** | SDXL | 30 | 6 | dpmpp_2m | karras | 1.0 |
| **FLUX** | FLUX distilled | 20~28 | ≈1 | euler / dpmpp | simple / beta | 1.0 |
| **图生图轻改** | 同模型 | 20 | 8 | euler | normal | 0.4~0.5 |
| **快速预览** | 同模型 | 8~12 | 7 | euler | normal | 1.0 |

> 注：这些是**起点不是标准答案**。不同模型/版本最佳参数不同；换模型先查其官方推荐。
> 少步/turbo 模型需要专门的参数组合，别套常规表。

---

## 小结

- 调参铁律：**锁 seed，一次只改一个变量，记录结果**（[ch12](../../02_image_workflow/docs/ch12_batch_seed.md) + [ch26](../../06_ecosystem/docs/ch26_performance.md)）。
- 最大的坑：FLUX distilled 的 CFG≈1，别用 SD1.5 的 8。
- 没思路就抄 B.6 的对应起点，再微调 steps / CFG。

> 下一附录：[附录 C 故障排查](appC_troubleshooting.md) ｜ 回 [附录首页](../README.md)
