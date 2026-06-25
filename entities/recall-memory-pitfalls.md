---
title: "recall-memory 踩坑記錄"
created: 2026-06-23
updated: 2026-06-25
type: entity
tags: [recall, memory, pitfalls]
wikilinks: [[recall-memory-devlog]], [[hermes-agent]]
---

# recall. 🧠 踩坑記錄

> 開發 recall-memory 與 Hermes 記憶系統整合過程中遇到的坑與解法。
> 系統性納入知識庫作為團隊參考。

---

## Honcho API 端點誤判

**坑：** 查 Honcho 用 `/api/` 舊端點拿到 404，錯誤判定 Honcho 為空殼。

**解法：**
```bash
# 正確方式：查 PostgreSQL
docker exec honcho-db psql -U honcho -d honcho -c "SELECT count(*) FROM messages;"

# 正確 API 路徑
curl -s http://localhost:8082/v3/workspaces/hermes-agent/search?q=query
```

**教訓：** 永遠先確認 API 版本和端點列表（`/openapi.json`），不要只試一條路徑就下結論。

---

## sqlite-vec 直接連線失敗

**坑：** 直接 `sqlite3.connect(recall_p0.db)` 會報 `no such module: vec0`。

**解法：** sqlite-vec 是載入式 extension，需透過 recall 的 CLI 或 API 操作：
```python
# ✅ 正確
from recall.store import SQLiteStore
store = SQLiteStore("path/to/db")
store.add(memory)

# ❌ 錯誤
conn = sqlite3.connect("recall_p0.db")  # vec0 not loaded
```

---

## Wiki API 唯讀

**坑：** Wiki SPA 後端只支援 GET，無法透過 API 建立新頁面。

**解法：** 直接 clone wiki repo（github.com/Jnocode/wiki），在 `entities/` 或 `concepts/` 下新增 markdown 後推送。

---

## Hermes memory tool 無 Honcho connector

**坑：** 以為 Honcho connector 有問題需要「修復」，但 memory tool 從未有過 Honcho connector。

**解法：** 從零建立 provider plugin。Hermes plugin 路徑 `plugins/memory/<name>/`，需實作 `MemoryProvider` abstract class。

---

## SQLite 併發寫入死鎖 (Database is Locked)

**坑：** 調用 `store_memory` 寫入 `hot` 梯度記憶時，100% 發生 `database is locked` 錯誤。

**根因：**
在 `store.add()` 中，Connection 1 開啟了資料庫事務寫入 `memories`，但在事務提交 (`commit`) 前，調用了 `_insert_vec_embedding()`，後者另外開啟了 Connection 2 嘗試寫入 `vec_embeddings`。Connection 2 被 Connection 1 的未提交鎖定堵塞，而 Connection 1 等待 Connection 2 返回，形成**自我死鎖 (Self-Deadlock)**。

**解法：**
將活動的 `conn` 連線作為參數傳遞給 `_insert_vec_embedding(..., conn=conn)`，使其在同一個 Transaction 中執行，避免重複開啟連線競爭排他鎖。同時，將所有 `sqlite3.connect` 連線加上 `timeout=30.0` 秒超時設定。

---

## Windows MCP 進程洩漏與孤兒化

**坑：** 當 IDE 重開或重載視窗時，後台掛起多個 `recall_mcp` 進程且無法關閉，導致持續鎖定資料庫。

**根因：**
在 Windows 平台下，當父進程（IDE）關閉 `stdin` 時，Python 的 `sys.stdin.readline()` 由於系統緩衝區或直譯器堵塞，未能及時回傳空字串 (EOF)，導致進程掛起成為孤兒。

**解法：**
在 `recall_mcp.py` 的啟動區塊，為 Windows 平台（`os.name == 'nt'`）註冊背景守護線程 (Daemon Thread)，透過 `ctypes.windll.kernel32` 開啟父進程 Handle。一旦偵測到父進程 (IDE) 的退出代碼不再是 `STILL_ACTIVE` (259)，子進程主動退出釋放鎖定。


## 關聯頁面
- [[recall-memory-devlog]]
- [[hermes-agent]]
