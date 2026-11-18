---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/模型"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 05：拆解 checkpoint，认识三输出

> 对应章节：[第 5 章 加载器](../docs/ch05_loaders.md) ｜ 预计耗时：25 分钟
> 状态：`[已完成]`

## 目标

把 `Load Checkpoint` 的三个输出分别接到能显示它们的节点上，直观认识 MODEL / CLIP / VAE 各是什么；并练习按 R 刷新模型列表。

## 前提

- [ ] [`ch03_task.md`](../../00_getting_started/tasks/ch03_task.md) 的工作流已保存
- [ ] `models\checkpoints\` 里至少有一个 SD1.5 模型

## 步骤

1. **加载 ch03 工作流**，找到 `Load Checkpoint` 节点，确认它有三个输出圆点：MODEL / CLIP / VAE。

2. **验证「没接的输出不影响出图」**：
   - 先把 VAE 那根线断开（选中线按 Delete），点 Queue Prompt
   - 观察出图颜色是否异常（发灰/发绿）——这说明 VAE 在起作用
   - 把线接回去（或从 `my_first_txt2img.json` 重新 Load 还原）

3. **验证三输出**：把鼠标悬停在三个输出圆点上，记下各自的类型名（MODEL / CLIP / VAE），填进记录表。

4. **练习刷新（R 键）**：
   - 记下当前 `ckpt_name` 下拉里有几个模型
   - 把一个 `.safetensors` 文件临时复制一份进 `checkpoints\` 目录（改个名，如 `test_copy.safetensors`）
   - 在 ComfyUI 界面按 `R`
   - 再看下拉列表，应该多出 `test_copy` —— 这就是刷新的作用
   - 验证完把临时文件删掉，再按 `R` 还原

5. **（可选）拆分加载体验**：如果你有单独的 VAE 文件放进 `models\vae\`，
   加一个 `Load VAE` 节点，把它的 VAE 输出接到 `VAE Decode`，替代 checkpoint 的 VAE。
   对比出图（能解决发灰问题）。

## 验收标准

- [ ] 能说出三个输出的类型名，填进记录表
- [ ] 断开 VAE 后观察到颜色变化，接回后恢复——理解了三输出各司其职
- [ ] 按 R 后新模型出现在列表——掌握了刷新

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 断开 VAE 线出图 | 颜色发灰/发绿 | 没有显影师解码，见 ch07 |
| 新模型文件放进目录但不刷新 | 列表里看不到 | ComfyUI 只在扫描时登记，见 ch05 5.3 |

## 可复现参数记录

| 输出端口 | 类型名 | 在 ch03 工作流里接到哪 |
|---|---|---|
| 输出1 | | |
| 输出2 | | |
| 输出3 | | |
| 刷新前模型数 / 刷新后 | / | |

## 常见问题

- 下拉列表看不到模型 → 检查路径 + 按 R，见 [ch05 5.3](../docs/ch05_loaders.md#c05-03)
- 出图颜色异常 → VAE 没接对，或换一个 VAE 试试
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

进入 [第 6 章 提示词与条件](../docs/ch06_conditioning.md)，搞清 CLIP 那根线（CONDITIONING）到底传的是什么。
