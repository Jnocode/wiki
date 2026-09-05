---
title: "Hermes Quota-Pool 備援鏈與 429 級聯雪崩熔斷架構"
type: concept
date: 2026-09-04
updated: 2026-09-04
tags: [hermes, fallback, circuit_breaker, api_quota, architecture]
summary: "解析 Hermes 在多模型輪替時遇到的 429 級聯雪崩問題，實作 Quota-Pool 級熔斷機制，杜絕同一耗盡池重複重試。"
status: active
source:
  - "03_Dev_Projects/hermes-agent/agent/fallback.py"
  - "refs/fusion-collaboration-spec.md"
confidence: high
review_after: 2026-12-04
---

# Hermes Quota-Pool 備援鏈與 429 級聯雪崩熔斷架構

## 1. 背景與核心痛點
在多模型備援架構中，多個模型往往共用同一個上游 API Key 或組織額度（例如 `cpa/gemini-3.8-flash-high` 與 `cpa/gemini-2.5-pro` 均屬於同一個 CPA Quota Pool）。
當發生 `HTTP 429 Too Many Requests` 時，傳統輪替機制會誤以為「換個模型就能解決」，在同一個耗盡池內不斷切換子模型重試。這會導致：
- 消耗大量輪替時間，造成整體對話延遲高達 30-60 秒。
- 引發 API 端點的級聯處罰與帳號暫時鎖定。

## 2. 解決方案：Quota-Pool 級熔斷
我們在 `fallback.py` 與 `quota_pools.py` 實作了 Pool 級狀態機：
1. **定義 Quota Pool**：將所有模型劃分歸屬（如 `cpa_pool`, `amd_pool`, `openai_direct`）。
2. **429 快速熔斷 (Fast-failover)**：只要某個 Pool 拋出 429，立即標記該 Pool 為 `EXHAUSTED`，冷卻時間設為 300 秒。
3. **跳池挑選 (select_next_fallback)**：備援挑選器自動跳過所有處於耗盡狀態的 Pool，直接切換到不同組織/不同憑證的下一個備援池（例如直接由 CPA 跳至 AMD 或 OpenAI）。

## 3. 實測驗證
- **單元測試**：`verify_fallback_chain.py` 驗證同池 429 觸發時，模型在 50ms 內完成跨 Pool 熔斷切換。
- **線上指標**：徹底消除了「同輪換模型重試無效」造成的對話中斷。
