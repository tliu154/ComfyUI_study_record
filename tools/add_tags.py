#!/usr/bin/env python3
"""按标签规范给仓库所有笔记打标签（幂等，可重复运行）。

用法（任意目录执行均可）：
    python tools/add_tags.py

设计目标：
- 「之后新增的笔记」也能一键覆盖：按文件路径规则推断标签，章号映射 topic。
- 幂等：已有标签只合并去重，不重复添加；保留 frontmatter 里其它字段。
- 遵循用户标签规范：英文/中文/中文、小写、无空格、最多3层、单数。
  标签一律写成 ``  - "#a/b"``（带引号带 #，YAML 里 # 必须引号包裹）。

标签方案（本仓库）：
- course：全部笔记 ``#course/计算机``
- type：docs → 笔记；tasks → 练习；README/SYLLABUS/CONTRIBUTING/NOTATION/篇README → 资料
- statu：教学/实操笔记 → 等待复习（框架文件不标）
- topic：按章号映射（见 TOPIC_BY_CH）
- flag：重点章的教学 → 重要（ch03/ch04/ch08）
- source：教学笔记 → 官方文档（本仓库内容依据）
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
HINT = '"#type #course #statu #flag #topic #source"'

# 章号 → topic（小写、单数、无空格；专有名词保留小写英文）
TOPIC_BY_CH: dict[str, str] = {
    "01": "基础", "02": "安装", "03": "工作流", "04": "节点", "05": "模型",
    "06": "提示词", "07": "潜空间", "08": "采样", "09": "图生图", "10": "局部重绘",
    "11": "放大", "12": "批处理", "13": "控制", "14": "参考图", "15": "提示词",
    "16": "节点", "17": "模型", "18": "模型", "19": "lora", "20": "工作流",
    "21": "视频", "22": "视频", "23": "多模态", "24": "节点", "25": "接口", "26": "性能",
}
APPENDIX_TOPIC = {"A": "节点", "B": "参数", "C": "排错", "D": "资源"}
IMPORTANT_CH = {"03", "04", "08"}


def tags_for(rel: str) -> list[str] | None:
    """根据相对路径（正斜杠）推断标签列表；返回 None 表示跳过。"""
    rel = rel.replace("\\", "/")
    name = os.path.basename(rel)
    if "/_templates/" in f"/{rel}" or rel.startswith("_templates/"):
        return None

    tags: list[str] = ["#course/计算机"]
    is_doc = "/docs/" in f"/{rel}"
    is_task = "/tasks/" in f"/{rel}"

    # type
    if is_doc:
        tags.append("#type/笔记")
    elif is_task:
        tags.append("#type/练习")
    else:
        tags.append("#type/资料")

    # statu：仅教学/实操笔记
    if is_doc or is_task:
        tags.append("#statu/等待复习")

    # topic：按章号或附录字母
    m = re.search(r"ch(\d{2})", name)
    if m:
        ch = m.group(1)
        topic = TOPIC_BY_CH.get(ch)
        if topic:
            tags.append(f"#topic/{topic}")
        if is_doc and ch in IMPORTANT_CH:
            tags.append("#flag/重要")
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
    """把 wanted 合并进 frontmatter：保留已有 tags（去重+保持顺序），去掉 tags 块，
    返回重写后的 frontmatter 行。"""
    existing: list[str] = []
    out: list[str] = []
    in_tags = False
    has_tags_key = False
    for line in fm:
        stripped = line.strip()
        if re.match(r"^tags\s*:", stripped):
            in_tags = True
            has_tags_key = True
            continue
        if in_tags:
            if stripped.startswith("- "):
                existing.append(stripped[2:].strip().strip('"').strip("'"))
                continue
            elif stripped == "":
                continue
            else:
                in_tags = False
        out.append(line)

    # 合并：wanted 优先，再补已有标签里没重复的
    merged: list[str] = []
    for t in wanted + existing:
        if t and t not in merged:
            merged.append(t)

    # 重建 tags 块，放在最前
    tag_block = ["tags:"] + [f'  - "{t}"' for t in merged]

    # 保留 created / 标签有哪些 字段习惯；缺则补
    joined = "\n".join(out)
    if not re.search(r"^created\s*:", joined, re.M):
        tag_block.append(f"created: {TODAY}")
    if not re.search(r"^标签有哪些\s*:", joined, re.M):
        tag_block.append(f"标签有哪些: {HINT}")

    return tag_block + out


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
