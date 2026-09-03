---
title: "GitHub 專案維運：20 個 Git 專案 .gitignore 補齊與快取雜檔治理"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [git_hygiene, gitignore, dev_ops, dev_projects, cache_exclusion]
summary: "排查 03_Dev_Projects 內 20 個 Git 專案；全面補齊標準 Python 與 UE5 .gitignore 排除規則（覆蓋率達 100%），產出結構化執行報告至 artifacts/git_cleanup_report.json。"
status: active
source:
  - "artifacts/git_cleanup_report.json"
confidence: high
review_after: 2026-10-04
---

# GitHub 專案維運：Git 專案 .gitignore 補齊與快取雜檔治理報告 (t_2ac30cc5)

## 1. 治理背景與標準規範

依據 `AGENT_COLLABORATION_SPEC.md` 工作區衛生與目錄隔離原則，開發專案必須維持乾淨的 Git 追蹤狀態，杜絕編譯快取、暫存檔與虛擬環境被誤推送至公開倉庫。

### 標準排除黑名單 (Hygiene Patterns)
1. **Python 核心**：`__pycache__/`, `*.py[cod]`, `*.so`, `.venv/`, `env/`, `dist/`, `build/`
2. **暫存與日誌**：`*.log`, `*.tmp`, `*.bak`, `*.db`, `*.sqlite3`
3. **系統雜檔**：`.DS_Store`, `Thumbs.db`, `.idea/`, `.vscode/`
4. **UE5 遊戲專案特化 (Spirits-Calling)**：`Binaries/*`, `DerivedDataCache/*`, `Intermediate/*`, `Saved/*`, `Build/*`, `*.VC.db`, `*.sln`

---

## 2. 實機執行與數據指標 (客觀事實依據)

- **結構化審計產物**：`/mnt/d/Workspace/artifacts/git_cleanup_report.json`
- **掃描專案總數**：20 個 Git 專案
- **.gitignore 存在覆蓋率**：**20 / 20 (100.0%)**
- **規則補充更新數**：**17 個** 專案完成防護模式注入（包含 `Spirits-Calling`、`wiki`、`shadowverse_worlds_beyond_tracker` 等核心專案）。
- **零程式碼破壞 (Non-destructive)**：僅針對 `.gitignore` 新增未涵蓋之 pattern，絕無強行 reset 或破壞任何開發者未提交的工作樹變更。

---

## 3. 交付產物路徑

1. 結構化報告：`/mnt/d/Workspace/artifacts/git_cleanup_report.json`
2. 知識庫沉澱：`/mnt/d/Workspace/agent_office/shared/brain/projects/dev_ops_maintenance/git_dirty_repos_hygiene_report.md`
