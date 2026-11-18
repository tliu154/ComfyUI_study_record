# 第 5 篇 模型与 LoRA（Models and LoRA）

前置：[第 2 篇](../01_core_nodes/README.md)、[第 3 篇](../02_image_workflow/README.md)。
目标：认识主流模型家族、理解 FLUX/SDXL 工作流的节点差异、用好 LoRA 改变风格与角色。

**学完你能**：按需求选模型与精度、把模型文件放对目录、用 LoraLoader 叠风格/角色、从零搭出 FLUX 工作流。

## 依赖

- ch17~ch18 是概念与文件管理，随时可查
- ch19 LoRA 依赖 [ch05 加载器](../01_core_nodes/docs/ch05_loaders.md)
- ch20 多模型工作流依赖 [ch06 双 CLIP](../01_core_nodes/docs/ch06_conditioning.md) 与 ch17 模型家族

## 章节

章节清单、状态、预定文件一律见 [SYLLABUS 第 5 篇](../SYLLABUS.md)，此处不重复。

## 实践方向

- 同一个提示词分别用 SD1.5 / SDXL 出图，对比最佳分辨率与细节
- 加载一个风格 LoRA，做 strength 0.4 / 0.8 / 1.2 的对照
- 用官方模板导入一条 FLUX 工作流，标出它和 SD1.5 的节点差异
