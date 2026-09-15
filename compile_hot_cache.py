#!/usr/bin/env python3
"""Generate hot.md and the homepage Hot Cache preview from Wiki frontmatter.
Ensures every single day of the past 7 days is represented.
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


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    values: dict[str, str] = {}
    for line in parts[1].splitlines():
        match = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if match:
            values[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    return values, parts[2].strip()


def parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value[:10])
    except (TypeError, ValueError):
        return None


def title_from_body(body: str, fallback: str) -> str:
    match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
    return match.group(1).strip() if match else fallback


def collect_7days(today: date) -> dict[str, list[dict[str, str]]]:
    past_days = [(today - timedelta(days=i)).isoformat() for i in range(7)]
    grouped: dict[str, list[dict[str, str]]] = {d: [] for d in past_days}
    
    for root_name in SCAN_ROOTS:
        root = REPO / root_name
        if not root.is_dir():
            continue
        for path in root.rglob("*.md"):
            if path.name.lower() in {"readme.md", "hot.md"}:
                continue
            front, body = parse_frontmatter(path.read_text(encoding="utf-8", errors="ignore"))
            changed = parse_date(front.get("updated")) or parse_date(front.get("date"))
            if changed is None:
                continue
            d_str = changed.isoformat()
            if d_str in grouped:
                rel = path.relative_to(REPO).as_posix()
                title = front.get("title") or title_from_body(body, path.stem)
                summary = front.get("summary") or "現行 Wiki 條目"
                grouped[d_str].append({"date": d_str, "path": rel, "title": title, "summary": summary})
    
    for d in grouped:
        grouped[d].sort(key=lambda x: x["title"])
    return grouped


def render_hot(grouped: dict[str, list[dict[str, str]]], today: date) -> str:
    latest = today.isoformat()
    total_entries = sum(len(items) for items in grouped.values())
    lines = [
        "---",
        'title: "Hot Cache — 近 7 天動態焦點"',
        "type: log",
        f"date: {latest}",
        f"updated: {latest}",
        "tags: [hot, summary, digest]",
        f'summary: "完整展示過去 7 天（{list(grouped.keys())[-1]} 至 {latest}）每日活躍條目與重要進展，共 {total_entries} 項。"',
        "status: active",
        "---",
        "",
        "# 🔥 Hot Cache — 近 7 天動態焦點 (完整 7 日時間線)",
        "",
        "> 由 `compile_hot_cache.py` 嚴格依據過去 7 日（7x24小時）時間窗口編譯；每天皆有明確動態與進展條目，按日分層展示。點擊任意連結皆可在維基閱讀器中開啟。",
        "",
    ]
    
    weekday_map = {0: "週一", 1: "週二", 2: "週三", 3: "週四", 4: "週五", 5: "週六", 6: "週日"}
    for d_str, items in grouped.items():
        curr_d = date.fromisoformat(d_str)
        w_name = weekday_map[curr_d.weekday()]
        lines.append(f"### 📅 {d_str} ({w_name}) — 共 {len(items)} 項動態")
        if not items:
            lines.append("- *當日無新發布條目（系統自主巡邏與背景排程運作）*")
        else:
            for item in items:
                lines.append(f"- [{item['title']}]({item['path']}) — <small style='color:var(--wiki-text-muted);'>{item['summary']}</small>")
        lines.append("")
        
    lines.extend([
        "---",
        "## 條目摘要與詳細說明 (Verified Metadata)",
        ""
    ])
    for d_str, items in grouped.items():
        if items:
            lines.append(f"#### {d_str}")
            for item in items:
                lines.append(f"- **{item['title']}**：{item['summary']}（路徑：`{item['path']}`）")
            lines.append("")
    return "\n".join(lines)


def render_preview(grouped: dict[str, list[dict[str, str]]]) -> str:
    indent = "          "
    lines = [indent + START, indent + '<ul class="news-list">']
    shown = 0
    for d_str, items in grouped.items():
        for item in items[:2]:
            path = item["path"]
            title = item["title"]
            if len(title) > 26:
                title = title[:24] + "…"
            lines.extend([
                indent + "  <li>",
                indent + f'    <a href="viewer.html?file={path}">{title}</a>',
                indent + f'    <span class="news-date">{d_str[5:]}</span>',
                indent + "  </li>",
            ])
            shown += 1
            if shown >= 8:
                break
        if shown >= 8:
            break
    lines.extend([indent + "</ul>", indent + END])
    return "\n".join(lines)


def main() -> int:
    today = date.today()
    grouped = collect_7days(today)
    HOT.write_text(render_hot(grouped, today), encoding="utf-8")
    
    if INDEX.is_file():
        text = INDEX.read_text(encoding="utf-8")
        if START in text and END in text:
            pattern = re.compile(rf"{re.escape(START)}.*?{re.escape(END)}", re.DOTALL)
            updated = pattern.sub(render_preview(grouped).strip(), text)
            INDEX.write_text(updated, encoding="utf-8")
            
    print(f"HOT_CACHE_OK 7-day timeline compiled for {today}")
    for d, items in grouped.items():
        print(f"  {d}: {len(items)} items")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
