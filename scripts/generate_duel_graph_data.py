#!/usr/bin/env python3
"""
Generate live 3D graph data for Jun's Holographic Duel Matrix.
Extracts all Markdown files from 03_Dev_Projects/wiki, strips frontmatter/metadata,
extracts real human summaries, maps each article to one of the 8 refined domains,
and computes 100+ cross-discipline neural bridges.
"""
from __future__ import annotations
import os
import re
import json
from pathlib import Path

WIKI_ROOT = Path("D:/Workspace/03_Dev_Projects/wiki")
OUTPUT_JSON = WIKI_ROOT / "matrix/graph_data.json"
OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)

DOMAIN_CFG = {
    "semi":   {"color": "#ffd700", "hex": 0xffd700, "name": "Semiconductor (晶圓工藝與封測)"},
    "agent":  {"color": "#00f0ff", "hex": 0x00f0ff, "name": "Agent Systems (代理人與控制面)"},
    "quant":  {"color": "#39ff14", "hex": 0x39ff14, "name": "Quant & Alpha (量化風控與交易)"},
    "game":   {"color": "#ff6600", "hex": 0xff6600, "name": "Game Dev (獨立遊戲與UE5)"},
    "aigc":   {"color": "#bf55ec", "hex": 0xbf55ec, "name": "AIGC & Media (代碼縫隙與影音)"},
    "spec":   {"color": "#ff3838", "hex": 0xff3838, "name": "Specs & QA (契約門禁與測試)"},
    "infra":  {"color": "#4da6ff", "hex": 0x4da6ff, "name": "Cloud Infra (私有雲與DevOps)"},
    "career": {"color": "#e0e6ed", "hex": 0xe0e6ed, "name": "Career & Meta (職涯沉澱與時間線)"},
    "core":   {"color": "#ffffff", "hex": 0xffffff, "name": "Core Philosophy (全域誠信中樞)"}
}

TAG_MAP = {
    "semi":   ["Wafer-SAW", "ASE-Packaging", "Blade-Inspect", "Zero-Tolerance"],
    "agent":  ["AI-Agent", "CDP-Guardian", "State-Machine", "Dual-Core"],
    "quant":  ["JoJo-Trader", "Risk-Control", "Stop-Loss", "Zero-Lot"],
    "game":   ["Spirits-Calling", "UE5-Stealth", "Blender-Mesh", "Roguelite"],
    "aigc":   ["Code-Gaps", "Gemini-TTS", "Voice-Clone", "-16LUFS"],
    "spec":   ["DATA-INTEGRITY", "Playwright-Harness", "Hard-Gate", "Audit"],
    "infra":  ["NAS-Cluster", "Tailscale", "Docker-Compose", "Auto-Heal"],
    "career": ["Jun-Profile", "Open-Source", "Timeline", "Architecture"]
}

HIGHLIGHT_MAP = {
    "semi":   "微米級精準度 · 實體零容錯防呆",
    "agent":  "Maker 施工 + Grader 38 項硬閘門驗收",
    "quant":  "本金 2 萬生命線 · 16,000 元強制熔斷",
    "game":   "UE5.8 賽博靈異潛行 · 實感物理手感",
    "aigc":   "-16 LUFS 廣播標竿 · 雙角色硬核對抗",
    "spec":   "DATA SOURCE INTEGRITY · 拒絕口頭假陽性",
    "infra":  "30分鐘自愈守護 · 內網零信任隔離",
    "career": "日月光工程師 · 個人研究與開源主線"
}

def clean_human_summary(filepath: Path, fallback_title: str, domain_name: str) -> str:
    try:
        raw = filepath.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return f"收錄於 Jun's Wiki 的 {fallback_title} 核心架構紀錄。"

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

