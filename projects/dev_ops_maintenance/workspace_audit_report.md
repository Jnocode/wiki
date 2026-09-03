---
title: "GitHub 開源專案 CI/CD 範本化與工作區自動化審計報告"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [devops, github_actions, cicd, auditor, workspace_hygiene, quality_gate]
summary: "完成全自動 Workspace 衛生與 Git 狀態審計工具 audit_workspace_hygiene.py；輸出最新衛生報告（根目錄 0 雜檔，20 個 Repos CI 覆蓋率 25%）；提供標準化 Python CI/CD 範本。"
status: active
source:
  - "agent_office/tools/workspace-auditor/audit_workspace_hygiene.py"
  - "agent_office/tools/workspace-auditor/latest_hygiene_report.json"
  - "agent_office/tools/cicd-templates/standard-python-ci.yml"
confidence: high
review_after: 2026-10-04
---

# GitHub 專案 CI/CD 與工作區自動化審計 (t_9c935db0)

## 1. 自動化工作區衛生審計器 (Workspace Auditor)

針對維護 Workspace 目錄衛生與開源專案品質之核心目標，開發全自動檢驗工具：
- **腳本路徑**：`/mnt/d/Workspace/agent_office/tools/workspace-auditor/audit_workspace_hygiene.py`
- **產出報告**：`/mnt/d/Workspace/agent_office/tools/workspace-auditor/latest_hygiene_report.json`
- **最新即時審計指標 (2026-09-04T00:57:42)**：
  1. **根目錄衛生指標 (Root Hygiene)**：
     - 根目錄實體檔案數：7 個（全數為 `.cursorrules`、`.gitignore` 等必要設定檔）。
     - 可疑臨時檔（`.tmp`, `.temp`, `.log`, `.bak`）：**0 個**。
     - 判定結論：`is_clean: true`（100% 達成目錄衛生紅線）。
  2. **Git 與 CI/CD 總體分佈**：
     - 總專案數：`20` 個。
     - CI/CD 覆蓋庫：`5` 個（`25.0%`，包含 `recall`, `recall-memory-hermes`, `jojo_trading`, `hermes-agent-fork`, `hermes-desktop-fork`）。
     - 待配置 CI/CD 庫：`15` 個（`75.0%`）。

---

## 2. 標準化 GitHub Actions CI/CD 範本庫

為加速其餘 15 個開源專案落地自動化驗收與 PR 檢查，建立可複用之標準化模板：
- **範本檔案**：`/mnt/d/Workspace/agent_office/tools/cicd-templates/standard-python-ci.yml`
- **核心驗收閘門**：
  - **Python 多版本矩陣**：支援 Python 3.11 與 3.12 跨版本測試。
  - **靜態語法與格式檢查**：整合 `ruff check .`（毫秒級高速 Linter）。
  - **靜態型別安全檢驗**：整合 `mypy src`。
  - **自動化單元測試**：整合 `pytest -v`，杜絕壞代碼合入 main 分支。

---

## 3. 目錄衛生與維運改進建議

1. **Dirty 專案重點清理清單**：
   - `Spirits-Calling` (157 files) 與 `shadowverse_worlds_beyond_tracker` (156 files)：建議優先補齊 `.gitignore`，將暫存與快取數據徹底阻隔在版本控制之外。
2. **定時巡檢整合**：
   - 建議將 `audit_workspace_hygiene.py` 加入定期心跳或排程巡檢中，即時警示任何違規建立於根目錄之雜檔。
