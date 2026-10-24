---
title: "長程自治 AI 工作流：額度冷卻自癒與確定性斷點接力架構"
type: concept
date: 2026-10-23
updated: 2026-10-24
tags: [agent, circuit_breaker, quota_relay, checkpoint, ralph_loop, architecture]
summary: "結合雙狀態機解耦、配額池連帶熔斷、Half-Open 探針自癒與 Fresh Context 確定性斷點接力，實現跨越 API 額度冷卻的長程無人值守產出架構。"
source: ["agent_office/shared/brain/01_tech/autonomous-self-healing-quota-relay-architecture.md"]
confidence: high
review_after: 2026-11-23
status: active
---
# 長程自治 AI 工作流：額度冷卻自癒與確定性斷點接力架構

## 1. 核心設計哲學：耐久控制面與狀態外置

在建立能夠跨越數小時乃至數天無人值守的 AI 自動化工作流時，社群最常見的致命架構陷阱是**「讓正在被限流的模型自己處理自己的冷卻」**（例如在對話迴圈內 `sleep 600`、或由 Cron 定時喚醒長會話詢問「額度好了沒」）。這種模式在遭遇池級 Rate Limit 或帳號凍結時，會瞬間引發對話死鎖、Token 暴增與參數污染。

**工程底線**：
> **「備援鏈只能換模型；真正的長程自治，必須有一個完全不依賴 LLM 存活的耐久控制面（Durable Control Plane）與完全外置於磁碟的狀態機（State Externalization）。」**

---

## 2. 雙狀態機解耦架構（Two Decoupled State Machines）

系統將**「推論資源可用性」**與**「業務任務生命週期」**徹底解耦為兩組獨立運作的狀態機：

```
【資源層：Quota & Circuit Breaker】（純 Python / 磁碟，零 LLM 消耗）
   [HEALTHY] ──(429 / 503)──► [OPEN / COOLDOWN]
      ▲                            │ (記錄 reset_at，設定冷卻計時)
      │                            ▼
   (探針 200) ◄── [HALF-OPEN] ◄── (時間到達 reset_at)
                    │ (單一 1-token Canary 探針)
                    └──(仍為 429)──► 指數退避加倍，回 OPEN

─────────────────────────────────────────────────────────────

【任務層：Durable Task Lifecycle】（依賴磁碟 Checkpoint）
   [READY] ──► [RUNNING] ──► [STEP COMPLETED] ──► [CHECKPOINT SAVED]
                   │ (偵測到 LLM 撞冷卻)                  │
                   ▼                                     ▼
             [SUSPENDED] ◄───────────────────────────────┘
          (進程優雅退出，釋放記憶體)
                   │
                   ▼ (等待資源層發出 RESUME 信號)
             [RESUME AT STEP N+1] ──► [INDEPENDENT QA] ──► [DELIVERED]
```

### 資源層（Resource Layer）
* 獨立持久化於磁碟狀態檔（`~/.hermes/runtime_cooldown.json`）。
* 在發送任何 LLM 請求或派工子代理前，控制器優先查詢該表。處於 `COOLDOWN` 狀態的供應商／配額池直接在進入點攔截，**零成本阻斷無效請求**。

### 任務層（Task Layer）
* 任務被嚴格拆解為具有冪等性保證的微步驟（Step）。
* 每個步驟完成後，立即將中間產物雜湊（SHA256）與執行指標落盤至 `checkpoint.json`。遇中斷時進程優雅退場，等待資源層恢復信號再行喚醒。

---

## 3. 錯誤分型與配額池連帶熔斷（Pool-Level Circuit Breaker）

傳統 Fallback 機制僅檢查 HTTP 狀態碼，容易將「整池額度耗盡」誤判為「單一模型暫時繁忙」，進而在同一帳號內輪流切換子模型重試（如 Claude Opus ➔ Sonnet ➔ Haiku），引發連鎖空轉。

