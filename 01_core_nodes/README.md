---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 第 2 篇 核心节点（Core Nodes）

前置：[第 1 篇](../00_getting_started/README.md)（能跑通第一条工作流）。
目标：把每条线「为什么这么连」搞懂，从照抄工作流变成能自己改、自己搭。

**状态**：`[已完成]` 5 章教学 + 5 份实操。
**学完你能**：解释节点/连线/数据类型、区分加载器三输出、写有效的正负提示词、理解潜空间、调明白 `KSampler` 的每个参数。

## 依赖

- [ch04 心智模型](../01_core_nodes/docs/ch04_mental_model.md) 是本篇地基，先读
- ch05~ch07 分别讲清第一条工作流里的每条线
- [ch08 KSampler](../01_core_nodes/docs/ch08_ksampler.md) 是本篇重点，参数速查链到 [appB](../90_appendix/docs/appB_parameter_cheatsheet.md)

## 章节

章节清单、状态、预定文件一律见 [SYLLABUS 第 2 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 拿 ch03 的默认工作流，逐个节点解释「这条线传的是什么类型的数据」
- 固定其它参数，只调 CFG / steps 各跑一组对照，记录到实操文件
- 拆开 `Load Checkpoint`，改用 `UNET + CLIP + VAE` 分开加载，验证出图一致
