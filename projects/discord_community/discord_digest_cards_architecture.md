---
title: "Discord 每日動態摘要卡片生成架構與預覽驗收標準"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [discord, cards, automation, qa, presentation]
summary: "打造 Discord 每日動態摘要卡片管線，支援前端 HTML/PNG 視覺預覽、結構化 JSON 與嚴格 QA 驗收。"
status: active
source:
  - "artifacts/discord-digest-cards/release/RESULT.md"
  - "artifacts/discord-digest-cards/qa_core.py"
confidence: high
review_after: 2026-12-04
---

# Discord 每日動態摘要卡片生成架構與預覽驗收標準

## 1. 任務背景
為了將每日大量 AI 前沿熱點、產線進度與重要決策快速同步至社群與團隊，需要一套「內部極致效率，對外只交成品」的卡片產線。

## 2. 核心架構
- **三層隔離管線**：
  1. **數據採集層**：由掃描器產出去重後的純文字與主題標籤。
  2. **視覺渲染層**：以純 CSS Grid 與自適應字體產出標準 HTML 預覽卡片，並可透過 Playwright 截圖為高畫質 PNG。
  3. **QA 驗證層**：`qa_core.py` 嚴格檢查卡片標題字數、是否有長句斷行破版、是否有未解析的 raw markdown 標記。

## 3. 落地成果
- 產出結構化預覽：`artifacts/discord-digest-cards/visual-preview/index.html`。
- 全自動化排程整合：確保每日晨間自動生成無瑕疵卡片並交付至對應頻道。
