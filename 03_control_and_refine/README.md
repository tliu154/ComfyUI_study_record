---
tags:
  - "#course/计算机"
  - "#type/资料"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 第 4 篇 控制与精修（Control & Refine）

前置：[第 3 篇](../02_image_workflow/README.md)（图像工作流）。
目标：从「靠提示词碰运气」到「精确控制构图、姿态、角色一致性」，并把变复杂的工作流整理干净。

**学完你能**：用 ControlNet 锁构图、用 IP-Adapter 保角色一致、用提示词权重细调、用 Reroute/Group/Mute 管理大工作流。

## 依赖

- ch13 ControlNet 依赖 [ch09 图生图](../02_image_workflow/docs/ch09_img2img.md) 的图像输入思路
- ch15 提示词进阶依赖 [ch06 条件](../01_core_nodes/docs/ch06_conditioning.md)
- ch16 节点技巧是工具性章节，任何阶段需要都能来查

## 章节

章节清单、状态、预定文件一律见 [SYLLABUS 第 4 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 同一提示词，加/不加 OpenPose ControlNet，对比姿态是否受控
- 用 IP-Adapter 固定一张角色脸，换场景与服装
- 把一个 20+ 节点的工作流用 Group 分区、Reroute 理线，Mute 掉某分支做 A/B
