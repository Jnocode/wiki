---
title: "資料來源完整性與 Provider 備援"
type: concept
date: 2026-09-08
updated: 2026-09-10
tags: [資料誠信, API, Provider, Fallback, QA]
summary: "統一即時資料查證、API 失敗處理、Quota Pool 熔斷與未驗證資訊標示規則。"
source: ["agent_office/shared/brain/01_tech/data-source-integrity-and-fallback.md"]
confidence: high
review_after: 2026-10-10
status: active
---
# 資料來源完整性與 Provider 備援

## 最高原則

所有對外數據必須多源交叉比對，並標示來源與時間。沒有即時來源就明說沒有；不得用模型記憶補造數值。

## 資料查證

- 官方文件、官方 API、原始資料集優先。
- 即時行情使用可驗證的即時端點，不從快取或模型記憶猜測。
- 404、402、429、timeout 與空回應不能靜默轉成零值或成功。
- 財報資料不完整時標示 `DATA_UNAVAILABLE`，不得下完整結論。
- AI 推論與來源事實分欄呈現。

## 備援規則

- 備援按 Quota Pool 分組，不只按模型名稱排序。
- 某池 quota 耗盡後，本輪直接跳過同池模型。
- 429 觸發池級熔斷；同一輪不得在同池換模型盲重試。
- Provider 失敗要保留可讀錯誤分類與退出狀態，但不得把秘密或完整認證回應送到 Discord。
- 配置驗證失敗時停止發布，不做假性降級。

## 來源與維護

實作與驗證工具分散於各專案產線；本頁只保存跨產線通用規則。任何 Provider、模型版本、定價或能力聲明都要重新查官方來源後再更新，並在 `review_after` 前複核。

## 相關頁面

- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
- [[concepts/discord-ai-digest-presentation.md|Discord AI 日報發布]]
