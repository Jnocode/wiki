---
title: "Codex 上下文管理與跨 Agent 帳本"
type: concept
date: 2026-09-08
updated: 2026-09-10
tags: [Codex, 上下文, Hermes, OpenClaw, 任務管理]
summary: "將 Codex 的長工作階段上下文與團隊共用 Markdown 任務帳本分層，避免把模型歷史誤當成驗收證據。"
source: ["agent_office/shared/brain/01_tech/codex-context-management.md"]
confidence: high
review_after: 2026-10-10
status: active
---
# Codex 上下文管理與跨 Agent 帳本

## 架構結論

採雙層上下文：

1. **Codex 層**：使用 Codex 的實驗性 context management，處理同一個 Codex 長工作階段內的筆記與可搜尋歷史。
2. **團隊層**：使用 Markdown 任務帳本，讓 Hermes、OpenClaw、Codex 與人類共享同一份可讀、可追蹤、可驗收的狀態。

兩層都不能取代 Git、測試、artifact 或外部狀態 read-back。

## 已驗證配置

```toml
[features.context_management]
experimental_mode = true
```

查證結果：

- Codex CLI：`0.153.4`。
- TOML 可解析。
- `codex exec --help` exit 0。
- 設定備份位於使用者 Codex 設定目錄；不得將備份內容複製到 Wiki。

## 何時使用

適合：

- 長時間重構。
- 跨檔案功能開發。
- 多輪除錯。
- 需要回溯多輪決策的研究。

不適合單獨承擔：

- 版本控制。
- 團隊永久記憶。
- 測試證據。
- 排程狀態或 Discord 發布 read-back。

## 共用帳本格式

帳本位置：

```text
agent_office/shared/context/<task-id>.md
```

至少記錄：

- 目標與驗收條件。
- 已驗證事實與來源。
- 架構決策。
- 嘗試與失敗原因。
- 風險、阻塞與下一步。

工具：

```text
agent_office/tools/context-ledger/context_ledger.py
```

完成前必須執行 `verify`，並留下實際測試結果；不可只寫「已完成」。帳本不得保存 token、密碼、API key 或未遮罩連線字串。

## 來源與限制

- 官方設定參考：`https://developers.openai.com/codex/config-reference`
- 本次任務帳本：`agent_office/shared/context/codex-context-management.md`
- 工具說明：`agent_office/tools/context-ledger/README.md`
- X 貼文僅作需求線索，不作官方能力證據。

## 相關頁面

- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
- [[concepts/workspace-architecture.md|Workspace 架構]]
