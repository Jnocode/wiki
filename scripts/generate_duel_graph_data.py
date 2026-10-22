#!/usr/bin/env python3
"""Generate live 3D graph data for Jun's Holographic Duel Matrix.

Extracts all Markdown files from 03_Dev_Projects/wiki, strips frontmatter/metadata,
extracts real human summaries, maps each article to one of the 5 official Kuriboh domains,
and computes 100+ cross-discipline neural bridges.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

WIKI_ROOT = Path("D:/Workspace/03_Dev_Projects/wiki")
OUTPUT_JSON = WIKI_ROOT / "matrix/graph_data.json"
OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

DOMAIN_CFG = {
    "agent":   {"color": "#00f0ff", "hex": 0x00f0ff, "name": "Agent Systems (青藍·代理控制面)"},
    "quant":   {"color": "#39ff14", "hex": 0x39ff14, "name": "Quant & Alpha (螢綠·量化風控)"},
    "semi":    {"color": "#ffd700", "hex": 0xffd700, "name": "Semiconductor (純金·晶圓工藝)"},
    "podcast": {"color": "#bf55ec", "hex": 0xbf55ec, "name": "AIGC Pipeline (賽博紫·代碼縫隙)"},
    "spec":    {"color": "#ff3838", "hex": 0xff3838, "name": "Specs & QA (緋紅·契約硬閘門)"},
    "infra":   {"color": "#ff7700", "hex": 0xff7700, "name": "Infra & Cloud (熔岩橙·私有雲)"},
    "core":    {"color": "#ffffff", "hex": 0xffffff, "name": "Core Philosophy (白金·誠信中樞)"}
}

TAG_MAP = {
    "agent": ["AI-Agent", "CDP-Control", "State-Machine", "Dual-Core"],
    "quant": ["JoJo-Trader", "Risk-Control", "Stop-Loss", "Zero-Lot"],
    "semi":  ["Wafer-SAW", "ASE-Packaging", "7-Steps-Blade", "Poka-Yoke"],
    "podcast": ["Code-Gaps", "Gemini-TTS", "Voice-Clone", "Automation"],
    "infra": ["NAS-Cluster", "Tailscale", "Docker-Compose", "Auto-Heal"],
    "spec":  ["Specs-Audit", "Playwright-QA", "Contract", "Zero-Defect"]
}

HIGHLIGHT_MAP = {
    "semi": "微米級精準度 · 實體零容錯防呆",
    "quant": "本金 2 萬生命線 · 16,000 元強制斷路",
    "agent": "Maker 施工 + Grader 38 項硬閘門獨立驗收",
    "podcast": "-16 LUFS 廣播標竿 · 雙角色硬核對抗",
    "infra": "30分鐘自愈守護 · 內網零信任隔離",
    "spec": "DATA SOURCE INTEGRITY · 拒絕口頭假陽性"
}


def clean_human_summary(filepath: Path, fallback_title: str, domain: str) -> str:
    try:
        raw = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return f"收錄於 Jun's Wiki 的 {fallback_title} 核心架構紀錄。"

    # 1. 抓取 frontmatter 中的 summary
    fm_match = re.search(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
    if fm_match:
        fm_text = fm_match.group(1)
        sum_m = re.search(r"summary:\s*[\"']?([^\"'\r\n]+)[\"']?", fm_text)
        if sum_m and len(sum_m.group(1).strip()) > 8:
            clean = sum_m.group(1).strip()
            clean = re.sub(r"[#`*_{}\[\]]", "", clean)
            return clean
        body = raw[fm_match.end():]
    else:
        body = raw

    # 2. 清理正文 Markdown
    body = re.sub(r"```.*?```", "", body, flags=re.DOTALL)
    body = re.sub(r"`.*?`", "", body)
    body = re.sub(r"^#+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"^>+.*$", "", body, flags=re.MULTILINE)
    body = re.sub(r"\[\[(.*?)\]\]", r"\1", body)
    body = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", body)
    body = re.sub(r"[*_~|]", " ", body)
    body = re.sub(r"(created|updated|type|tags|confidence|status|來源|狀態|模板格式|實體\s*PDF):\s*\S+", "", body)
    body = re.sub(r"\s+", " ", body).strip()

    sentences = [s.strip() for s in re.split(r"[。！？\n]", body) if len(s.strip()) > 10]
    if sentences:
        return sentences[0] + "。"
    if len(body) > 15:
        return body[:110] + "..."
    return f"收錄於 Jun's Wiki 的 {fallback_title} 技術架構紀錄。"


def build_graph():
    nodes = []
    links = []
    node_ids = set()

    # 1. 核心大腦中樞 (Convergence Hubs)
    hubs = [
        {
            "id": "HUB_DATA_INTEGRITY",
            "name": "⚡ DATA SOURCE INTEGRITY (最高原則中樞)",
            "domain": "core",
            "val": 30,
            "isHub": True,
            "cleanSummary": "全域第一原則：多源交叉比對、拒絕偽安全感、冷讀獨立驗收。貫穿量化交易風控、半導體精密點檢、AI Agent 雙核閉環。",
            "tags": ["Absolute-Truth", "No-Sycophancy", "Hard-Gate"],
            "highlight": "DATA SOURCE INTEGRITY · 拒絕口頭假陽性"
        },
        {
            "id": "HUB_AUTOMATION_CDP",
            "name": "🛡️ CDP & 狀態機控制面 (自動化大腦)",
            "domain": "core",
            "val": 25,
            "isHub": True,
            "cleanSummary": "零依賴 Chrome/Brave 瀏覽器底層控制 SDK (agent-cdp-guardian)、狀態機防呆與 NAS 容器叢集，將半導體改機 21 動標準移植至軟體自動化。",
            "tags": ["CDP-Guardian", "Zero-Dependency", "Sandboxing"],
            "highlight": "工業級狀態機 · 瀏覽器底層控制面"
        },
        {
            "id": "HUB_SHARED_BRAIN",
            "name": "🎙️ 代碼縫隙 × 知識沉澱 (外溢與傳播)",
            "domain": "core",
            "val": 22,
            "isHub": True,
            "cleanSummary": "《代碼縫隙》自治多媒體產線：Google Gemini 雙角色演繹底帶 + 本地 OpenVoice 聲紋換皮，將工程踩坑轉化為每週自動上架播客與 Wiki 正本。",
            "tags": ["Code-Gaps", "Gemini-TTS", "Two-Stage"],
            "highlight": "-16 LUFS 廣播標竿 · 雙角色硬核對抗"
        }
    ]
    for h in hubs:
        cfg = DOMAIN_CFG[h["domain"]]
        h["color"] = cfg["color"]
        h["colorHex"] = cfg["hex"]
        h["domainName"] = cfg["name"]
        nodes.append(h)
        node_ids.add(h["id"])

    # 2. 遍歷 Markdown 文件
    md_files = list(WIKI_ROOT.glob("**/*.md"))
    for p in md_files:
        rel = p.relative_to(WIKI_ROOT).as_posix()
        if "node_modules" in rel or ".git" in rel or "matrix" in rel:
            continue
        base = p.stem
        raw_text = p.read_text(encoding="utf-8", errors="ignore")

        # 判定領域
        nid = rel.lower()
        if any(k in nid for k in ("jojo", "quant", "trade", "stock", "alpha", "order", "smc", "pnl")):
            dom = "quant"
        elif any(k in nid for k in ("saw", "semi", "wafer", "ase", "dicing", "blade", "singulation")):
            dom = "semi"
        elif any(k in nid for k in ("podcast", "voice", "audio", "soulx", "gemini", "shorts", "縫隙")):
            dom = "podcast"
        elif any(k in nid for k in ("nas", "docker", "infra", "tailscale", "cron", "synology", "wsl")):
            dom = "infra"
        elif any(k in nid for k in ("contract", "spec", "qa", "gate", "audit", "rubric", "integrity")):
            dom = "spec"
        else:
            dom = "agent"

        # 標題
        title = base
        m_title = re.search(r"^#\s+([^\r\n]+)", raw_text, re.MULTILINE)
        if m_title:
            title = m_title.group(1).strip()

        cfg = DOMAIN_CFG[dom]
        node = {
            "id": rel,
            "name": title,
            "domain": dom,
            "color": cfg["color"],
            "colorHex": cfg["hex"],
            "domainName": cfg["name"],
            "val": min(max(len(raw_text) // 350, 4), 16),
            "cleanSummary": clean_human_summary(p, title, cfg["name"]),
            "tags": TAG_MAP.get(dom, ["Engineering", "Verified"]),
            "highlight": HIGHLIGHT_MAP.get(dom, "核心工程架構"),
            "isHub": False
        }
        nodes.append(node)
        node_ids.add(rel)

    node_map = {n["id"]: n for n in nodes}

    # 3. 建立連線 (Links)
    for p in md_files:
        rel = p.relative_to(WIKI_ROOT).as_posix()
        if rel not in node_map:
            continue
        raw_text = p.read_text(encoding="utf-8", errors="ignore")
        for target in re.findall(r"[\(\"\'\=]([a-zA-Z0-9_\-\.\/]+\.md)[\)\"\'\s]", raw_text):
            clean_tgt = os.path.normpath(os.path.join(os.path.dirname(rel), target)).replace("\\", "/")
            if clean_tgt in node_map and clean_tgt != rel:
                is_cross = node_map[rel]["domain"] != node_map[clean_tgt]["domain"]
                links.append({"source": rel, "target": clean_tgt, "cross": is_cross})

    # 4. 跨領域主動脈連接 (Cross-Bridges)
    cross_links = []
    for n in nodes:
        if n["isHub"]:
            continue
        dom = n["domain"]
        if dom in ("quant", "semi", "spec"):
            cross_links.append({"source": "HUB_DATA_INTEGRITY", "target": n["id"], "cross": True})
        if dom in ("agent", "infra", "semi"):
            cross_links.append({"source": "HUB_AUTOMATION_CDP", "target": n["id"], "cross": True})
        if dom in ("podcast", "agent"):
            cross_links.append({"source": "HUB_SHARED_BRAIN", "target": n["id"], "cross": True})

    cross_links.append({"source": "HUB_DATA_INTEGRITY", "target": "HUB_AUTOMATION_CDP", "cross": True})
    cross_links.append({"source": "HUB_AUTOMATION_CDP", "target": "HUB_SHARED_BRAIN", "cross": True})
    cross_links.append({"source": "HUB_SHARED_BRAIN", "target": "HUB_DATA_INTEGRITY", "cross": True})

    links.extend(cross_links)

    # 去重
    seen_links = set()
    dedup_links = []
    for l in links:
        s, t = l["source"], l["target"]
        key = tuple(sorted([s, t]))
        if key not in seen_links and s != t:
            seen_links.add(key)
            dedup_links.append(l)

    output_data = {"nodes": nodes, "links": dedup_links}
    OUTPUT_JSON.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated live duel graph: {len(nodes)} nodes, {len(dedup_links)} links -> {OUTPUT_JSON}")


if __name__ == "__main__":
    build_graph()
