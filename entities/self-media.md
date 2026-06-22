---
title: "自媒體內容產出"
created: 2026-06-23
updated: 2026-06-23
type: entity
tags: [media, podcast]
wikilinks: [[creative-works]], [[aixquantmedia]]
---

# 自媒體內容產出

來源: `07.自媒體/`

## 內容策略

- **文章**: 每週一篇（技術教學、專業分享、品牌故事）
- **影片**: 每兩週一支（技術解說）
- **圖片**: 每週一張（品牌宣傳、技術教學）
- **發布時間**: 文章週二、圖片週五

## 已發布內容

### OpenClaw 多模態除錯 (2026-06-01)
標題: *一次修好 OpenClaw 多模態失效：從 image_model failed 到穩定看圖*

**根因分析:**
- 模型端正常（含 mmproj、API 回傳 multimodal）
- 問題在路由層：agent 模型只宣告 `"input": ["text"]`，圖片不會被路由到 image 流程
- Gateway 顯示 `image_model failed`

**修正步驟:**
1. 確認模型端有多模態: `Invoke-RestMethod "http://127.0.0.1:8080/v1/models"` → 看 `capabilities` 含 `multimodal`
2. 補全域模型能力宣告 `"input": ["text", "image"]`
3. 補 agent 模型能力宣告 `"input": ["text", "image"]`
4. Compaction 保留值調整為 `reserveTokensFloor: 20000`（與 32K 窗口相容）
5. 重啟 Gateway + `/new` session

## 創作原則

- 內容有吸引力、有價值、與品牌/專業相關
- 多樣化格式（文本、圖片、影片、音訊）
- 與粉絲互動相關聯（問卷、投票、競賽）


## 關聯頁面
- [[creative-works]]
- [[aixquantmedia]]
