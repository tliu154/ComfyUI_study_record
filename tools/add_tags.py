#!/usr/bin/env python3
"""按标签规范给仓库所有笔记打标签（幂等，可重复运行）。

用法（任意目录执行均可）：
    python tools/add_tags.py

设计目标：
- 「之后新增的笔记」也能一键覆盖：按文件路径规则推断标签，章号映射 topic。
- 幂等：已有标签合并去重；同时会**清理**下方 REMOVE_TAGS 里的旧标签与 REMOVE_FIELDS 里的旧字段，
  所以改标签方案后重跑一次即可全库同步，不残留旧内容。

当前标签方案（2026-11-18 用户最新指定）：
- course：全部笔记 ``#course/ComfyUI``（用户明确要求大写，作为本仓库特例覆盖通用"小写"规范）
- type：docs → 笔记；tasks → 练习；README/SYLLABUS/CONTRIBUTING/NOTATION/篇README → 资料
- topic：按章号映射（见 TOPIC_BY_CH）
- source：教学笔记 → 官方文档
- 已移除：#statu/等待复习、#flag/重要、标签有哪些 字段
- _templates/ 跳过（模板是复制源，不打标签）
"""
from __future__ import annotations

import os
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().isoformat()

# 需要清除的旧标签（改方案后重跑一次即可从已打标的笔记里删掉）
REMOVE_TAGS = {"#course/计算机", "#statu/等待复习", "#flag/重要"}
# 需要清除的旧 frontmatter 字段（用户已移除的临时提醒字段）
REMOVE_FIELDS = ("标签有哪些",)

# 章号 → topic（单数、无空格；专有名词保留小写英文）
TOPIC_BY_CH: dict[str, str] = {
    "01": "基础", "02": "安装", "03": "工作流", "04": "节点", "05": "模型",
    "06": "提示词", "07": "潜空间", "08": "采样", "09": "图生图", "10": "局部重绘",
    "11": "放大", "12": "批处理", "13": "控制", "14": "参考图", "15": "提示词",
    "16": "节点", "17": "模型", "18": "模型", "19": "lora", "20": "工作流",
    "21": "视频", "22": "视频", "23": "多模态", "24": "节点", "25": "接口", "26": "性能",
}
APPENDIX_TOPIC = {"A": "节点", "B": "参数", "C": "排错", "D": "资源"}


def tags_for(rel: str) -> list[str] | None:
    """根据相对路径（正斜杠）推断标签列表；返回 None 表示跳过。"""
    rel = rel.replace("\\", "/")
    name = os.path.basename(rel)
    if "/_templates/" in f"/{rel}" or rel.startswith("_templates/"):
        return None

    tags: list[str] = ["#course/ComfyUI"]
    is_doc = "/docs/" in f"/{rel}"
    is_task = "/tasks/" in f"/{rel}"

    # type
    if is_doc:
        tags.append("#type/笔记")
    elif is_task:
        tags.append("#type/练习")
    else:
        tags.append("#type/资料")

    # topic：按章号或附录字母
    m = re.search(r"ch(\d{2})", name)
    if m:
        ch = m.group(1)
        topic = TOPIC_BY_CH.get(ch)
        if topic:
            tags.append(f"#topic/{topic}")
    else:
        ma = re.search(r"app([A-D])_", name)
        if ma:
            tags.append(f"#topic/{APPENDIX_TOPIC[ma.group(1)]}")

    # source：教学笔记依据官方文档
    if is_doc:
        tags.append("#source/官方文档")

    return tags


def split_frontmatter(text: str) -> tuple[list[str], list[str]]:
    """返回 (frontmatter 行, 正文行)。无 frontmatter 时前者为空。"""
    lines = text.split("\n")
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return lines[1:i], lines[i + 1:]
    return [], lines


def merge_tags(fm: list[str], wanted: list[str]) -> list[str]:
    """重写 frontmatter：应用 wanted 标签、清除 REMOVE_TAGS / REMOVE_FIELDS，
    保留其它字段（如 created），返回重写后的 frontmatter 行。"""
    existing: list[str] = []
    out: list[str] = []
    in_tags = False
    for line in fm:
        stripped = line.strip()
        if re.match(r"^tags\s*:", stripped):
            in_tags = True
            continue
        if in_tags:
            if stripped.startswith("- "):
                existing.append(stripped[2:].strip().strip('"').strip("'"))
                continue
            elif stripped == "":
                continue
            else:
                in_tags = False
        # 清除用户已移除的临时字段
        if any(re.match(rf"^{field}\s*:", stripped) for field in REMOVE_FIELDS):
            continue
        out.append(line)

    # 合并：wanted 优先，再补已有标签里没重复的；过滤掉待清除旧标签
    merged: list[str] = []
    for t in wanted + existing:
        if t and t not in merged and t not in REMOVE_TAGS:
            merged.append(t)

    # 重建 tags 块，放在最前
    new_fm = ["tags:"] + [f'  - "{t}"' for t in merged]

    # 保留 created（缺则补）；不再添加"标签有哪些"
    joined = "\n".join(out)
    if not re.search(r"^created\s*:", joined, re.M):
        new_fm.append(f"created: {TODAY}")

    return new_fm + out


def process(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    wanted = tags_for(rel)
    if wanted is None:
        return False
    text = path.read_text(encoding="utf-8")
    fm, body = split_frontmatter(text)
    new_fm = merge_tags(fm, wanted)
    new_text = "---\n" + "\n".join(new_fm) + "\n---\n" + "\n".join(body)
    if new_text != text:
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(new_text)
        return True
    return False


def main() -> int:
    changed = 0
    skipped = 0
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if tags_for(rel) is None:
            skipped += 1
            continue
        if process(path):
            changed += 1
            print("  +", rel)
    print(f"\n完成：{changed} 个文件更新/确认，{skipped} 个模板跳过。重复运行无副作用。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