def refine_domain(rel_path: str, title: str, text: str) -> str:
    r = rel_path.lower()
    t = (title + " " + rel_path).lower()

    if any(k in r for k in ["spirits_calling", "live2d_pipeline", "avatar", "vskin"]) or any(k in t for k in ["spirits-calling", "ue5", "unreal", "blender", "遊戲"]):
        return "game"
    if any(k in r for k in ["saw", "semi", "dicing"]) or any(k in t for k in ["semiconductor", "晶圓", "封裝", "封測", "換刀", "disco", "ase", "切割"]):
        return "semi"
    if any(k in r for k in ["jojo", "trading", "quant"]) or any(k in t for k in ["jojo", "量化", "選股", "風控", "smc", "台股", "期貨", "生命線", "回測", "止損", "布林"]):
        return "quant"
    if any(k in r for k in ["podcast", "media", "social_content"]) or any(k in t for k in ["podcast", "播客", "代碼縫隙", "gemini-tts", "soulx", "短影音", "comfyui", "stable-diffusion", "音訊", "母帶"]):
        return "aigc"
    if any(k in r for k in ["governance"]) or any(k in t for k in ["contract", "integrity", "門禁", "驗收", "審計", "qa", "harness", "rubric", "除錯", "bug", "踩坑"]):
        return "spec"
    if any(k in r for k in ["dev_ops", "nas_vitepress"]) or any(k in t for k in ["nas", "synology", "docker", "tailscale", "cron", "postgresql", "meilisearch", "自愈", "wsl", "伺服器", "環境圖", "工作區架構"]):
        return "infra"
    if any(k in r for k in ["job_search", "job_patrol"]) or any(k in t for k in ["resume", "hot.md", "log.md", "schema.md", "履歷", "求職", "定位", "時間線", "書籍筆記"]):
        return "career"
    return "agent"

def build_graph():
    nodes = []
    links = []
    node_ids = set()

    hubs = [
        {
            "id": "HUB_DATA_INTEGRITY",
            "name": "⚡ DATA SOURCE INTEGRITY (最高原則中樞)",
            "domain": "core",
            "val": 30,
            "isHub": True,
            "cleanSummary": "全域第一原則：多源交叉比對、拒絕口頭假陽性、冷讀獨立驗收。貫穿量化交易風控、半導體精密點檢、AI Agent 雙核閉環。",
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

    md_files = list(WIKI_ROOT.glob("**/*.md"))
    for p in md_files:
        rel = p.relative_to(WIKI_ROOT).as_posix()
        if "node_modules" in rel or ".git" in rel or "matrix" in rel:
            continue
        base = p.stem
        raw_text = p.read_text(encoding="utf-8", errors="ignore")

        title = base
        m_title = re.search(r"^#\s+([^\r\n]+)", raw_text, re.MULTILINE)
        if m_title:
            title = m_title.group(1).strip()

        dom = refine_domain(rel, title, raw_text)
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

    cross_links = []
    for n in nodes:
        if n["isHub"]:
            continue
        dom = n["domain"]
        if dom in ("quant", "semi", "spec"):
            cross_links.append({"source": "HUB_DATA_INTEGRITY", "target": n["id"], "cross": True})
        if dom in ("agent", "infra", "semi", "game"):
            cross_links.append({"source": "HUB_AUTOMATION_CDP", "target": n["id"], "cross": True})
        if dom in ("aigc", "agent", "career"):
            cross_links.append({"source": "HUB_SHARED_BRAIN", "target": n["id"], "cross": True})

    cross_links.append({"source": "HUB_DATA_INTEGRITY", "target": "HUB_AUTOMATION_CDP", "cross": True})
    cross_links.append({"source": "HUB_AUTOMATION_CDP", "target": "HUB_SHARED_BRAIN", "cross": True})
    cross_links.append({"source": "HUB_SHARED_BRAIN", "target": "HUB_DATA_INTEGRITY", "cross": True})

    links.extend(cross_links)

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
    print(f"Generated refined 8-domain duel graph: {len(nodes)} nodes, {len(dedup_links)} links -> {OUTPUT_JSON}")

if __name__ == "__main__":
    build_graph()
