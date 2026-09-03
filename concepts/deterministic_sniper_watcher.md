---
title: "限時高併發搶購與 Deterministic Watcher 排程架構規範"
type: concept
date: 2026-09-03
updated: 2026-09-03
tags: [concurrency, watcher, scheduling, sniper, fail_closed, timesync]
summary: "解析傳統 cron 分鐘級排程在限時搶購的失效根因，確立基於 monotonic clock、提前預熱、Fail-closed 狀態機與單一 Controller Lease 的 Deterministic Watcher 架構。"
status: active
source:
  - "03_Dev_Projects/momo-request-sniper/README.md"
  - "03_Dev_Projects/momo-request-sniper/src/momo_sniper/timesync.py"
  - "03_Dev_Projects/momo-request-sniper/src/momo_sniper/statemachine.py"
  - "03_Dev_Projects/momo-request-sniper/artifacts/evidence/verify-report.json"
confidence: high
review_after: 2026-10-03
---

# 限時高併發搶購與 Deterministic Watcher 排程架構 (t_bd98007a)

## 1. 踩坑教訓：為何分鐘級 Cron 無法勝任限時搶購

在電商或限量搶購場景（如 momo 限時特賣），傳統的系統級/代理人 Cron（如每分鐘執行一次）存在致命缺陷：
1. **量化延遲（Quantization Delay）**：Cron 觸發粒度為 60 秒，若商品於 `00:00:00.000` 開賣，Cron 可能在 `00:00:59` 才喚醒，熱門商品在數百毫秒內即秒殺售罄。
2. **Cold Start 致命懲罰**：當秒級時間到達時才發起行程，包含 Python 直譯器載入、網路 DNS 解析、TLS 握手、連線建立，至少耗費 300ms ~ 1500ms。
3. **時鐘漂移與 Wall Clock 跳躍**：依賴本地系統時間（Wall clock）會因為本機時間與遠端伺服器時間存在數百毫秒至數秒偏差，或遭遇 NTP 校時突然回撥/快進，導致提前開火（被擋/被鎖 IP）或逾期開火。

---

## 2. 核心架構：Deterministic Watcher 設計原則

針對上述痛點，標準搶購管線必須具備以下四大決定性機制：

### (1) HTTP Date NTP 伺服器時間校準 (`timesync.py`)
- 利用目標伺服器 HTTP 回應標頭中的 `Date` 計算真實伺服器偏差：
  $$\text{offset} = \text{server\_time} - \frac{t_{\text{send}} + t_{\text{recv}}}{2}$$
  $$\text{delay} = t_{\text{recv}} - t_{\text{send}}$$
- 挑選 RTT 最短樣本作為基準，計算不確定度（$\text{delay}/2 + 0.5\text{s}$）。若不確定度超過安全閥值則強制不開火（Fail-closed）。
- 排程內部強制改換為 `time.monotonic` 截止點，徹底免疫系統時間變更。

### (2) 階段式提前預熱 (Pre-warm / T-minus Pacing)
- **T-300s (心跳與租約確認)**：透過 Lease 機制確認單機唯一 Controller，防止雙重下單。
- **T-30s (事前觸發驗證)**：檢查登入態 Token/Cookie 是否有效、收件地址與支付設定是否齊全。
- **T-5s (連線池預熱)**：建立 TCP/TLS 長連線（HTTP Keep-Alive），完成 DNS 預解析，消除開賣當下的網路握手開銷。
- **T-0s (開賣瞬間)**：熱路徑直接透過現成連線送出請求，毫秒級抵達。

### (3) 熱路徑無 AI / 無 DOM 操作與 Fail-Closed 狀態機
- 狀態鏈條嚴格鎖定：`INIT` $\rightarrow$ `LEASED` $\rightarrow$ `CALIBRATED` $\rightarrow$ `ARMED` $\rightarrow$ `WAITING` $\rightarrow$ `ACQUIRING` $\rightarrow$ `CHECKOUT` $\rightarrow$ `VALIDATING` $\rightarrow$ `PAYMENT` $\rightarrow$ `SUBMIT_GATE` $\rightarrow$ `STOPPED_BEFORE_SUBMIT`。
- **防禦性設計**：總價超標、分期條件不符、多重相似選項、驗證碼出現時，立即進入 `HARD_STOP` / `HUMAN_BLOCKED`，寧可未購得，絕不錯買。

---

## 3. 專案實作驗證證據 (客觀事實數據)

本機既有專案 `03_Dev_Projects/momo-request-sniper` 驗證指標：

- **驗證執行報告**：`artifacts/evidence/verify-report.json`
- **關鍵指標數據**：
  - 秘密外洩掃描 (`scan-secrets`)：掃描 79 個檔案，**命中 0 處**，Exit Code `0`。
  - 設定嚴格驗證 (`validate-config`)：Exit Code `0`。
  - 出發前檢查 (`preflight`)：離線防護檢核正確阻斷，Exit Code `0`。
  - 狀態機正常路徑 (`dry-run-happy`)：精準停在送出閘門前（`STOPPED_BEFORE_SUBMIT`），Exit Code `0`。
  - 防超額防護 (`dry-run-price-over-cap`)：超過價格上限強制 Fail-closed，Exit Code `1`（符合非零退出預期）。
  - 分期防護 (`dry-run-missing-installment`)：缺少 12 期 0 利率強制停止，Exit Code `1`。
  - 訂單日誌查核 (`journal`)：真實下單記錄為 0，安全無外溢，Exit Code `0`。
  - **總體驗證結果**：7/7 項測試步驟全數通過（`all_green: true`）。
