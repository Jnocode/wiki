---
title: "記憶分家架構（Memory / Wiki / Business DB Separation）"
type: concept
date: 2026-07-07
updated: 2026-07-07
tags: [memory, architecture, governance, ai_memory]
summary: "本 brain 系統自身的設計原則：四層邊界、canonical home、provenance 鏈、寫入閘門與預設不記住。"
aliases: ["記憶分家", "memory architecture", "四層邊界"]
source:
  - "D:/Workspace/artifacts/f5-memory-wiki-architecture/fable5_architecture_2026-07-07_03-00-06.md"
confidence: high
review_after: 2026-10-07
status: active
---

# 記憶分家架構

> 這頁是本 vault 系統自身的設計蒸餾；完整設計文件見 frontmatter source。
> 資料契約正本是 [[SCHEMA.md|SCHEMA]]，本頁只講「為什麼這樣設計」。

## 核心原則

**一份資料只有一個 canonical home，其他位置只放指標。**
系統的品質不取決於放進什麼，而取決於擋掉什麼——90% 的對話內容
本來就該留在 session log 自然死去（預設不記住）。

## 四層邊界

| 層 | 定位 | 正本位置 |
|---|---|---|
| Raw Source | 不可變原始佐證，append-only | `raw/` |
| LLM Wiki | 人類可讀的蒸餾知識網 | vault 的 entity/concept/project 頁 |
| Recall Memory | AI 快速召回的原子事實（≤280 字） | recall plugin（本系統只經 adapter 供料） |
| Business DB | 可計算狀態（能被 `SELECT count(*)` 回答） | `shared/db/business.db` |
| Session Log | 短期工作記憶，預設不入長期記憶 | Honcho |

## Provenance 鏈（誠信原則的工程化）

Recall memory → `source_ref` → Wiki 頁 → frontmatter `source` → `raw/` 原文
→ 外部 URL。**斷鏈即 lint error**；摘要的摘要（source 指向另一筆 memory）被禁止。

## 寫入閘門

- 唯一寫入入口 `ingest_source.py`：hash 去重、二進位拒收、低信心進 `inbox/` 檢疫。
- Wiki → Recall 只經 `> [!memory]` callout + `sync_recall.py` 三條准入規則
  （無 source_ref 不寫入、content_hash 去重、confidence < 0.5 拒收）。
- session → 長期記憶只經 `persona_writer.py`（每次上限 5 筆、必附引文、進待審佇列）。
- 舊資料回填只經 `backfill_select.py` 選擇性抽取，禁止全量匯入。

## 相關頁

- [[projects/hermes_development/index|Hermes 開發]] — recall plugin 與 router 接點
- [[queries/weekly_review|每週回顧查詢配方]] — 體檢與審核例行程序
