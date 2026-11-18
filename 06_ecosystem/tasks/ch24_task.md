---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/节点"
created: 2026-11-18
---
# 实操 24：装一个节点包，走通管理与缺失排查

> 对应章节：[第 24 章 Manager 与自定义节点](../docs/ch24_manager.md) ｜ 预计耗时：30 分钟
> 状态：`[已完成]`

## 目标

亲手用 Manager 装一个自定义节点包，验证重启生效，更新/卸载各走一遍，
最后演练一次「节点缺失 → 一键安装」的完整排查流程。

## 前提

- [ ] ComfyUI 已能启动（`localhost:8188` 打开正常）—— 见 [ch02](../../00_getting_started/docs/ch02_installation.md)
- [ ] Manager 已安装（顶部菜单有 `Manager`）；没有则按 [ch24 24.2](../docs/ch24_manager.md#c24-02) 先装
- [ ] 网络可访问节点包来源（GitHub / Comfy Registry）

## 步骤

1. **确认 Manager 在位**：打开 ComfyUI，看顶部菜单是否有 `Manager`。
   没有 → 按 [24.2](../docs/ch24_manager.md#c24-02) 手动 clone `ComfyUI-Manager` 到 `custom_nodes/` 并重启。

2. **搜索并装一个包**：`Manager → Custom Nodes Manager` → 搜索框输一个你听过或教程里用到的包
   （如 `Ultimate SD Upscale`、`ControlNet` 相关包；拿不准就装 Manager 推荐的热门包）→ 点 Install。
   - 记录包名（不是节点类名）：____________

3. **重启生效**：完全重启 ComfyUI（关掉进程再启动），浏览器 `Ctrl+F5` 强刷。
   在画布右键搜索节点，确认新包的节点出现了。

4. **走一遍更新**：`Custom Nodes Manager` 里对刚装的包点 Update（若有更新）。
   观察是否需要重启，重启后节点还在不在。

5. **演练缺失排查**：
   - 临时把刚装的包目录改名（`custom_nodes/<包名>` → `<包名>_bak`）模拟「缺失」，重启 ComfyUI
   - 打开一条用到该节点的工作流（或你之前存的工作流），看是否出现红色缺失节点 / Missing Nodes 提示
   - 用 `Manager → Install Missing Custom Nodes` 尝试一键安装，看能否恢复
   - 恢复后把 `_bak` 目录删掉（若一键装的是新副本，注意别留两份）

6. **（可选）卸载**：确认不需要后，Uninstall 该包并重启，画布搜索不到对应节点即成功卸载。
   若还要用，装回去即可。

## 验收标准

- [ ] 能通过 Manager 搜索并安装一个节点包，重启后在画布搜到其节点
- [ ] 更新/卸载操作各走一遍，理解「重启才生效」
- [ ] 能制造并识别「节点缺失」，用一键安装恢复，或说出手动兜底步骤

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 装完包不重启，直接搜节点 | 搜不到新节点 | 节点包在启动时才加载，见 ch24 24.2 |
| 把节点包目录改名后打开工作流 | 出现红色缺失节点 | 工作流依赖的节点代码找不到，见 ch24 24.3 |
| 无脑 Update All 后再打开老工作流 | 有概率节点报错/行为变化 | 更新可能改节点接口，见 ch24 24.4 |

## 可复现记录

| 项 | 值 |
|---|---|
| ComfyUI 版本 / 启动方式 | |
| 安装的包名 + 来源 | |
| 是否需重启生效 | 是/否 |
| 缺失排查结果 | 一键恢复 / 手动兜底 |

## 常见问题

- 搜索不到包 → 可能在默认索引外，找 GitHub 仓库地址用 URL 安装，见 [ch24 24.2](../docs/ch24_manager.md#c24-02)
- 装完节点不出现 → 没重启 / 浏览器缓存，重启 + `Ctrl+F5`
- 一键安装失败 → 冷门包或依赖冲突，手动查包名与仓库，见 [ch24 24.3](../docs/ch24_manager.md#c24-03)
- 报错是「模型缺失」而非节点 → 那是另一类问题，见 [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

节点管理搞定后，进入 [第 25 章 API 与自动化](ch25_api_automation.md)（选读）——
了解怎么把手动点的流程变成脚本批量跑。
