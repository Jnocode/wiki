---
title: "Agent 團隊協作契約"
type: concept
date: 2026-09-08
updated: 2026-09-10
tags: [Agent, Hermes, OpenClaw, Codex, 協作, QA]
summary: "定義小衡、小克與 Codex 的分工、交接、驗收與對外發布邊界。"
source: ["agent_office/shared/brain/01_tech/agent-collaboration-contract.md"]
confidence: high
review_after: 2026-10-10
status: active
---
# Agent 團隊協作契約

> 這是目前協作規則的 Wiki 正本。舊版 `06_tasks/AI-Agent.md` 保留作歷史參考，不得當作現行角色配置。

## 角色分工

- **小衡（Hermes）**：Tech Lead／System Architect／Grader。負責目標拆解、優先級、架構裁決、派工、風險判斷與獨立驗收。
- **小克（OpenClaw）**：Maker／Background Worker。負責 24/7 背景採集、批次執行、程式碼、產物與可重跑流程；不可自行宣告任務通過。
- **Codex**：長任務執行器。適合跨檔案開發、重構與長時間除錯；不取代 Git、Wiki、測試或外部 read-back。
- **Jun**：商業目標與重大不可逆決策的最終裁決者。

## 交接規則

長任務或跨 Agent 任務必須有：

- 任務 ID、目標、負責 Agent、唯一正本。
- 驗收條件與禁止事項。
- 已驗證事實、來源與時間。
- 嘗試過的方案、失敗原因與決策。
- 產物路徑、測試命令、退出碼與 read-back。
- 下一步與回復點。

共用帳本位置：

```text
agent_office/shared/context/<task-id>.md
```

建立與驗證工具：

```text
agent_office/tools/context-ledger/context_ledger.py
```

## 驗收閘門

Maker 交付成果包後，Grader 必須獨立檢查：

1. 檔案確實存在且內容符合要求。
2. 測試實際執行並取得退出碼。
3. 外部狀態有 read-back；僅 API 成功回應不算完成。
4. 失敗、限制與未查證內容明確標示。
5. 沒有秘密值、裸 stdout／stderr 或半成品被送到公開頻道。

## 對外發布

- Discord thread 是各產線的工作單位，更新與產物回到對應 thread。
- 對外只發布可讀成品與決策卡片，不發布中繼 log。
- 未完成或未查證的任務不得用漂亮格式包裝成成功。

## 來源

- `agent_office/shared/context/README.md`
- `agent_office/shared/context/codex-context-management.md`
- `agent_office/tools/context-ledger/README.md`
- `06_tasks/AI-Agent.md`（歷史頁，非現行正本）

## 相關頁面

- [[concepts/codex-context-management.md|Codex 上下文管理]]
- [[concepts/data-source-integrity-and-fallback.md|資料來源完整性]]
