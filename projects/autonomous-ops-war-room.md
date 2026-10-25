---
title: "自治運營戰情室 — 五大核心營運指標常態看板"
type: report
date: 2026-10-25
updated: 2026-10-25
tags: [war_room, telemetry, quota_relay, auto_refill, audit]
summary: "長程自治 AI 工作流實時戰情室：即時呈現已驗收實質成果、真實 Token 帳單、派工排隊清冊、全產線 29 條健康矩陣與監督責任鏈心跳。"
status: active
---

# 🛰️ 自治運營戰情室 (Autonomous Ops War Room)

> **資料更新時間**：`2026-10-25T01:58:28.094912+00:00`  
> **系統 Epoch**：`2026-10-25` | **架構正本**：[[concepts/autonomous-self-healing-quota-relay-architecture.md]]  
> **資料源狀態**：本機 `ops_war_room_status.json` 與公網 GitHub Pages 交叉比對 **100% 一致 (HTTP 200)**。

---

## 1. 實質運作成果清冊 (Verified Outcomes & Cryptographic Proof)

> 所有交付產物皆經過獨立 Grader 執行測試 Harness 驗收，嚴格遵循 Default-FAIL 原則，並附上磁碟實體 SHA256 雜湊。

| 任務 ID | 說明 | 檔案路徑 | SHA256 雜湊 (前 16 碼) | 驗收狀態 |
| :--- | :--- | :--- | :--- | :--- |
| `quota_relay_slice1_receipt` | Slice 1 獨立 QA 驗收收據 (F01-F07 全部 PASS) | `artifacts/quota-relay-self-healing-20261024/verification_receipt.json` | `9e15782908fbdc4b...` | **PASS** |
| `quota_relay_slice2_receipt` | Slice 2 獨立 QA 驗收收據 (F08-F14 全部 PASS) | `artifacts/quota-relay-self-healing-20261024/verification_receipt_slice2.json` | `b64e12f3a05df6a2...` | **PASS** |
| `quota_relay_e2e_drill_receipt` | E2E 故障注入與自動補位整合演練收據 (Phase 1-5 全部 PASS) | `artifacts/quota-relay-self-healing-20261024/e2e_drill_receipt.json` | `059ac6412a100cfb...` | **PASS** |
| `quota_relay_architecture_spec` | 長程自治 AI 工作流：額度冷卻自癒與確定性斷點接力架構正本 | `03_Dev_Projects/wiki/concepts/autonomous-self-healing-quota-relay-architecture.md` | `345593bc6e614f13...` | **PASS** |

---

## 2. 即時額度與 Token 帳單 (Live Token Ledger & Pool Status)

> 自 `state.db` 即時聚合近 3 日真實調用量（統計場次：**854 場**）。

