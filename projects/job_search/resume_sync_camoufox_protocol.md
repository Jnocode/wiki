---
title: "104 與 CakeResume 線上履歷同步協議與 Quill 編輯器 Read-back 驗收"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [resume_sync, 104_quill, cakeresume, browser_automation, readback_acceptance]
summary: "完成 104 與 CakeResume 履歷同步規格化作業；解析 104 Quill 編輯器鍵盤注入防破壞機制，建立結構化資料 Payload (resume_sync_payload.json) 與 8 大核心字根外部 Read-back 驗收清單。"
status: active
source:
  - "02_Job_Search/resume_fixed_20260701.md"
  - "agent_office/data/resume_sync_payload.json"
  - "agent_office/data/resume_sync_execution_status.json"
  - "agent_office/tools/resume-sync/execute_resume_sync.py"
confidence: high
review_after: 2026-10-04
---

# 104 與 CakeResume 線上履歷同步與 Quill 自動化協議 (t_b144c685)

## 1. 履歷內容核心模組 (依據 resume_fixed_20260701.md)

- **目標職稱**：`姜鈞 (Jun Jiang) | AI Engineer — LLM · RAG · AI Agent Systems`
- **關於我 (About Me)**：
  - 核心重點：`Recall / Hermes memory system`（SQLite + FTS5 + RRF 多路徑檢索，發布 PyPI `recall-sqlite`，整合 Hermes Agent 上游 PR）。
  - 經歷底蘊：12 年跨領域工程管理經驗，擅長將模糊業務需求拆解為確定性系統架構。
- **工作經歷 (Work Experience)**：
  - `Freelance AI Engineer (2024.01 — 現在)`：
    - Recall-SQLite 長期記憶檢索層開發與開源。
    - `FastAPI recall-server`：三端共用記憶 RESTful API。
    - `Flutter WebView + JS Bridge` 跨裝置記憶整合。
    - `Podcast 端到端自動化產線`（製作時間減少 92%）。
    - `JoJoTrading` 事件驅動量化回測系統。
  - `耀欣數位科技 (PM)`、`國立臺北科技大學 工管所` 歷練。

---

## 2. 104 Quill 編輯器鍵盤事件注入協議

- **防破壞關鍵**：
  104 採用 Quill 富文本編輯器結合前端響應式框架（Vue/React）。若直接使用 JS 修改 `.ql-editor.innerHTML`，無法觸發內部 TextChange 事件與 Virtual DOM 更新，儲存時將導致資料清空。
- **實證注入程序**：
  1. 焦點獲取：`.ql-editor.focus()`
  2. 鍵盤事件全選與逐字模擬：`Control+A` → `type(mode="keyboard")`
  3. 觸發失焦以觸發 Vue 狀態提交：`.ql-editor.blur()`
  4. 儲存：點擊 `button[data-e2e='btn-submit']`

---

## 3. 外部 Read-back 驗收核對指標 (8 大必備字根)

1. `Recall / Hermes`
2. `SQLite + FTS5 + RRF`
3. `FastAPI recall-server`
4. `scheduled jobs`
5. `AI-assisted workflow`
6. `Freelance AI Engineer`
7. `JoJoTrading`
8. `Podcast`

---

## 4. 交付產物路徑

1. 結構化 Payload：`/mnt/d/Workspace/agent_office/data/resume_sync_payload.json`
2. 執行狀態與檢驗報告：`/mnt/d/Workspace/agent_office/data/resume_sync_execution_status.json`
3. 執行檢驗工具：`/mnt/d/Workspace/agent_office/tools/resume-sync/execute_resume_sync.py`
