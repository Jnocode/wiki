#!/usr/bin/env python3
"""Sync selected current Wiki pages from the canonical shared brain.

This is the GitHub Pages lane. NAS synchronization remains separate.
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import date, timedelta
from pathlib import Path

CANONICAL = Path("D:/Workspace/03_Dev_Projects/agent_office/shared/brain")
REPO = Path(__file__).resolve().parent
MAPPINGS = {
    "01_tech/agent-collaboration-contract.md": "concepts/agent-collaboration-contract.md",
    "01_tech/codex-context-management.md": "concepts/codex-context-management.md",
    "01_tech/data-source-integrity-and-fallback.md": "concepts/data-source-integrity-and-fallback.md",
    "90_system/workspace-architecture.md": "concepts/workspace-architecture.md",
    "90_system/runtime-environment-map.md": "concepts/runtime-environment-map.md",
    "04_media/podcast-current-production-contract.md": "concepts/podcast-current-production-contract.md",
    "04_media/discord-ai-digest-presentation.md": "concepts/discord-ai-digest-presentation.md",
}
RELATED = {
    "concepts/agent-collaboration-contract.md": [
        ("concepts/codex-context-management.md", "Codex 上下文管理"),
        ("concepts/data-source-integrity-and-fallback.md", "資料來源完整性"),
    ],
    "concepts/codex-context-management.md": [
        ("concepts/agent-collaboration-contract.md", "Agent 協作契約"),
        ("concepts/workspace-architecture.md", "Workspace 架構"),
    ],
    "concepts/data-source-integrity-and-fallback.md": [
        ("concepts/agent-collaboration-contract.md", "Agent 協作契約"),
        ("concepts/discord-ai-digest-presentation.md", "Discord AI 日報發布"),
    ],
    "concepts/workspace-architecture.md": [
        ("concepts/runtime-environment-map.md", "Runtime 環境圖"),
        ("concepts/agent-collaboration-contract.md", "Agent 協作契約"),
    ],
    "concepts/runtime-environment-map.md": [
        ("concepts/workspace-architecture.md", "Workspace 架構"),
        ("concepts/codex-context-management.md", "Codex 上下文管理"),
    ],
    "concepts/podcast-current-production-contract.md": [
        ("concepts/agent-collaboration-contract.md", "Agent 協作契約"),
        ("concepts/data-source-integrity-and-fallback.md", "資料來源完整性"),
    ],
    "concepts/discord-ai-digest-presentation.md": [
        ("concepts/data-source-integrity-and-fallback.md", "資料來源完整性"),
        ("concepts/agent-collaboration-contract.md", "Agent 協作契約"),
    ],
}


def frontmatter_and_body(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("source has no YAML frontmatter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("invalid YAML frontmatter delimiter")
    return parts[1], parts[2].lstrip("\n")


def field(front: str, name: str, default: str = "") -> str:
    match = re.search(rf"^{re.escape(name)}:\s*(.+)$", front, re.MULTILINE)
    return match.group(1).strip() if match else default


def render(source: Path, target_rel: str, today: date) -> str:
    front, body = frontmatter_and_body(source.read_text(encoding="utf-8"))
    title = field(front, "title", source.stem)
    source_date = field(front, "date", today.isoformat())
    tags = field(front, "tags", "[wiki]")
    summary = field(front, "summary", "現行 Wiki 知識頁")
    review_after = today + timedelta(days=30)
    related = "\n## 相關頁面\n\n" + "\n".join(
        f"- [[{path}|{label}]]" for path, label in RELATED[target_rel]
    ) + "\n"
    header = "\n".join(
        [
            "---",
            f"title: {title}",
            "type: concept",
            f"date: {source_date}",
            f"updated: {today.isoformat()}",
            f"tags: {tags}",
            f"summary: {summary}",
            f"source: [\"agent_office/shared/brain/{source.relative_to(CANONICAL).as_posix()}\"]",
            "confidence: high",
            f"review_after: {review_after.isoformat()}",
            "status: active",
            "---",
            "",
        ]
    )
    return header + body.rstrip() + "\n" + related


def sync(today: date) -> list[str]:
    changed: list[str] = []
    for source_rel, target_rel in MAPPINGS.items():
        source = CANONICAL / source_rel
        target = REPO / target_rel
        if not source.is_file():
            raise FileNotFoundError(source)
        rendered = render(source, target_rel, today)
        target.parent.mkdir(parents=True, exist_ok=True)
        old = target.read_text(encoding="utf-8") if target.exists() else None
        if old != rendered:
            target.write_text(rendered, encoding="utf-8", newline="\n")
            changed.append(target_rel)
    return changed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="只檢查來源是否可讀，不寫入")
    parser.add_argument("--date", default=date.today().isoformat())
    args = parser.parse_args()
    today = date.fromisoformat(args.date)
    if args.check:
        missing = [str(CANONICAL / src) for src in MAPPINGS if not (CANONICAL / src).is_file()]
        if missing:
            for item in missing:
                print(f"MISSING {item}")
            return 1
        print(f"CHECK_OK sources={len(MAPPINGS)}")
        return 0
    changed = sync(today)
    print(f"SYNC_OK pages={len(MAPPINGS)} changed={len(changed)}")
    for item in changed:
        print(f"UPDATED {item}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
