#!/usr/bin/env python3
"""修复失效的相对链接：当链接目标的文件名在仓库中唯一存在、只是相对路径写错时，
自动改写为正确的相对路径。默认 dry-run 只打印，加 --apply 才写回。

用法：
    python tools/fix_links.py           # 预览将要修复的链接
    python tools/fix_links.py --apply   # 实际写回

配合 verify_all.py 使用：本脚本修路径写错，verify_all.py 查锚点与残留失效链接。
"""
from __future__ import annotations

import os
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_CODE_RE = re.compile(r"`[^`]*`")
# 外链 / 邮件 / 纯锚点前缀
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "data:")


def strip_code(text: str) -> str:
    return INLINE_CODE_RE.sub("", FENCE_RE.sub("", text))


def md_files() -> list[Path]:
    return sorted(
        p for p in ROOT.rglob("*.md")
        if ".git" not in p.parts and "_templates" not in p.parts and "tools" not in p.parts
    )


def main() -> int:
    apply = "--apply" in sys.argv
    files = md_files()

    # 文件名 -> 文件列表（用于按 basename 找唯一目标）
    by_name: dict[str, list[Path]] = defaultdict(list)
    for p in files:
        by_name[p.name].append(p)

    # 收集修复建议：(源文件, 原target, 新target)
    fixes: list[tuple[Path, str, str]] = []
    # 目标文件名在仓库中找不到或不唯一，无法自动修
    unresolved: list[str] = []

    for f in files:
        text = strip_code(f.read_text(encoding="utf-8"))
        for target in LINK_RE.findall(text):
            path_part, sep, anchor = target.partition("#")
            path_part = path_part.strip().strip("<>")
            if not path_part or path_part.startswith(SKIP_PREFIX):
                continue
            resolved = (f.parent / path_part).resolve()
            if resolved.exists():
                continue  # 链接本来就对

            name = Path(path_part).name
            candidates = by_name.get(name, [])
            if len(candidates) == 1:
                rel = os.path.relpath(candidates[0], f.parent).replace("\\", "/")
                new_target = rel + ("#" + anchor if sep else "")
                fixes.append((f, target, new_target))
            else:
                unresolved.append(
                    f"{f.relative_to(ROOT)} -> {target}（同名候选 {len(candidates)} 个）"
                )

    # 按文件分组打印
    by_file: dict[Path, list[tuple[str, str]]] = defaultdict(list)
    for f, old, new in fixes:
        by_file[f].append((old, new))

    print(f"扫描 {len(files)} 个 md 文件。")
    print(f"可自动修复：{len(fixes)} 条链接，涉及 {len(by_file)} 个文件。\n")
    for f, items in by_file.items():
        print(f"  {f.relative_to(ROOT)}")
        for old, new in items:
            print(f"     - {old}")
            print(f"     + {new}")
    if unresolved:
        print(f"\n无法自动修复（同名 0 或多个）：{len(unresolved)} 条")
        for u in unresolved:
            print("   ·", u)

    if not apply:
        print("\n[dry-run] 未写回。确认无误后加 --apply 执行。")
        return 0

    # 写回：对每个文件做精确字符串替换
    changed = 0
    for f, items in by_file.items():
        raw = f.read_text(encoding="utf-8")
        for old, new in items:
            raw = raw.replace(f"]({old})", f"]({new})")
        f.write_text(raw, encoding="utf-8")
        changed += 1
    print(f"\n[apply] 已写回 {changed} 个文件。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
