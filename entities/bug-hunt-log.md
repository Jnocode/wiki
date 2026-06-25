---
title: Bug Hunt Log — 專案除錯日誌
created: 2026-06-25
updated: 2026-06-25
type: entity
tags: [openclaw, recall, python, mcp, debug]
wikilinks: [[recall-memory-pitfalls]], [[hermes-agent]]
---

# Bug Hunt Log — 專案除錯日誌

## 2026-06-25 09:25 [recall/store] 記憶儲存時 SQLite database is locked 自我死鎖與 Windows 孤兒進程洩漏
- **現象**: 
  - 調用 `store_memory` 寫入 `hot` 梯度記憶時，持續出現 `database is locked` 錯誤。
  - 重啟 IDE 或重載視窗後，後台殘留多個 `recall_mcp` 進程且無法關閉，導致持續鎖定資料庫。
- **根因**:
  - **自我死鎖 (Self-Deadlock)**: `store.add()` 開啟 Connection 1 寫入 `memories`（Transaction 尚未提交）。在同一事務中調用了 `_insert_vec_embedding()`，後者嘗試開立全新的 Connection 2 寫入 `vec_embeddings`。Connection 2 被 Connection 1 的排他寫入鎖堵塞，而 Connection 1 等待 Connection 2 返回，形成死鎖。
  - **進程殘留 (Orphan Processes)**: 在 Windows 平台下，IDE 重啟關閉 stdin 管道後，子進程因 python readline 堵塞未能收到 EOF 而掛起成為孤兒，維持對 SQLite 的連結。
- **修復**:
  - **解死鎖**: 重構 `_insert_vec_embedding()` 接受可選的 `conn=conn` 參數。在 `add()` 寫入 `hot` 梯度時，直接將 Connection 1 實例傳入共享同一筆 Transaction。
  - **清孤兒**: 在 `recall_mcp.py` 啟動時為 Windows 平台加入守護執行緒 (Daemon Thread)，定期以 `ctypes` 監控父進程。一旦父進程 (IDE) 消失，自動關閉連線並退出。
  - **連線逾時**: 在所有 `sqlite3.connect` 中將預設 timeout 增加為 `30.0` 秒。
- **影響檔案**: 
  - [store.py](file:///D:/Workspace/03_Dev_Projects/recall/src/recall/store.py)
  - [recall_mcp.py](file:///D:/Workspace/03_Dev_Projects/recall/src/recall/recall_mcp.py)
- **驗證**: 
  - 執行 `test_mcp_store.py` 寫入 `hot` 記憶測試，返回 `{"id": "...", "status": "stored"}` 成功。
  - 在 IDE 載入時，直接透過 `call_mcp_tool` 調用 `store_memory`，秒級返回儲存成功，完全恢復正常。
- **防呆**:
  - 連接 SQLite 時務必顯式傳入 `timeout` 參數以容忍並發排隊。
  - 在同一進程的 Transaction 未提交前，絕不能對同一資料庫開啟新連線嘗試寫入。
  - Stdio MCP 伺服器必須對 Windows 平台進行父進程存活監控以防孤兒化。