| 模型名稱 | 配額池 (Pool ID) | 執行場次 | Input Tokens | Output Tokens | Cache Read Tokens | 預估費用 (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `gemini-3.8-flash-high` | `cpa_pool` | 285 | 49,696,116 | 1,096,512 | 244,379,250 | $0.0000 (Proxy/Pool) |
| `default` | `cpa_pool` | 6 | 27,196,852 | 235,271 | 154,637,215 | $0.0000 (Proxy/Pool) |
| `gpt-5.6-sol` | `codex_pool` | 169 | 16,253,649 | 1,831,821 | 224,569,856 | $0.0000 (Proxy/Pool) |
| `gpt-6.1-sol` | `codex_pool` | 106 | 12,543,507 | 919,606 | 127,819,624 | $0.0000 (Proxy/Pool) |
| `gemini-3.6-flash-high` | `cpa_pool` | 188 | 8,654,521 | 428,652 | 31,107,927 | $0.0000 (Proxy/Pool) |
| `claude-opus-5` | `codex_pool` | 170 | 8,495,981 | 106,470 | 0 | $0.0000 (Proxy/Pool) |
| `gemini-3.7-flash-high` | `cpa_pool` | 91 | 7,990,835 | 156,097 | 19,658,850 | $0.0000 (Proxy/Pool) |
| `claude-opus-4-6-thinking` | `codex_pool` | 139 | 4,855,942 | 322,377 | 29,834,684 | $0.0000 (Proxy/Pool) |
| `gpt-5.6-luna` | `codex_pool` | 64 | 4,418,851 | 532,691 | 47,476,736 | $0.0000 (Proxy/Pool) |
| `DeepSeek-V4-Flash` | `codex_pool` | 52 | 2,500,693 | 420,418 | 13,408,640 | $0.0000 (Proxy/Pool) |
| `Qwen3.8-Flash-Next` | `amd_pool` | 20 | 2,455,274 | 466,983 | 16,593,283 | $0.0000 (Proxy/Pool) |
| `deepseek-v4-pro` | `codex_pool` | 15 | 2,259,248 | 40,383 | 6,914,644 | $0.1151 |
| `Qwen3.6 35B` | `amd_pool` | 35 | 1,492,612 | 125,640 | 19,816,064 | $0.0000 (Proxy/Pool) |
| `gpt-5.5` | `codex_pool` | 1 | 1,167,524 | 49,251 | 26,245,888 | $0.0000 (Proxy/Pool) |
| `google/gemma-4-12b-qat` | `codex_pool` | 2 | 609,631 | 18,500 | 0 | $0.0000 (Proxy/Pool) |
| `claude-sonnet-4-6` | `codex_pool` | 15 | 597,509 | 35,140 | 2,599,070 | $0.0000 (Proxy/Pool) |
| `deepseek-v4-flash` | `codex_pool` | 7 | 577,297 | 143,678 | 35,926,912 | $0.0148 |
| `claude-opus-4-8` | `codex_pool` | 2 | 262,080 | 56,549 | 6,357,568 | $0.0000 (Proxy/Pool) |
| `gpt-6-sol` | `codex_pool` | 5 | 215,990 | 41,633 | 2,717,568 | $0.0000 (Proxy/Pool) |
| `claude-opus-4-6` | `codex_pool` | 2 | 172,096 | 15,064 | 1,565,724 | $0.0000 (Proxy/Pool) |
| `nvidia/nemotron-3-super-120b-a12b` | `codex_pool` | 1 | 113,361 | 12,325 | 1,066,208 | $0.0000 (Proxy/Pool) |
| `unsloth/gemma-4-E4B-it-GGUF:UD-Q4_K_XL` | `codex_pool` | 1 | 91,988 | 1,278 | 134,226 | $0.0000 (Proxy/Pool) |
| `Qwen3.6-35B-A3B-Q4_K_M.gguf` | `amd_pool` | 3 | 90,694 | 15,224 | 713,475 | $0.0000 (Proxy/Pool) |
| `gpt-5.6-terra` | `codex_pool` | 4 | 85,825 | 5,298 | 124,928 | $0.0000 (Proxy/Pool) |
| `qwen/qwen3.8-27b` | `amd_pool` | 1 | 83,904 | 2,252 | 0 | $0.0000 (Proxy/Pool) |
| `deepseek-chat` | `codex_pool` | 3 | 69,966 | 627 | 0 | $0.0000 (Proxy/Pool) |
| `GPT-5.5` | `codex_pool` | 1 | 42,695 | 5,842 | 883,593 | $0.0000 (Proxy/Pool) |
| `gemini-3.1-pro-low` | `cpa_pool` | 3 | 40,917 | 165 | 12,079 | $0.0000 (Proxy/Pool) |
| `gemini-4-argon-high` | `cpa_pool` | 1 | 36,112 | 1,316 | 0 | $0.0000 (Proxy/Pool) |
| `Deepseek-V4 Pro` | `codex_pool` | 1 | 14,210 | 158 | 30,822 | $0.0000 (Proxy/Pool) |
| `unknown` | `codex_pool` | 2 | 6,642 | 562 | 47,422 | $0.0000 (Proxy/Pool) |

---

## 3. 派工與排隊原因清冊 (Queue Census & Auto-Refill State)

> 自動補位調度器（AutoRefillController）實時監控工作槽位與額度冷卻。嚴禁自動拉取 `todo` 或業務阻擋卡片。

| 卡片 ID | 任務標題 | 狀態 | 負責 Agent | 排隊/等待原因 | 預期喚醒時間 |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `card_ec176f8d` | Slice 1: 配額冷卻登記表與錯誤分類狀態機 | **`done`** | main (🦞🦐 小克) | — | — |
| `card_daba206d` | Slice 2: 自動補位調度器、半開哨兵探針與五大營運指標 | **`done`** | main (🦞🦐 小克) | — | — |
| `wb_4125c395` | EP21 心理成長主軸 draft（Option A：10/23五檔期從簡、10/28三上架） | **`todo`** | main (🦞🦐 小克) | `WAITING_FOR_SLOT` | 2026-10-25T14:00:00+08:00 |
| `wb_f48045f2` | Podcast 聽感 SOP v1：EP20 私人樣本與獨立全片驗收 | **`todo`** | main (🦞🦐 小克) | `WAITING_FOR_DEPENDENCY` | 2026-10-25T18:00:00+08:00 |

---

## 4. 全產線健康狀態矩陣 (29 Pipeline Health Matrix)

> 實時統計：**正常 18 條** | **報錯 4 條** | **手動暫停 7 條** | 總計 **29 條**

### 🚨 異常管線根因診斷 (Truthful Error Reporting)
- **`browser-ops-watchdog`** (`every 360m`)：
  - **錯誤根因**：`Script exited with code 2 (Cua Driver daemon contract version 0.8.0 mismatch SDK 0.7.0)`
  - **上次執行**：`2026-10-25T03:58:50`
- **`xiaoke-brain-distill-daily`** (`0 22 * * *`)：
  - **錯誤根因**：`Script exited with code 1 (wiki_lint detected broken wikilinks & missing frontmatter)`
  - **上次執行**：`2026-10-24T22:01:59`
- **`Hermes 夜間自動更新`** (`0 4 * * *`)：
  - **錯誤根因**：`Script exited with code 1 (檢查或狀態讀寫超時/失敗)`
  - **上次執行**：`2026-10-25T04:00:44`
- **`巴哈勇者福利社每日免費抽獎`** (`5 0 * * *`)：
  - **錯誤根因**：`Script exited with code 1 (狀態回報 PARTIAL_OR_BLOCKED，點擊等待逾時)`
  - **上次執行**：`2026-10-25T00:25:50`

### 🟢 正常運行管線 (Healthy Pipelines)
- `tw-stock-close-report` (35 15 * * 1-5) — 上次執行: `2026-10-23T15:53:28`
- `wiki-auto-sync` (0 2 * * *) — 上次執行: `2026-10-25T02:00:45`
- `agent-health-check` (0 */6 * * *) — 上次執行: `2026-10-25T06:00:14`
- `f5-subscription-monitor` (0 */6 * * *) — 上次執行: `2026-10-25T06:00:23`
- `discord-vskin-gate-projection` (20 10 * * *) — 上次執行: `2026-10-24T10:20:09`
- `content-pipeline-github-sync` (30 8 * * 1) — 上次執行: `2026-10-19T08:31:09`
- `threads_token_watchdog` (every 2880m) — 上次執行: `2026-10-24T14:05:17`
- `platform_auth_weekly_check` (15 9 * * 1) — 上次執行: `2026-10-19T09:16:04`
- `podcast-wed-fri-release-verifier` (5,35 18 * * 3,5) — 上次執行: `2026-10-23T18:40:20`
- `ai-frontier-tech-scout` (0 8 * * *) — 上次執行: `2026-10-25T08:07:03`
- `nightly-dreaming-consolidation` (0 3 * * *) — 上次執行: `2026-10-25T03:00:14`
- `unattended-closure-warden-20261016` (every 20m) — 上次執行: `2026-10-25T09:38:38`
- `codex-parallel-session-watcher` (every 10m) — 上次執行: `2026-10-25T09:44:14`
- `quant-lifeline-evening` (10 16 * * 1-5) — 上次執行: `2026-10-23T16:10:10`
- `quant-lifeline-morning-executor` (30 8 * * 1-5) — 上次執行: `2026-10-23T08:30:08`
- `hindsight-liveness-warden` (every 30m) — 上次執行: `2026-10-25T09:34:13`
- `ase-learning-liveness-warden` (every 30m) — 上次執行: `2026-10-25T09:28:13`
- `recall-oss-daily-maintenance` (0 10 * * *) — 上次執行: `2026-10-24T10:15:11`

---

## 5. 監督責任鏈與自癒心跳 (Supervision & Audit Chain)

- **系統架構師兼 Grader**：`Xiao Heng (小衡 / System Architect & Grader)`
- **執行 Agent (Maker)**：`Xiao Ke (小克 / main, Maker)`
- **協作鐵律**：`Maker ≠ Grader 絕對分權隔離，Default-FAIL 零口頭承諾驗收`
- **熔斷與自癒政策**：`Pool-Level 硬隔離，TPM/RPM 指數退避，429 禁同池即時重試，1-token Canary 探針 200 自動解鎖`
- **最近 Grader 巡檢心跳**：`2026-10-25T01:58:28.094889+00:00`
- **哨兵探針心跳 (Sentinel Liveness)**：`2026-10-25T01:58:28.094908+00:00`
