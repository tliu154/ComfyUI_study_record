---
tags:
  - "#course/计算机"
  - "#type/练习"
  - "#statu/等待复习"
  - "#topic/安装"
created: 2026-11-18
标签有哪些: "#type #course #statu #flag #topic #source"
---
# 实操 02：装好并启动 ComfyUI

> 对应章节：[第 2 章 安装与启动](../docs/ch02_installation.md) ｜ 预计耗时：20~40 分钟
> 状态：`[已完成]`
> 路线：本任务以**新手推荐的 Windows 便携包**为主线；云端用户看文末「云端分支」。

## 目标

ComfyUI 能启动，浏览器打开 `http://localhost:8188` 能看到画布（哪怕画布上还没有模型）。

## 前提

- [ ] 已按 [`ch01_task.md`](ch01_task.md) 查过显卡/显存，确定走本地路线
- [ ] 网络能访问 GitHub（下载便携包）

## 步骤

1. **下载便携包**：到官方仓库 Releases / README 找 Windows Portable 压缩包（入口见 [附录 D](../../90_appendix/docs/appD_resources.md)），下载 `.zip`。

2. **解压到无中文路径**：例如 `D:\ComfyUI\`。
   > ⚠️ 路径不要有中文、空格、特殊符号。这是最常见的启动失败原因。

3. **下载一个测试模型**（本步先完成，ch03 会用到）：
   - 下载 SD1.5 模型 `v1-5-pruned-emaonly-fp16.safetensors`（来源见 [附录 D](../../90_appendix/docs/appD_resources.md)）
   - 放进 `ComfyUI_windows_portable\ComfyUI\models\checkpoints\`

4. **启动**：双击解压目录里的 `run_nvidia_gpu.bat`，等命令行窗口出现 `http://127.0.0.1:8188` 字样。

5. **打开界面**：浏览器访问 `http://localhost:8188`，应该看到画布（默认会有一张预置工作流）。

6. **验证模型被识别**：在画布上找到 `Load Checkpoint` 节点，点开 `ckpt_name` 下拉，能看到刚放进去的模型名。

### 云端分支（无独显 / Mac）

- 打开 `cloud.comfy.org` → 登录 → 选 Z-Image-Turbo 文生图模板 → 能进到画布即达标
- 模型由平台提供，跳过第 3 步

## 验收标准

- [ ] 浏览器打开 `localhost:8188` 能看到 ComfyUI 画布
- [ ] `Load Checkpoint` 的 `ckpt_name` 列表里能看到你的模型（本地路线）
- [ ] 命令行窗口没有红色报错

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 把模型文件临时移出 checkpoints 目录，按 `R` 刷新 | 下拉列表里模型消失 | 列表来自目录扫描，不是记忆 |

（做完把模型放回去，再按 `R`）

## 可复现参数记录

| 项 | 值 |
|---|---|
| 安装路线 | （便携包 / 桌面版 / 源码 / 云端）|
| 安装路径 | （填写，确认无中文）|
| 模型文件名 | |
| 启动方式 | |
| 浏览器地址 | `http://localhost:8188` |

## 常见问题

- 黑窗口一闪而过 / 打不开网页 / 看不到模型 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)
- 下载太慢 → 换网络或镜像源；模型约 2~4GB，耐心等
- 其它安装方式（桌面版 / 源码 / comfy-cli）→ 回看 [ch02 2.1~2.3](../docs/ch02_installation.md#c02-01)

## 下一步

进入 [第 3 章 第一个工作流](../docs/ch03_first_workflow.md)，从空画布亲手搭出文生图。
