# Wiki Log

> 操作紀錄。append-only。

## [2026-06-20] create | Wiki 初始化
- 位置: D:\Personal_Website\wiki
- SCHEMA.md, index.md, log.md 建立完成
- 等待首次 ingest

## [2026-06-20] ingest | Hermes Agent
- 建立 entities/hermes-agent.md

## [2026-06-20] ingest | Agent Office Shared
- 建立 entities/agent-office-shared.md
- 來源: D:\Workspace\agent_office\shared\ (77 md, Obsidian vault)

## [2026-06-20] ingest | 批次 ingest brain 知識庫
- 建立 entities/openclaw.md
- 建立 entities/aixquantmedia.md
- 建立 entities/jojo-trading.md
- 建立 concepts/model-training.md
- 來源: D:\Workspace\agent_office\shared\brain/ (77 md files)
- 跳過: 07_notes(日記), 03_meetings(會議), 06_tasks(任務) — 時效性內容


## 2026-06-23
- 新增 recall-memory-devlog.md (entities/)
- 新增 recall-memory-pitfalls.md (entities/)
- 補齊 11 頁 YAML frontmatter
- 補齊 wikilinks（每頁 ≥2 條出鏈）
- 修復 CORS [*] → restrict origins
- 修復 datetime.utcnow → datetime.now(timezone.utc)
- 修復 config.py 硬編碼 → os.getenv fallback
- SCHEMA.md 同步：移除 comparisons/ queries/ raw/ 定義

## 2026-06-23 (二修)
- server/backend/main.py: CORS [*] → 限制 origin
- server/backend/models.py: 3處 datetime.utcnow → timezone.utc
- server/backend/config.py: 硬編碼 → os.getenv fallback
- 修正 10 頁 frontmatter 三重括號 [[[xxx]]] → [[xxx]]

## 2026-06-25
- 更新 entities/recall-memory-pitfalls.md，納入 SQLite 併發寫入自我死鎖與 Windows MCP 孤兒進程洩漏的根因及修復方案。
- 併入本機除錯日誌至 entities/bug-hunt-log.md，將 2026-06-25 每日記憶存檔移入 entities/memories/2026-06-25.md。重新初始化並索引 SQLite 知識庫資料庫。


