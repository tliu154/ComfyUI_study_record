---
tags:
  - "#course/ComfyUI"
  - "#type/资料"
created: 2026-11-18
---
# 新增章节规范

给自己看的约定。加一章走 5 步，保证整个仓库风格统一、链接不烂、随时能自检。

**状态只改 [SYLLABUS.md](SYLLABUS.md)**，篇 README 和根 README 不重复维护章节清单。
术语与节点名见 [NOTATION.md](NOTATION.md)。

## 0. Obsidian / GitHub 双兼容约定

- 一律 `.md`，UTF-8，相对超链（不要绝对路径、不要用 `[[wikilink]]`），这样 GitHub 和 Obsidian 都能点开
- **不打 tags**：frontmatter 省略或留空，tag 由自己按需加
- 章节互引用相对 Markdown 链接，例：`[ch08](01_core_nodes/docs/ch08_ksampler.md)`
- 锚点引用用显式 ID（见下），不依赖 GitHub 自动 slug

## 0.5 标签规范（每篇必打）

沿用知识库标签规范（权威源 `D:\我的知识库\README.md`），**每篇笔记 frontmatter 都要有 `tags:`**：

```markdown
---
tags:
  - "#course/ComfyUI"
  - "#type/笔记"
  - "#topic/采样"
  - "#source/官方文档"
created: YYYY-MM-DD
---
```

规则：层级 `英文/中文/中文`、无空格、最多 3 层、统一单数；标签带引号带 `#`。
本仓库取值（2026-11-18 用户最新指定）：

| 类别 | 本仓库取值 |
|---|---|
| `#course/` | 一律 `ComfyUI`（用户明确指定大写，作为本仓库特例覆盖通用"小写"规范）|
| `#type/` | docs → `笔记`；tasks → `练习`；框架/README → `资料` |
| `#topic/` | 按章号映射（ch08 采样 / ch09 图生图 …），见 `tools/add_tags.py` 的 `TOPIC_BY_CH` |
| `#source/` | 教学笔记 → `官方文档` |

**已移除**（用户 2026-11-18 指定，不要再出现）：`#statu/等待复习`、`#flag/重要`、以及
`标签有哪些: ...` 这个临时提醒字段。脚本会自动清理这些旧内容。

**不要手动逐个加标签**：写完一批笔记后跑 `python tools/add_tags.py`，它按路径规则自动打、
幂等（重跑无副作用）、清理旧标签，并保留 `created` 等其它 frontmatter 字段。
`_templates/` 是复制源，跳过不打。

## 1. 命名：全局章号

```
<篇目录>/docs/chNN_<短名>.md     教学
<篇目录>/tasks/chNN_task.md      实操任务
```

- `NN` 是 [SYLLABUS.md](SYLLABUS.md) 里分配的**两位章号**，全仓库唯一
- 章号不随篇移动而变；跨篇搬文件时不用改名
- 教学和实操**同号**，一眼对上

| 篇目录 | 章号范围 |
|---|---|
| `00_getting_started/` | 01~03 |
| `01_core_nodes/` | 04~08 |
| `02_image_workflow/` | 09~12 |
| `03_control_and_refine/` | 13~16 |
| `04_models_and_lora/` | 17~20 |
| `05_video_and_advanced/` | 21~23 |
| `06_ecosystem/` | 24~26 |
| `90_appendix/` | `app[A-D]_*.md` |

## 2. 写章节（`_templates/chapter_template.md`）

> 模板里的链接是**占位**，复制后逐个替换；`verify_all.py` 自动跳过 `_templates/`。

必须有的三样：

1. **本章子概念索引置顶** —— 每个概念链到对应小节的显式锚点
2. **一个概念一个三级标题** —— `### 8.2 seed / steps / CFG`，标题前单独一行 `<a id="c08-02"></a>`
3. **每节四段模板** —— 见下

### 锚点规则（重要）

中文 + 括号 + 英文的标题，GitHub 自动生成的 slug 会被吞括号、中英混排易变，
**禁止在索引里链自动锚点**。统一：

