---
title: "Podcast：代碼縫隙 Code Gaps"
type: project
date: 2026-07-07
updated: 2026-07-07
tags: [podcast, code_gaps, content]
summary: "Jun 的技術 Podcast 專案 MOC：主持設定、製作流程與集數導覽；集數狀態正本在 business.db。"
aliases: ["代碼縫隙", "Code Gaps", "podcast"]
source:
  - "raw/2026/2026-07-07_ep4_memory_script.md"
  - "raw/2026/2026-07-07_ep5_ai_dev_tools_script.md"
confidence: high
review_after: 2026-10-07
status: active
---

# 代碼縫隙 Code Gaps

## 節目設定

- 語言：繁體中文。
- 主持：柴柴（S1，AI 主持人，吐槽擔當）×
  傑諾（S2，人類工程師，即 [[jun_profile|Jun]]）。
- 形式：雙人對談，上半部雜談兼主題預覽、下半部硬核內容（來源：EP4/EP5 稿件結構）。

## 集數狀態（正本在 business.db，以下為唯讀渲染）

<!-- db:begin table=podcast_episodes -->
> 唯讀渲染區塊（表 `podcast_episodes`，共 2 列）：狀態正本在 `shared/db/business.db`；手改此區塊會被 business_sync.py 偵測為 drift 並以 DB 覆蓋。

| ep_no | title | status | script_path | publish_date |
|---|---|---|---|---|
| 4 | AI 的記憶系統 | scripting | raw/2026/2026-07-07_ep4_memory_script.md | — |
| 5 | AI 開發工具的真實面貌 | scripting | raw/2026/2026-07-07_ep5_ai_dev_tools_script.md | — |
<!-- db:end -->

> 查詢狀態請走 `brain_scripts/router_query.py` 或直接 SQL；
> 本區塊手改視為 drift，DB 值勝出。

## 集數筆記

- [[projects/podcast/ep04_notes|EP4：AI 的記憶系統]]
- [[projects/podcast/ep05_notes|EP5：AI 開發工具的真實面貌]]

## 製作流程備忘

- 稿件在 `agent_office/temp/EPxx/` 撰寫，完稿後經 `ingest_source.py` 歸檔至 `raw/2026/`。
- TTS 生成會佔用 LM Studio（port 1234），與 recall 的 embedding 模型互斥。
