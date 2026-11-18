---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/节点"
created: 2026-11-18
---
# 实操 16：整理工作流与 Mute 对比

> 对应章节：[第 16 章 节点操作进阶](../docs/ch16_node_skills.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

把一个多分支工作流用 Group 分区、Reroute 理线，并用 Mute 做一次「加/不加某分支」的 A/B 对比。

## 前提

- [ ] 有一个稍复杂的工作流（可用 ch14 的 IP-Adapter 工作流，或 ch11 的两段放大工作流）

## 步骤

1. **打开一个复杂工作流**，先保存一份备份（另存为 `before_tidy.json`）。

2. **Group 分区**（照 [ch16 16.2](../docs/ch16_node_skills.md#c16-02)）：
   - 框选「模型加载 + 提示词」相关节点 → Ctrl+G → 命名「输入与条件」
   - 框选「采样 + 解码」节点 → 成组命名「生成」
   - 若有 ControlNet/IP-Adapter → 成组命名对应分支
   - 给不同组设不同颜色；试着折叠/展开一个组，确认节点仍照常执行

3. **Reroute 理线**：找一个被多处使用的输出（如 Checkpoint 的 VAE 同时供 Encode/Decode），
   加一个 `Reroute`，把总线接到它再分流，让线更整齐。

4. **Note 备注**：加一个 `Note` 节点，在关键位置写一句说明（如「Hires-fix 二次采样，denoise 0.5」）。

5. **Mute 做 A/B**（照 [ch16 16.3](../docs/ch16_node_skills.md#c16-03)）：
   - 若工作流有 ControlNet/IP-Adapter 分支，Mute 掉它的 Apply 节点（注意下游依赖，可能需要备用路径）
   - Queue Prompt 出图 A（无该分支效果），再取消 Mute 出图 B（有该分支）
   - 对比差异，然后确认恢复到正常状态（没有节点是灰的）

## 验收标准

- [ ] 工作流被分成 ≥2 个命名 Group，折叠不影响执行
- [ ] 至少一处用 Reroute 理线、一个 Note 备注
- [ ] 用 Mute 做过一次 A/B 对比，并恢复到正常状态

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 折叠 Group | 节点隐藏但照常出图 | Group 只管显示，见 ch16 16.2 |
| Mute 掉关键节点 | 下游飘红/报错 | Mute 让输出消失，见 ch16 16.3 |
| Bypass 一个 LoraLoader | 图变成不带该 LoRA 效果，且不报错 | Bypass 透传，见 ch16 16.3 |

## 可复现参数记录

| 项 | 值 |
|---|---|
| 整理的工作流 | （原文件名）|
| 备份 | before_tidy.json |
| Group 数量 / 命名 | （填写）|
| Mute 对比的节点 | （填写）|
| 对比结论 | A vs B 差异描述 |

## 常见问题

- Mute 后报错 → 下游依赖该节点输出，改用 Bypass（若有透传路径），见 [ch16 16.3](../docs/ch16_node_skills.md#c16-03)
- 找不到成组快捷键 → 右键菜单里找 Add Group，以版本为准
- 快捷键不生效 → 不同版本可能不同，用右键菜单替代
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

**第 4 篇控制与精修完成！** 你已经能精确控制构图、姿态、一致性，并把复杂工作流整理干净。
进入 [第 5 篇 模型与 LoRA](../../04_models_and_lora/README.md)，从 [ch17 模型家族](../../04_models_and_lora/docs/ch17_model_families.md) 开始。
