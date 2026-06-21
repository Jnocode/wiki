# Wiki Schema

## Domain
AI 系統架構、量化交易開發、自動化工程、科技自媒體 — Jun 的個人知識庫。

## Conventions
- 檔名：小寫 + 連字號（如 `jojo-trading-architecture.md`）
- 每頁必有 YAML frontmatter
- 用 `[[wikilinks]]` 跨頁連結（每頁最少 2 條出鏈）
- 更新頁面時 bump `updated` 日期
- 新頁面必須加入 `index.md` 對應區塊
- 每個操作必須 append 到 `log.md`

## Frontmatter
```yaml
---
title: 頁面標題
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [從分類表選]
sources: [raw/articles/source-name.md]
---
```

## Tag Taxonomy
- **專案**: jojo-trading, baha-auto, podcast, hermes, openclaw
- **工具**: python, nodejs, docker, nas, comfyui, tts
- **概念**: rag, agent, llm, imap, oauth, fintech
- **硬體**: nvidia-gpu, nas, local-llm
- **媒體**: podcast, video-gen, content-creation
- **交易**: options, futures, backtest, taiwan-stock

## 目錄結構
- entities/     # 實體頁面（人、專案、工具、產品）
- concepts/     # 概念頁面（技術名詞、方法論）
- comparisons/  # 比較頁面（A vs B 分析）
- queries/      # 值得保留的查詢結果
- raw/          # 原始資料（永不修改）

## Update Policy
新資訊與既有內容衝突時：
1. 比較日期 — 新的通常 supersede 舊的
2. 若矛盾，同時記錄兩方（含日期與來源）
3. 在 frontmatter 標記 contradictions
