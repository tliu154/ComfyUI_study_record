---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/批处理"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 12：批量出图与参数记录

> 对应章节：[第 12 章 批处理与种子](../docs/ch12_batch_seed.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

用 batch_size 一次出多张，体验 seed 递增；并用 Primitive 统一控制，最后为产出做一份可复现参数记录。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 工作流会搭
- [ ] 显存够出 4 张 512 图（不够就减到 2）

## 步骤

1. **批量出图**：加载文生图工作流，`Empty Latent Image` 的 `batch_size` 设为 4，其余不变。
   Queue Prompt，一次得到 4 张。观察它们 seed 递增、内容各异（见 [ch12 12.1](../docs/ch12_batch_seed.md#c12-01)）。

2. **体验锁 seed**：把 KSampler 的 seed 锁定（点锁图标），连跑两次 Queue Prompt，确认两次出的 4 张完全一样（复现）。
   再解锁/随机 seed，看结果变化（见 [ch12 12.2](../docs/ch12_batch_seed.md#c12-02)）。

3. **用 Primitive 统一 seed**：加一个 `Primitive` 节点设为 int，连到 KSampler 的 `seed`。
   改 Primitive 的值，验证 KSampler 的 seed 跟着变——理解「一个值驱动多处」（见 [ch12 12.3](../docs/ch12_batch_seed.md#c12-03)）。

4. **做参数记录**：从 4 张里挑一张最好的，把它存成工作流 JSON（命名含 seed，如 `best_seed42.json`），
   并填写下面的记录表。

## 验收标准

- [ ] 一次 batch 出 4 张，seed 递增、内容不同
- [ ] 锁 seed 后两次结果一致
- [ ] Primitive 改动能驱动 KSampler 的 seed
- [ ] 完成一张好图的参数记录表

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| batch_size 设很大（如 16） | OOM | 显存随 batch 线性涨，见 ch12 12.1 |
| 调参时 seed 也随机 | 无法归因参数作用 | 控制变量要锁 seed，见 ch12 12.2 |
| 只记 seed 不记模型/提示词 | 后来复现不出来 | 复现要完整参数，见 ch12 12.4 |

## 可复现参数记录（挑出的最好一张）

| 项 | 值 |
|---|---|
| 模型 | （填写）|
| seed | （填写）|
| 正向提示词 | （填写）|
| 负向提示词 | （填写）|
| steps / cfg | / |
| sampler / scheduler | / |
| 尺寸 / batch_size | 512×512 / 4 |
| 工作流文件 | best_seed__.json |

## 常见问题

- batch 出图 OOM → 减小 batch_size，见 [ch12 12.1](../docs/ch12_batch_seed.md#c12-01)
- 锁了 seed 还是变 → 检查 batch 递增模式是否覆盖，见 [ch12 12.2](../docs/ch12_batch_seed.md#c12-02)
- Primitive 连不上 → 类型不匹配，见 [ch04 连线规则](../../01_core_nodes/docs/ch04_mental_model.md#c04-04)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

**第 3 篇图像工作流完成！** 你已经掌握文生图之外的三大高频玩法。
进入 [第 4 篇 控制与精修](../../03_control_and_refine/README.md)，从 [ch13 ControlNet](../../03_control_and_refine/docs/ch13_controlnet.md) 开始，
从「靠提示词碰运气」升级到「精确控制构图」。
