---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/工作流"
created: 2026-11-18
---
# 实操 20：导入模板并对照节点差异

> 对应章节：[第 20 章 多模型工作流对照](../docs/ch20_workflow_variants.md) ｜ 预计耗时：40 分钟
> 状态：`[已完成]`

## 目标

导入一条官方/社区模板工作流（SDXL 或 FLUX），跑通或至少看清结构，并标出它和 SD1.5 的节点差异。
**本篇以"看懂差异"为主；不必强求跑通 FLUX（显存门槛较高）。**

## 前提

- [ ] 会搭 SD1.5 文生图（ch03），并理解其节点（ch04~ch08）
- [ ] 网络可访问模板来源（官方模板标签页 / Cloud / 社区）

## 步骤

1. **选一个模板**：在 ComfyUI 的模板入口（`Workflow > Browse Templates` 或官方 Cloud）选一条
   SDXL 或 FLUX 文生图模板，导入到画布。

2. **放好模型**：按模板提示下载所需模型文件放对应目录（[ch18](../docs/ch18_model_files.md)），按 `R` 刷新。
   若显存/模型不全跑不了，也没关系，重点看结构。

3. **逐节点对照 SD1.5**（照 [ch20 差异表](../docs/ch20_workflow_variants.md#c20-01)），在记录表里标出：
   - 加载环节用了什么节点？（对照 SD1.5 的 `Load Checkpoint`）
   - 文本编码用了什么？（单 CLIP / SDXL 双 CLIP / CLIP+T5）
   - KSampler 的 cfg / steps 是多少？（对照 SD1.5 的 cfg8/steps20）
   - 有没有负向提示词？
   - 后半段是不是还是 `VAE Decode → Save Image`？

4. **（条件允许）跑通**：改提示词，Queue Prompt，看是否出图。

5. **总结差异**：用一句话说出「这条模板和 SD1.5 最大的不同是什么」。

## 验收标准

- [ ] 记录表填出模板的加载/编码/采样参数
- [ ] 能指出至少 2 处和 SD1.5 的节点差异
- [ ] 验证了「核心链相同、加载+编码不同」的骨架认知

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| FLUX 模板里把 cfg 改成 8 | 画面异常 | distilled FLUX 要 cfg≈1，见 ch20 20.3 |
| 模板缺模型就跑 | 报模型缺失 | 模板不含模型文件，见 ch20 20.4 |
| 用 SD1.5 的编码节点替换 SDXL 的 | 效果差/报错 | 编码器要和模型配套，见 ch20 20.2 |

## 可复现参数记录

| 维度 | 模板（SDXL/FLUX） | SD1.5 对照 |
|---|---|---|
| 加载节点 | | Load Checkpoint |
| 文本编码节点 | | 单个 CLIP Text Encode |
| cfg / steps | | 8 / 20 |
| 负向词 | 有/无 | 有 |
| 后半段 | | VAE Decode → Save Image |

## 常见问题

- 模板跑不起来 → 多半缺模型，看报错缺哪个就下哪个，见 [ch18](../docs/ch18_model_files.md#c18-03)
- FLUX 显存不够 → 用 fp8 模型 / 低显存模式（[ch26](../../06_ecosystem/docs/ch26_performance.md)）
- 看不懂模板节点 → 回看 [ch20 20.3](../docs/ch20_workflow_variants.md#c20-03) 骨架
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

**第 5 篇模型与 LoRA 完成！** 你现在认识主流模型家族、会管模型文件、会用 LoRA、看得懂不同模型的工作流。
进入 [第 6 篇 视频与进阶](../../05_video_and_advanced/README.md)，从 [ch21 视频生成入门](../../05_video_and_advanced/docs/ch21_video_basics.md) 开始。
