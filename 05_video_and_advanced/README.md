---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 第 6 篇 视频与进阶（Video and Advanced）

前置：[第 2 篇](../01_core_nodes/README.md)、[第 5 篇](../04_models_and_lora/README.md)。
目标：从静态图迈向动态视频，了解多模态扩展。本篇多为 `[选读]`，按需深入，不必线性啃。

**学完你能**：跑通一段最小视频工作流、用首帧控制图生视频、知道 3D/音频/MCP 生态大致有什么。

## 依赖

- ch21 视频基础依赖 [ch08 采样](../01_core_nodes/docs/ch08_ksampler.md) 与 ch17 模型家族
- ch22 图生视频依赖 ch21 + [ch09 图生图](../02_image_workflow/docs/ch09_img2img.md)
- ch23 多模态概览是扫盲，链到 [ch25 API](../06_ecosystem/docs/ch25_api_automation.md)

## 章节

**状态：[已完成] 3 章教学 + 2 份实操**（ch21 / ch22 各含教学 + 实操；ch23 为多模态概览，按规划无实操）。
章节清单、状态、预定文件一律见 [SYLLABUS 第 6 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 用图生视频把一张静态图变成 2~3 秒短片，记录帧数/尺寸/显存占用
- 对比首帧控制与无首帧的运动稳定性
-  skim 一遍官方 MCP / Comfy CLI 文档，判断和自己是否相关
