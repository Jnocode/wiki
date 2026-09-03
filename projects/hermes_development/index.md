---
title: "Hermes 開發"
type: project
date: 2026-07-07
updated: 2026-07-07
tags: [hermes, agent, development]
summary: "自架 Hermes Agent 的開發專案 MOC：記憶系統以 recall plugin 為唯一 provider，Honcho fallback OFF。"
aliases: ["Hermes", "hermes agent"]
source:
  - "D:/Workspace/.antigravity/rules.md"
  - "C:/Users/Jun/.hermes/skills/hermes-multi-agent/memory-system/SKILL.md"
confidence: high
review_after: 2026-10-07
status: active
---

# Hermes 開發

## 現況（2026-07-07）

- 長期記憶：`recall-memory-hermes` plugin（3-path RRF：ANN + SQL JOIN + FTS5），
  DB 在 `~/.hermes/recall.db`；Honcho 在 :8082 待命但 fallback OFF。
- 本 vault 與 `business.db` 是 Hermes 之外新增的可信資料層；
  router 前置層見 `brain_scripts/router_query.py`（不改 Hermes core）。

> [!memory] type=decision subject=jun confidence=0.9 topic=recall_retrieval_fusion
> Jun 決定 Hermes recall 記憶檢索採三路名次融合（語意＋關鍵字＋時間的 RRF 式投票），棄用分數加權混合——實測加權混合比單用語意檢索低十幾個百分點（EP4 逐字稿有完整記錄）。

## 相關頁

- [[jun_profile|Jun]]
- [[projects/podcast/index|Podcast]]（EP4 即以此記憶系統為主題）
