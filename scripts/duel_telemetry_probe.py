#!/usr/bin/env python3
"""Live Telemetry Probe for Jun's Holographic Duel Matrix.

Probes the 5 core real-world infrastructure services and exports
deterministic state machine status for the 3D Duel Field monster zones.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path

OUT_JSON = Path("D:/Workspace/03_Dev_Projects/wiki/matrix/telemetry_state.json")
OUT_JSON.parent.mkdir(parents=True, exist_ok=True)

SERVICES = [
    {
        "zone": 0,
        "id": "HINDSIGHT-CORE",
        "name": "記憶中樞 · Hindsight 9077",
        "kuriboh": "白金·資料誠信栗子球",
        "color": "#ffffff",
        "url": "http://127.0.0.1:9077/health",
        "desc": "雙層架構長程語意關聯與記憶沈澱中樞",
        "heal_cmd": "python C:/Users/Jun/.hermes/scripts/hindsight_liveness_warden.py",
        "port": 9077
    },
    {
        "zone": 1,
        "id": "NAS-WIKI-STACK",
        "name": "私有雲 · NAS Wiki 叢集",
        "kuriboh": "熔岩橙·私有雲栗子球",
        "color": "#ff7700",
        "url": "http://192.168.1.107:8000/api/stats/",
        "desc": "Synology DSM 容器化 PostgreSQL 5434 + Meilisearch",
        "heal_cmd": "python C:/Users/Jun/.hermes/scripts/wiki_sync_cron_wrapper.py",
        "port": 8000
    },
    {
        "zone": 2,
        "id": "CPA-GATEWAY",
        "name": "渠道調度 · CLIProxyAPI 18004",
        "kuriboh": "翡翠綠·量化風控栗子球",
        "color": "#39ff14",
        "url": "http://127.0.0.1:18004/v1/models",
        "desc": "多帳號 AI 模型存取本機代理與自動熔斷網關",
        "heal_cmd": "cli-proxy-api",
        "port": 18004
    },
    {
        "zone": 3,
        "id": "BRAVE-CDP-GUARDIAN",
        "name": "控制面 · Brave CDP 9222",
        "kuriboh": "青藍·代理控制面栗子球",
        "color": "#00f0ff",
        "url": "http://127.0.0.1:9222/json/version",
        "desc": "零依賴底層 CDP 安全 SDK，防注入與登入態調度面",
        "heal_cmd": "brave --remote-debugging-port=9222",
        "port": 9222
    },
    {
        "zone": 4,
        "id": "ASE-VAULT-18090",
        "name": "晶圓工藝 · 日月光私人路徑 18090",
        "kuriboh": "純金·晶圓工藝栗子球",
        "color": "#ffd700",
        "url": "http://127.0.0.1:18090/",
        "desc": "半導體切割封裝遊戲化學習儀表板與安全驗證閘門",
        "heal_cmd": "python C:/Users/Jun/.hermes/scripts/ase_learning_warden.py",
        "port": 18090
    }
]


def probe_all():
    records = []
    up_count = 0

    for s in SERVICES:
        t0 = time.time()
        status = "DOWN"
        code = 0
        try:
            req = urllib.request.Request(s["url"], headers={"User-Agent": "DuelTelemetry/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                code = resp.getcode()
                if code in (200, 302, 501):
                    status = "UP"
        except urllib.error.HTTPError as he:
            code = he.code
            if code in (401, 403, 302, 501):
                status = "UP"
        except Exception:
            status = "DOWN"

        latency = int((time.time() - t0) * 1000)
        if status == "UP":
            up_count += 1
            mode = "ATTACK"  # 攻擊表示
            atk = 2400
            defense = max(999 - latency * 2, 100)
        else:
            mode = "GRAVEYARD"  # 破壞送進墓地
            atk = 0
            defense = 0

        records.append({
            "zone": s["zone"],
            "id": s["id"],
            "name": s["name"],
            "kuriboh": s["kuriboh"],
            "color": s["color"],
            "status": status,
            "mode": mode,
            "code": code,
            "port": s["port"],
            "desc": s["desc"],
            "latency_ms": latency if status == "UP" else None,
            "atk": atk,
            "def": defense,
            "heal_cmd": s["heal_cmd"]
        })

    payload = {
        "timestamp": int(time.time()),
        "time_iso": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": len(SERVICES),
        "up": up_count,
        "down": len(SERVICES) - up_count,
        "zones": records
    }

    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[{payload['time_iso']}] Telemetry: {up_count}/{len(SERVICES)} UP -> {OUT_JSON}")
    return payload


if __name__ == "__main__":
    probe_all()
