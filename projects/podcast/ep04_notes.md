---
title: "EP4 筆記：AI 的記憶系統"
type: project
date: 2026-07-07
updated: 2026-07-07
tags: [podcast, code_gaps, ep4, ai_memory]
summary: "EP4 完稿筆記：無狀態 LLM、外接記憶、三路檢索與名次融合（RRF 式投票）取代分數加權的實戰教訓。"
aliases: ["EP4", "ep4"]
source:
  - "raw/2026/2026-07-07_ep4_memory_script.md"
confidence: high
review_after: 2026-10-07
status: active
---

# EP4：AI 的記憶系統

> 原文逐字稿：`raw/2026/2026-07-07_ep4_memory_script.md`（33KB 完稿）。
> 集數狀態正本在 `business.db` 的 `podcast_episodes`（ep_no=4）。

## 稿件結構

INTRO → 上半部（雜談兼主題預覽）→ 下半部（主題深入）→ OUTRO，
柴柴（S1，AI）× 傑諾（S2，Jun）雙人對談。

## 核心內容（蒸餾）

1. **AI 沒有記性**：LLM 對話本質無狀態，「同一對話內記得」也是每輪重讀全部逐字稿
   （便利商店速讀店員比喻）。
2. **外接腦袋**：解法是外接記憶——重要事實寫入外部儲存，對話前檢索相關片段給模型。
3. **三把武器**：語意搜尋（座標點/embedding）、關鍵字搜尋（字面精確）、時間排序（新者優先），
   各有強弱與破洞。
4. **加權混合的失敗**：分數尺度不同（國文/數學計分比喻）→ 三合一特調比單用語意搜尋
   低十幾個百分點；正規化與調權重都救不回（打地鼠）。
5. **Embedding 各向異性**：所有座標點擠在「演唱會搖滾區」，換更大模型也一樣——
   已知技術現象，非資料或模型大小問題。
6. **最終架構：名次融合**：只看名次不看分數，名次換票數加總（花式滑冰裁判制），
   尺度統一、對異常值免疫、幾乎零參數。

> [!memory] type=fact subject=hermes_agent confidence=0.9 topic=recall_retrieval
> Hermes recall 記憶系統的檢索採三路名次融合（語意 + 關鍵字 + 時間，RRF 式投票），是 Jun 實測後棄用分數加權混合的結果（EP4 有完整敘述）。

## 相關頁

- [[projects/podcast/index|Podcast MOC]]
- [[projects/podcast/ep05_notes|EP5：AI 開發工具的真實面貌]]
