#!/usr/bin/env python3
"""Generate hot.md and the homepage Hot Cache preview from Wiki frontmatter.

The GitHub Pages repository is the projection source for existing Wiki content;
new shared-brain pages are projected here before this compiler runs.
"""
from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

REPO = Path(__file__).resolve().parent
HOT = REPO / "hot.md"
INDEX = REPO / "index.html"
SCAN_ROOTS = ("concepts", "projects", "entities", "raw")
START = "<!-- HOT_CACHE_ITEMS_START -->"
END = "<!-- HOT_CACHE_ITEMS_END -->"
MAX_ITEMS = 12


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        return {}, text
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"')
    return values, parts[2].lstrip("\n")


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value[:10])
    except (TypeError, ValueError):
        return None


def title_from_body(body: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def collect(today: date) -> list[dict[str, str]]:
    cutoff = today - timedelta(days=6)
    entries: list[dict[str, str]] = []
    for root_name in SCAN_ROOTS:
        root = REPO / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            if path.name.lower() in {"readme.md", "hot.md"}:
                continue
            front, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            changed = parse_date(front.get("updated")) or parse_date(front.get("date"))
            if changed is None or changed < cutoff:
                continue
            rel = path.relative_to(REPO).as_posix()
            title = front.get("title") or title_from_body(body, path.stem)
            summary = front.get("summary") or "現行 Wiki 條目"
            entries.append({"date": changed.isoformat(), "path": rel, "title": title, "summary": summary})
    entries.sort(key=lambda x: (x["date"], x["path"]), reverse=True)
    return entries[:MAX_ITEMS]


def render_hot(entries: list[dict[str, str]]) -> str:
    latest = max((x["date"] for x in entries), default=date.today().isoformat())
    lines = [
        "---",
        'title: "Hot Cache — 近 7 天動態焦點"',
        "type: log",
        f"date: {latest}",
        f"updated: {latest}",
        "tags: [hot, summary, digest]",
        f'summary: "依 Wiki 條目 frontmatter 編譯近 7 天活躍條目，共 {len(entries)} 項。"',
        "status: active",
        "---",
        "",
        "# 🔥 Hot Cache — 近 7 天動態焦點",
        "",
        "> 由 `compile_hot_cache.py` 根據 Wiki repo 內各條目的 `updated/date` deterministic 編譯；沒有日期的條目不納入，不以檔案時間猜測更新。",
        "",
        "## 近期活躍焦點 (Active Threads)",
        "",
    ]
    if not entries:
        lines.append("- 近 7 天沒有具備可驗證 frontmatter 日期的更新條目。")
    for item in entries:
        lines.append(f"- {item['date']} — [{item['title']}]({item['path']})")
    lines.extend(["", "## 條目摘要 (Verified Metadata)", ""])
    for item in entries:
        lines.append(f"- **{item['title']}**：{item['summary']}（{item['date']}）")
    lines.append("")
    return "\n".join(lines)


def render_preview(entries: list[dict[str, str]]) -> str:
    indent = "          "
    lines = [indent + START, indent + '<ul class="news-list">']
    for item in entries[:5]:
        path = item["path"]
        lines.extend([
            indent + "  <li>",
            indent + f'    <a href="viewer.html?file={path}">{item["title"]}</a>',
            indent + f'    <span class="news-date">{item["date"][5:]}</span>',
            indent + "  </li>",
        ])
    if not entries:
        lines.append(indent + "  <li>近 7 天沒有具備可驗證日期的更新條目。</li>")
    lines.extend([indent + "</ul>", indent + END])
    return "\n".join(lines)


def main() -> int:
    today = date.today()
    entries = collect(today)
    if not entries:
        raise SystemExit("HOT_CACHE_BLOCKED no_dated_entries=true")
    HOT.write_text(render_hot(entries), encoding="utf-8", newline="\n")
    raw_index = INDEX.read_bytes()
    newline = "\r\n" if b"\r\n" in raw_index else "\n"
    html = raw_index.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if not pattern.search(html):
        raise SystemExit("HOT_CACHE_BLOCKED homepage_markers_missing=true")
    updated = pattern.sub(render_preview(entries), html, count=1)
    INDEX.write_bytes(updated.replace("\n", newline).encode("utf-8"))
    print(f"HOT_CACHE_OK entries={len(entries)} latest={entries[0]['date']}")
    for item in entries[:5]:
        print(f"HOT_ITEM {item['date']} {item['path']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