```markdown
<a id="c08-02"></a>
### 8.2 seed / steps / CFG 三兄弟
```

索引里写 `[seed / steps / CFG](#c08-02)`。
ID 格式 `c<章号>-<节号>`，分配后不改；删节保留占位并标「已合并」。

### 单节四段（`_templates/concept_section.md`）

```
概念定义 → 直觉类比 → 界面/参数 → 常见误区
（节末）对应实操链接 · 够用边界 · 和已有认知的差异
```

取舍说明：

- **直觉类比必备**：符号/术语第一次出现配「读法 / 人话」；基础薄弱优先，先懂「在干嘛」再谈原理
- **界面/参数写清**：节点名、端口名、控件名按 [NOTATION.md](NOTATION.md) 统一，写清在哪个菜单找得到
- **实操不在每节重复** —— 每章一份 `chNN_task.md`，节内只放 `[实操](...)` 链接
- **原理可跳过**：需要深入时链到附录或官方文档，正文不堆大段推导

### 够用边界（每节标一句）

写清「学到哪就够、什么可以跳过」，例如：
> **够用边界**：会用 denoise 控制改动幅度即可；去噪的数学推导可跳过，链 [官方文档](https://docs.comfy.org/)。

### 章节头模板

```markdown
# 第 N 章 中文名（English Name）

> 前置：第 X 章（链接） ｜ 对应实操：[`chNN_task.md`](../tasks/chNN_task.md)
> 状态：`[待写/部分完成/已完成]` ｜ 所属篇：`XX/`

**一句话**：<用一句话说清这章在干嘛>

> 本篇一条线：上一章（链）→ 本章 → 下一章（链）。

## 本章子概念索引
| 概念 | 小节 |
|---|---|
| [xxx](#cNN-01) | N.1 |
...
```

## 3. 写实操任务（`_templates/task_template.md`）

1. 顶部写清：任务目标、对应章节、预计耗时、前提（已装好/已下载什么）
2. 步骤编号，每一步可照做；关键参数给出**可复现值**（模型、seed、steps、CFG、尺寸）
3. 验收标准：如何判断做对了（出图/节点连线状态）
4. 「改一改会怎样」小实验：至少 1 个变量对照
5. 常见问题链到 [appC 故障排查](90_appendix/docs/appC_troubleshooting.md)
6. 不依赖仓库外大文件；模型与工作流文件记路径 + 来源链接，不入库

## 4. 校验（不能跳过）

在仓库根目录跑（脚本按自身位置推断仓库根）：

```bash
python tools/verify_all.py
```

任一检查失败，退出码 1。脚本做两件事：

| 检查项 | 做法 |
|---|---|
| 相对链接 | 检查所有 `.md` 的链接目标存在；跳过围栏代码块与行内代码；`http(s)` 外链不查 |
| 显式锚点 | 检查 `#cNN-MM` 链接在目标文件里确有 `<a id="cNN-MM"></a>` |

另外人工检查一次：

- [ ] 子概念索引里每个链接都能跳到对应 `<a id>`
- [ ] **无非标准锚点链接**：`grep -n '](#' 新文档.md | grep -v '#c'` 应为空
- [ ] 章号、文件名、实操文件三者一致
- [ ] 节点名/端口名与 [NOTATION.md](NOTATION.md) 一致
- [ ] 没有重复定义同一个概念（先在 SYLLABUS 里搜一遍）

## 5. 更新状态

- [SYLLABUS.md](SYLLABUS.md)：该章状态改 `[已完成]`，填实际文件列
- 根 README：只更新「进度」里的汇总
- 一篇收口时，在该篇 README 补一句实际产出

## 提交习惯

- 一章一个 commit：`add ch08: KSampler 参数全解教学与实操`
- **例外**：一章的教学 + 实操 + 状态文件一起改时，合成一个 commit 并写清章号章名
- 框架类改动单独 commit：`docs: 搭建 ComfyUI 教学框架`
