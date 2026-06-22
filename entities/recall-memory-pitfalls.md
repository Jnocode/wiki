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
