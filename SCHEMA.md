# Wiki Schema

## Domain
AI 系統架構、量化交易開發、自動化工程、科技自媒體 — Jun 的個人知識庫。

## Conventions
- 檔名：小寫 + 連字號（如 `jojo-trading-architecture.md`）
- 每頁必有 YAML frontmatter
- 用 `[[wikilinks]]` 跨頁連結（每頁最少 2 條出鏈）
- 更新頁面時 bump `updated` 日期
- 每次修改必須 append 到 `log.md`

## Frontmatter
```yaml
---
title: 頁面標題
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept
tags: [從分類表選]
wikilinks: [[相關頁面]], [[另一頁]]
---
```

## Tag Taxonomy
- **專案**: jojo-trading, baha-auto, podcast, hermes, openclaw, recall
- **工具**: python, nodejs, docker, nas, comfyui, tts, mcp
- **概念**: rag, agent, llm, memory, fintech
- **硬體**: nvidia-gpu, nas, local-llm
- **媒體**: podcast, video-gen, content-creation, self-media
- **交易**: options, futures, backtest, taiwan-stock
- **學習**: ie, book, course

## 目錄結構
- entities/     # 實體頁面（人、專案、工具、產品）
- concepts/     # 概念頁面（技術名詞、方法論）

## Update Policy
新資訊與既有內容衝突時：
1. 比較日期 — 新的通常 supersede 舊的
2. 若矛盾，同時記錄兩方（含日期與來源）
3. 在 frontmatter 標記 contradictions
