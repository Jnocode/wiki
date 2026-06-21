---
title: Agent Office Shared
created: 2026-06-20
updated: 2026-06-20
type: entity
tags: [hermes, openclaw, agent, infrastructure]
confidence: high
---

# Agent Office Shared

Hermes 與 OpenClaw 雙 Agent 協作的工作目錄。路徑：`D:\Workspace\agent_office\shared\`

## 內容

### COLLABORATION_PROTOCOL.md
雙 Agent 協作協議 v1.0，定義：
- **Hermes**：前線秘書、Windows 操作、服務監控、輕量排程
- **OpenClaw**：後端重型運算、量化回測、併發多 Agent

### brain/ — Obsidian 知識庫
完整的 Obsidian vault，包含 Obsidian Git、Dataview、Excalidraw 等插件。

#### 目錄結構
- `00_about/` — 使用指南、組織資訊
- `01_tech/` — 技術筆記（OpenClaw Setup、Model Training）
- `02_projects/` — 專案檔案導覽與規劃
- `03_meetings/` — 會議記錄、TODO、週分享
- `04_media/` — 社群貼文、腳本
- `05_business/AIxQuantMedia/` — 公司營運、日報、技能文件
- `06_tasks/` — 任務管理
- `07_notes/` — 日記、歌詞
- `90_system/` — 系統設定
- `integrated_memory/` — 整合記憶

### Python 腳本
- `honcho_import.py` / `migrate_memory_to_honcho.py` — Honcho 記憶遷移工具
- `set_peer_card.py` — Honcho peer card 設定

## 相關頁面
- [[hermes-agent]] — 前線 Agent
- [[OpenClaw]] — 後端 Agent
- [[Honcho]] — 記憶系統
