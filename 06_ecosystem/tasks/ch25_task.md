---
tags:
  - "#course/ComfyUI"
  - "#type/练习"
  - "#topic/接口"
created: 2026-11-18
---
# 实操 25：导出 API 格式，用脚本批量改 seed

> 对应章节：[第 25 章 API 与自动化](../docs/ch25_api_automation.md) ｜ 预计耗时：45 分钟
> 状态：`[已完成]`

## 目标

把一条文生图工作流导出成 API 格式，看懂它的结构，
再用一小段 Python 脚本改 `seed` 批量提交 3 个任务，理解「程序化出图」的最小闭环。
**不要求写出健壮的生产脚本，跑通一次、看懂改了哪里即可。**

## 前提

- [ ] 会搭并跑通 SD1.5 文生图（ch03），见 [ch03](../../00_getting_started/docs/ch03_first_workflow.md)
- [ ] ComfyUI 在本机 `127.0.0.1:8188` 运行
- [ ] Python 环境装了 `requests`（`pip install requests`）
- [ ] 前置概念：两种 JSON 格式的区别，见 [ch25 25.1](../docs/ch25_api_automation.md#c25-01)

## 步骤

1. **开开发者模式**：`Settings`（齿轮）→ 勾选 **Enable Dev mode Options**。

2. **导出 API 格式**：确认当前工作流能正常出图 → 工作流菜单 → **Export (API)** → 存为 `workflow_api.json`。

3. **看懂结构**：用文本编辑器打开，找到 `class_type` 为 `KSampler` 的那条，记下：
   - 它的节点 id：________（例 `"3"`）
   - `inputs` 里的 `seed` 字段：________
   - 确认这是 API 格式（有 `class_type`/`inputs`，不是画布坐标），见 [25.1](../docs/ch25_api_automation.md#c25-01)。

4. **写脚本批量改 seed**：在 `workflow_api.json` 同目录建 `batch.py`：
   ```python
   import requests, json, copy

   prompt = json.load(open("workflow_api.json", encoding="utf-8"))
   KS_ID = "3"   # 改成你在第 3 步记下的 KSampler 节点 id

   for seed in [1, 2, 3]:
       p = copy.deepcopy(prompt)
       p[KS_ID]["inputs"]["seed"] = seed
       r = requests.post(
           "http://127.0.0.1:8188/prompt",
           json={"prompt": p},
       )
       print(seed, r.status_code, r.json())
   ```
   - 把 `KS_ID` 换成你自己的节点 id。

5. **运行并观察**：`python batch.py`。
   - ComfyUI 队列里应出现 3 个任务依次执行；`output/` 目录多出 3 张图。
   - 终端每个 `print` 应看到 `200` 和一个 `prompt_id`。

6. **核对结果**：打开 `output/` 里 3 张图，确认它们是**同提示词不同 seed** 的结果（构图/细节不同）。

## 验收标准

- [ ] 导出的是 API 格式（结构为 `{"id": {"class_type", "inputs"}}`）
- [ ] 能在 JSON 里定位 KSampler 的节点 id 和 `seed` 字段
- [ ] 脚本成功提交 3 个任务，ComfyUI 队列执行，`output/` 出现 3 张不同图
- [ ] 能说清「脚本改的是 JSON 里哪个字段」对应「手动改的是界面上哪个框」

## 改一改会怎样（小实验）

| 改动 | 预期现象 | 为什么 |
|---|---|---|
| 用 UI 格式 JSON 发 `/prompt` | 报错 | /prompt 只收 API 格式，见 ch25 25.1 |
| `KS_ID` 填错（写成别的节点 id） | 图不按 seed 变/报错 | 改错了节点，见 ch25 25.3 |
| 把 `steps` 一起改成 5 | 出图变快、质量降 | 改 `inputs` 里任意参数都生效，见 ch25 25.3 |
| 提交时 ComfyUI 没开 | 连接失败 | /prompt 是本机后端接口，见 ch25 25.3 |

## 可复现记录

| 项 | 值 |
|---|---|
| KSampler 节点 id | |
| 改的参数 / 值 | seed = 1, 2, 3 |
| 提交接口 | `http://127.0.0.1:8188/prompt` |
| 出图数量 / 目录 | 3 张 / `output/` |

## 常见问题

- 导出菜单没有 `Export (API)` → 开发者模式没开，回第 1 步
- 报 `prompt 格式错误` → 用了 UI 格式，重新用 `Export (API)` 导出，见 [25.1](../docs/ch25_api_automation.md#c25-01)
- 图没按 seed 变 → `KS_ID` 填错，回到 JSON 里核对 KSampler 的 id，见 [25.3](../docs/ch25_api_automation.md#c25-03)
- 想在别的机器/云端跑 → 用同一份 API 格式，见 [25.4](../docs/ch25_api_automation.md#c25-04)
- 其它 → [附录 C 故障排查](../../90_appendix/docs/appC_troubleshooting.md)

## 下一步

脚本化搞定后，进入 [第 26 章 性能与显存优化](../docs/ch26_performance.md)（选读）——
解决「跑得动、跑得快」的问题。
