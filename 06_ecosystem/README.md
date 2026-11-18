---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 第 7 篇 生态与工程（Ecosystem）

前置：[第 1~3 篇](../00_getting_started/README.md)。目标：把 ComfyUI 从「能玩」变成「稳定、高效、可编程、可协作」。

**学完你能**：用 Manager 管自定义节点、排查节点缺失、用 API 批量出图、定位并缓解显存瓶颈。

## 依赖

- ch24 Manager 是工具性章节，装好就能用，越早读越省事
- ch25 API 依赖 [ch03 工作流导出](../00_getting_started/docs/ch03_first_workflow.md)（API 格式 JSON）
- ch26 性能依赖 [ch18 精度/量化](../04_models_and_lora/docs/ch18_model_files.md)

## 章节

章节清单、状态、预定文件一律见 [SYLLABUS 第 7 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 用 Manager 装一个常用节点包，更新、卸载各走一遍
- 导出一条 API 格式工作流，用脚本改 seed 批量提交
- 记录自己机器的显存与典型生成耗时，试低显存模式看差异
