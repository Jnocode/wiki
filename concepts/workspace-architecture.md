---
title: "Workspace 工作區架構與整理規則"
type: concept
date: 2026-09-08
updated: 2026-09-12
tags: [Workspace, 架構, 檔案管理, Agent, 維運]
summary: "定義 D:\\Workspace 的資料邊界、正本判定、搬移驗證與 artifacts 生命週期。"
source: ["agent_office/shared/brain/90_system/workspace-architecture.md"]
confidence: high
review_after: 2026-10-12
status: active
---
# Workspace 工作區架構與整理規則

## 目前可確認的邊界

| 類別 | 路徑 | 用途 |
|---|---|---|
| 團隊辦公室正本候選 | `D:/Workspace/03_Dev_Projects/agent_office` | 共用 brain、context、工具與產線腳本 |
| 專案產物 | `D:/Workspace/artifacts/<task-name>/` | 報告、驗證結果、截圖、備份 |
| 暫存 | `D:/Workspace/03_Dev_Projects/agent_office/temp/` 或 `shared/` | 交換檔與運行暫存 |
| 知識庫 | `D:/Workspace/03_Dev_Projects/agent_office/shared/brain/` | 長期規則、決策與可重用 SOP |
| 任務上下文 | `D:/Workspace/03_Dev_Projects/agent_office/shared/context/` | 長任務交接帳本，不取代 Wiki |

## 雙 `agent_office` 風險

工作區根目錄與 `03_Dev_Projects` 下曾同時存在同名 `agent_office`。在未完成引用、排程、服務依賴盤點前：

- 不直接搬移或刪除任一份。
- 不宣稱已完成正本合併。
- 新增長期 Wiki、context 與工具優先放在 `03_Dev_Projects/agent_office`，因目前共用 brain 與任務帳本均在此。
- 任何正式服務路徑變更都要先備份，再做 smoke test。

## 搬移流程

1. 唯讀盤點檔案、引用、排程與服務依賴。
2. 判定唯一正本並記錄理由。
3. 備份原檔到同目錄或任務 artifact 的 `backups/`。
4. 小批搬移，不混合刪除。
5. 更新引用與啟動器。
6. 執行 smoke test、服務健康檢查與路徑 read-back。
7. 觀察後才處理舊副本。

## 目錄衛生

- 根目錄不新增臨時雜項。
- 二進位產物放 `02_Resources` 或任務 artifacts，不放 shared brain。
- shared brain 只放 Markdown 與必要索引。
- Wiki 放可重用規則；一次性 log、截圖、wav、JSON 與測試輸出留在 artifacts。
- 修改既有檔案前先備份。

## 狀態

本頁是現行整理規則，不代表雙 `agent_office` 已合併；正本判定仍是待辦事項。

## 相關頁面

- [[concepts/runtime-environment-map.md|Runtime 環境圖]]
- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