本架構實施三層錯誤分型：
1. **短暫並發限制（Concurrency Spike）**：
   * 錯誤特徵：`global_concurrency_rate_limit_exceeded`。
   * 處置策略：微退避（Jittered Backoff 3~10 秒），降低併發度即可，**不標記長時間冷卻**。
2. **速率窗口耗盡（TPM / RPM Rate Limit）**：
   * 錯誤特徵：HTTP 429 帶有 `Retry-After` 或 `x-ratelimit-reset` 標頭。
   * 處置策略：解析標頭計算精確的 `cooldown_until = now + delay`，將該 Provider 移入 `COOLDOWN`。
3. **帳號／代理池每日或每週配額耗盡（Pool Quota Exhausted / 503 No Account）**：
   * 錯誤特徵：`daily_limit_exceeded`、`no_available_account`、或週額度耗盡通知。
   * 處置策略：**整池硬鎖定（HARD_LOCK）** 直至下一個重置週期，備援鏈直接跨越整個故障域（Cross-Domain Jump），跳至完全不相關的獨立第三方供應商。

---

## 4. 半開探針機制（Half-Open Canary Probe）

當系統冷卻計時到達（`now >= cooldown_until`）時，嚴禁立即將排隊堆積的生產任務全量湧入上游。

* **哨兵排程（Sentinel Daemon）**：由輕量背景腳本（`provider_recovery_sentinel.py`，純 Python 運行）接管。
* **狀態轉移**：冷卻時間到達後，狀態機轉為 `HALF-OPEN`。
* **探針行為**：哨兵發送單一極小探針（`max_tokens=1` 或 `Reply: PONG`，零 side-effect）：
  * **探針 HTTP 200** ➔ 判定上游額度真實恢復，熔斷器復位為 `CLOSED / HEALTHY`，生產隊列漸進放行（Ramp-up）。
  * **探針依然 429/503** ➔ 說明上游仍未就緒，立即套用指數退避與隨機擾動（Exponential Backoff + Jitter），將冷卻時間加倍並退回 `OPEN`。

---

## 5. 確定性斷點接力與 Fresh Context 循環

借鏡 2026 年 Anthropic 官方長程自主研究與 Ralph Wiggum 模式：

1. **One item per loop**：每次 Agent 執行循環僅專注推進一個明確的微步驟（例如：產生大綱、寫一段邏輯、跑單一測試），完成後立即 Commit 並退場。
2. **100% 乾淨上下文（Fresh Context）**：下一輪 Agent 啟動時擁有零負擔的全新上下文視窗，完全消除「對話長度膨脹導致指令遺忘與參數洩漏（Context Rot）」的頑疾。
3. **Default-FAIL 硬契約**：
   * 所有待辦事項預設 `passes: false`。
   * 唯有通過獨立驗收程式（Grader）實測 Exit 0，系統才准翻轉狀態。
4. **Outbox 冪等保護**：
   * 對外產生副作用的動作（如 Podcast 上架、社群廣播、Git Push）均附帶唯一 `idempotency_key`。
   * 斷點恢復重跑時，已完成交付的步驟自動略過，保證零重複發送。

---

## 6. 全雲端冷卻時的離線降級作業（Graceful Local Fallback）

當遇到外部網絡極端故障或全雲端 API 同時進入冷卻時，控制器自動執行分流：
* **本地算力降級通道**：
  * 執行本機音訊 FFmpeg 轉碼與 -16 LUFS 廣播級壓制。
  * 執行本地單元測試套件與覆蓋率分析。
  * 執行 Wiki 知識庫 Lint 檢查與向量嵌入索引建立。
* **安靜掛起（Silent Park）**：若隊列中皆為純雲端生成任務，系統直接轉入靜默待機，終止所有 CPU Polling，靜候 OS 定時器（Task Scheduler / Cron）於半開探針窗口觸發喚醒。

## 相關頁面

- [[concepts/data-source-integrity-and-fallback.md|資料來源完整性]]
- [[concepts/hermes_quota_pool_circuit_breaker.md|Quota-Pool 熔斷架構]]
- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
