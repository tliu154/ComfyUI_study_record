---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/lora"
created: 2026-11-18
---
# 实操 19：加载风格 LoRA 做强度对照

> 对应章节：[第 19 章 LoRA](../docs/ch19_lora.md) ｜ 预计耗时：35 分钟
> 状态：`[已完成]`

## 目标

把一个风格 LoRA 叠加到工作流上，做 strength 对照，理解 LoRA 如何改变画风；如含触发词，验证触发词作用。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 工作流会搭
- [ ] 下载一个**与你模型家族匹配**的 LoRA（如 SD1.5 风格 LoRA），放 `models/loras/`，按 `R` 刷新
- [ ] 记下该 LoRA 的触发词（如有，看下载页）

## 步骤

1. **搭基线**：用 ch03 文生图工作流，提示词写清楚主体（如 `a landscape mountain, sunset`），固定 seed，出图 A（不加 LoRA）。

2. **插入 LoraLoader**（照 [ch19 19.2 骨架](../docs/ch19_lora.md#c19-02)）：
   ```
   Checkpoint(MODEL) → LoraLoader(model) → KSampler(model)
   Checkpoint(CLIP)  → LoraLoader(clip)  → CLIP Text Encode(clip)
   LoraLoader 里选你的 LoRA 文件
   ```

3. **（如有触发词）写进正向**：在正向提示词加入触发词（如 `char_abc, a landscape mountain, sunset`）。

4. **strength 对照**（固定 seed/提示词，只改 strength_model 与 strength_clip，两者设同值）：
   - 0.0 → 等同没加（可用 Bypass 代替）→ 图 A 基线
   - 0.5 → 存图 B
   - 0.8 → 存图 C
   - 1.0 → 存图 D
   → 对比 A/B/C/D：LoRA 风格强度随 strength 增强，D 可能过头。

5. **触发词验证（可选）**：若有触发词，删掉触发词再跑一次，看 LoRA 效果是否变弱——印证触发词的激活作用。

## 验收标准

- [ ] 出图显示 LoRA 确实改变了画风
- [ ] strength 0.5/0.8/1.0 呈现风格逐渐增强
- [ ] （如有触发词）去掉后效果变弱

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 用错家族的 LoRA | 加载失败或无效 | LoRA 与家族绑定，见 ch19 19.1 |
| 只接 MODEL 不接 CLIP | 触发词可能不生效 | strength_clip 管文本理解，见 ch19 19.2 |
| 强度拉 1.5 | 画面僵硬/崩 | 过高过拟合，见 ch19 19.2 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 基础模型 | |
| LoRA 文件 / 家族 | |
| 触发词 | （有则填写）|
| 正向提示词 | a landscape mountain, sunset |
| strength A/B/C/D | 0 / 0.5 / 0.8 / 1.0 |
| seed / steps / cfg | 固定 / 20 / 8 |

## 常见问题

- LoRA 不在列表 → 放对 `models/loras/` 并按 R，见 [ch18](../docs/ch18_model_files.md#c18-03)
- LoRA 没效果 → 检查家族匹配、是否写了触发词、strength 是否为 0
- 出图崩 → 降低 strength，或减少叠加的 LoRA 数量，见 [ch19 19.4](../docs/ch19_lora.md#c19-04)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 20 章 多模型工作流对照](../docs/ch20_workflow_variants.md)，认识 SDXL/FLUX 工作流的节点差异。
