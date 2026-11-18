#!/usr/bin/env python3
"""全仓库自检：相对链接 + 显式锚点。

用法（任意目录执行均可，脚本按自身位置推断仓库根）：
    python tools/verify_all.py

检查项：
1. 所有 .md 的相对链接目标是否存在（跳过 _templates/、外链 http(s)、锚点、mailto）
2. 所有 #cNN-MM 形式的锚点链接，在目标文件里确有 <a id="cNN-MM"></a>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 匹配 Markdown 链接 [text](target)，忽略图片 ![]()
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
ANCHOR_RE = re.compile(r"<a\s+id=\"([^\"]+)\"\s*></a>")
# 只校验 cNN-MM 这类显式锚点
C_ANCHOR_RE = re.compile(r"^c\d{2}-\d{2}$")
# 框架阶段：预定但尚未开写的章节文件，链接失效属正常
PLANNED_RE = re.compile(r"(^|/)(ch\d{2}_[^/]*\.md|app[A-D]_[^/]*\.md)$")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")


def strip_code(text: str) -> str:
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return text


def md_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and "_templates" not in p.parts
    )


def split_target(target: str) -> tuple[str, str]:
    """拆成 (路径部分, 锚点部分)。"""
    target = target.strip().strip("<>")
    if "#" in target:
        path, anchor = target.split("#", 1)
        return path, anchor
    return target, ""


def main() -> int:
    errors: list[str] = []
    planned: list[str] = []
    files = md_files()

    # 仓库内所有 md 的文件名集合：用于区分「真·未写的预定章节」与「路径写错的已存在章节」
    names_present = {f.name for f in files}

    # 预建每个文件的显式锚点集合（忽略代码块里的示例锚点）
    anchors_by_file: dict[Path, set[str]] = {}
    id_counts: dict[tuple[Path, str], int] = {}
    for f in files:
        text = strip_code(f.read_text(encoding="utf-8"))
        ids = ANCHOR_RE.findall(text)
        anchors_by_file[f] = set(ids)
        for i in ids:
            id_counts[(f, i)] = id_counts.get((f, i), 0) + 1

    for f in files:
        raw = f.read_text(encoding="utf-8")
        text = strip_code(raw)
        for target in LINK_RE.findall(text):
            path_part, anchor = split_target(target)
            # 外链、邮件、纯锚点跳过
            if path_part.startswith(("http://", "https://", "mailto:", "#")):
                continue
            if not path_part:
                # 同文件内锚点
                if anchor and C_ANCHOR_RE.match(anchor) and anchor not in anchors_by_file.get(f, set()):
                    errors.append(f"[锚点缺失] {f.relative_to(ROOT)} -> #{anchor}（本文件）")
                continue
            resolved = (f.parent / path_part).resolve()
            if not resolved.exists():
                norm = path_part.replace("\\", "/")
                target_name = norm.rstrip("/").split("/")[-1]
                # 只有当目标章节文件在仓库里还不存在时，才算「预定未写」；
                # 若同名文件已存在，则是相对路径写错，必须报错（fix_links.py 可一键修）。
                if PLANNED_RE.search(norm) and target_name not in names_present:
                    planned.append(f"{f.relative_to(ROOT)} -> {target}")
                    continue
                errors.append(f"[链接失效] {f.relative_to(ROOT)} -> {target}")
                continue
            if anchor and C_ANCHOR_RE.match(anchor):
                target_file = resolved if resolved.suffix == ".md" else None
                if target_file and anchor not in anchors_by_file.get(target_file, set()):
                    errors.append(f"[锚点缺失] {f.relative_to(ROOT)} -> {target}")

    # 重复锚点检查
    for (f, i), n in id_counts.items():
        if n > 1:
            errors.append(f"[锚点重复] {f.relative_to(ROOT)} 的 #{i} 出现 {n} 次")

    if planned:
        print(f"（框架阶段）{len(planned)} 条链接指向预定未写的章节文件，属正常：")
        for p in planned:
            print("   ·", p)
        print()

    if errors:
        print(f"FAIL：发现 {len(errors)} 个问题\n")
        for e in errors:
            print("  -", e)
        return 1

    print(f"ALL PASS：检查 {len(files)} 个 md 文件，相对链接与显式锚点均正常。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
