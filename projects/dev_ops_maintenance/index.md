---
title: "GitHub 專案維運與 CI/CD 環境健康審查報告"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [devops, github, cicd, git, workspace_hygiene, quality_gate]
summary: "全面盤點 D:/Workspace 下 20 個主力開源專案之 Git 狀態、CI/CD 配置覆蓋率，定位遺漏自動化腳本並建立目錄衛生與維運標準。"
status: active
source:
  - "03_Dev_Projects/recall/.github/workflows/ci.yml"
  - "03_Dev_Projects/recall-memory-hermes/.github/workflows/ci.yml"
  - "03_Dev_Projects/wiki/wiki_sync.py"
confidence: high
review_after: 2026-10-03
---

# GitHub 項目維運與環境健康審查報告 (t_9c935db0)

## 1. 專案 Git 狀態與 CI/CD 覆蓋率實況盤點 (客觀事實數據)

針對 `/mnt/d/Workspace/03_Dev_Projects` 20 個主力儲存庫進行狀態掃描與 CI 檢驗：

| 儲存庫名稱 | Git 工作目錄狀態 | GitHub Actions CI/CD 配置 | 備註 / 風險點 |
|---|---|---|---|
| `recall-memory-hermes` | **CLEAN** | ✅ `ci.yml` / `publish.yml` | 標準典範儲存庫 |
| `recall` | DIRTY (37 files) | ✅ `ci.yml` / `publish.yml` | 具備完整 CI，待清理本地 dirty 狀態 |
| `Jnocode.github.io` | DIRTY (1 file) | ❌ 無配置 | 個人/作品集站點 |
| `SAMMI-TC-Patch` | DIRTY (2 files) | ❌ 無配置 | 本地化補丁 |
| `Windows-Copilot-API` | DIRTY (37 files) | ❌ 無配置 | API 封裝，有未追蹤檔案 |
| `claude-code-openai-server`| DIRTY (42 files) | ❌ 無配置 | 代理轉發服務 |
| `gout_diet_cam` | DIRTY (16 files) | ❌ 無配置 | 視覺辨識專案 |
| `llama-launcher` | DIRTY (7 files) | ❌ 無配置 | 本地推理啟動器 |
| `maiagent-exam` | DIRTY (2 files) | ❌ 無配置 | 測試專案 |
| `portfolio` | DIRTY (2 files) | ❌ 無配置 | 作品展示庫 |
| `recall-vault` | DIRTY (2 files) | ❌ 無配置 | 筆記儲存庫 |
| `shadowverse_tracker` | DIRTY (156 files)| ❌ 無配置 | 數據追蹤，大量未提交臨時數據 |
| `taiwan-career-ops` | DIRTY (22 files) | ❌ 無配置 | 求職/職涯運營 |
| `well_cut` | DIRTY (11 files) | ❌ 無配置 | 影音剪輯工具 |
| `wiki` | DIRTY (70+ files) | ❌ 無配置 | 核心 Wiki 服務，含 `wiki_sync.py` 未追蹤 |
| `Spirits-Calling` | 鎖定中 / 巨型庫 | ❌ 依賴本機 UAT | C++ / UE5.8 遊戲專案 |
| `hermes-agent-fork` | 巨型庫 | ❌ 待查核 | 上游 Fork |
| `hermes-desktop-fork`| 巨型庫 | ❌ 待查核 | 上游 Fork |
| `jojo_trading` | 巨型庫 | ❌ 待查核 | 量化交易 |
| `suno-api` | 巨型庫 | ❌ 待查核 | 音樂 API 逆向 |

---

## 2. 核心發現與環境健康隱患

1. **CI/CD 配置覆蓋率偏低**：
   - 20 個專案中僅 `recall` 與 `recall-memory-hermes` 具備自動化 CI（測試/打包/發布）。
   - 其餘 18 個專案缺乏 Pull Request 驗證、Lint 檢查與自動測試閘門，依賴本機手工執行。
2. **目錄衛生與未追蹤腳本堆積**：
   - `03_Dev_Projects/wiki` 中存在關鍵自動化同步腳本 `wiki_sync.py` 與備份 `wiki_sync.py.bak.20260829`、`wiki.db` 處於未追蹤狀態（Untracked），存在檔案遺失與被誤覆蓋風險。
   - `shadowverse_tracker` 存在高達 156 個未追蹤/修改項目，缺乏合規 `.gitignore` 排除暫存檔。

---

## 3. 維運改善標準與處置建議

1. **標準 CI/CD 模板推廣**：
   - 參照 `recall-memory-hermes/.github/workflows/ci.yml`，為 Python 專案引入標準化 `pytest` + `ruff` + `mypy` GitHub Actions 範本。
2. **自動化腳本收斂與歸檔**：
   - 將 `03_Dev_Projects/wiki/wiki_sync.py` 納入 Git 版本控制，將備份檔案移入專屬歸檔目錄，設定 `.gitignore` 排除本機 SQLite 資料庫（`*.db`）。
3. **工作區防污染巡檢**：
   - 定期運行目錄衛生檢查，維持 `D:/Workspace` 根目錄 0 臨時檔案。
