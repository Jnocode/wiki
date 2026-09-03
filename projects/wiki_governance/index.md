---
title: "Wiki 知識庫 NAS 與本地雙向同步與索引治理專案報告"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [wiki, nas, vitepress, linter, sync, governance, schema]
summary: "完成 agent_office/shared/brain 知識庫 60 篇 Markdown 格式全面修復，達成 100% SCHEMA.md 合規率；驗證 wiki_sync.py 雙向同步通道與 VitePress 索引建置標準。"
status: active
source:
  - "agent_office/shared/brain/SCHEMA.md"
  - "agent_office/tools/brain-linter/brain_vault_linter.py"
  - "03_Dev_Projects/wiki/wiki_sync.py"
confidence: high
review_after: 2026-10-04
---

# Wiki 知識庫 NAS 與本地雙向同步與索引治理 (t_5b5f912b)

## 1. 知識庫 Schema 憲法落實與 Linter 工具建置

針對看板任務核心目標「確保所有技術沉澱均具備 YAML frontmatter，杜絕無結構雜檔」：
- **專屬 Linter/Fixer 工具**：`/mnt/d/Workspace/agent_office/tools/brain-linter/brain_vault_linter.py`
- **合規性標準**：嚴格依循 `/mnt/d/Workspace/agent_office/shared/brain/SCHEMA.md` 定義之 6 大白名單類型（`entity`, `concept`, `project`, `source`, `query`, `log`）與必要欄位。
- **全庫掃描與自動修復成果**：
  - 修復前：總計 60 篇 Markdown，合規 29 篇（合規率僅 **48.3%**，主要為 `raw/2026/` 存檔缺少 `type: source`）。
  - 修復執行：`python3 brain_vault_linter.py --fix`（Exit Code `0`，修復 31 篇）。
  - 修復後驗證：總計 60 篇 Markdown，合規 60 篇，**合規率達到 100.0%**。

---

## 2. NAS 與本地 Markdown 雙向同步機制 (wiki_sync.py)

實體同步核心腳本：`/mnt/d/Workspace/03_Dev_Projects/wiki/wiki_sync.py`
- **通訊架構**：
  - NAS 目標主機：`192.168.1.107:7414` (SSH Key: `C:\Users\Jun\.ssh\id_ed25519_openclaw`)
  - 運作模式：記憶體內 Tarball 打包（`concepts`, `entities`, `projects`, `raw/2026`）$\rightarrow$ SFTP 傳輸至 NAS 容器 $\rightarrow$ 解壓縮並自動觸發 VitePress 重新構建。
  - 格式淨化：自動修復 Wikilinks 語法（`[[[` $\rightarrow$ `[[`）並校驗 frontmatter title，確保 VitePress 渲染無白畫面或破版。

---

## 3. 索引建置與目錄衛生規範

1. **零根目錄雜檔防護**：
   - 杜絕於 `D:/Workspace` 根目錄產生任何臨時檔。
   - 所有 Linter 與工具收攏於 `agent_office/tools/brain-linter/`，快取資料夾受 `.gitignore` 排除。
2. **持續合規閘門**：
   - 任何 Agent（Hermes 或小克）撰寫知識沉澱前，均需遵循標準 Frontmatter 格式，並定期執行 `brain_vault_linter.py` 作為 CI 驗收閘門。
