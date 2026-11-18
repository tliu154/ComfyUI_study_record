---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 第 3 篇 图像工作流（Image Workflow）

前置：[第 2 篇](../01_core_nodes/README.md)（核心节点与采样参数）。
目标：把「文生图一个套路」扩展成图生图、局部重绘、放大这三类高频工作流。

**状态**：`[已完成]` 4 章教学 + 4 份实操。
**学完你能**：用已有图做 img2img、用蒙版只改局部、把小图高清放大、批量出图并管理种子。

## 依赖

- ch09 图生图依赖 [ch07 潜空间](../01_core_nodes/docs/ch07_latent.md)（VAE Encode）与 [ch08 denoise](../01_core_nodes/docs/ch08_ksampler.md)
- ch10 局部重绘依赖 ch09
- ch11 放大依赖 ch07 + ch08 的二次采样
- ch12 批处理依赖 [ch08 seed](../01_core_nodes/docs/ch08_ksampler.md)

## 章节

章节清单、状态、预定文件一律见 [SYLLABUS 第 3 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 同一张图，用不同 denoise 跑 img2img，做一张「改动幅度」对照表
- 给一张图抠出某个物体做局部重绘，只换主体、保留背景
- 一张 512 图走完整放大流程到 2K，对比放大前后细节
