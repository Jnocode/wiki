---
title: "Discord AI 日報卡片與安全發布"
type: concept
date: 2026-09-08
updated: 2026-09-09
tags: [Discord, AI 日報, OpenClaw, 發布, QA]
summary: "定義 Discord AI 日報的資料誠信、卡片版型、錯誤隔離與發布 read-back 規則。"
source: ["agent_office/shared/brain/04_media/discord-ai-digest-presentation.md"]
confidence: high
review_after: 2026-10-09
status: active
---
# Discord AI 日報卡片與安全發布

## 對外原則

- 事實、AI 分析、來源連結分開呈現。
- 未查證內容不得包裝成已驗證新聞。
- 對外只顯示可讀卡片；stdout、stderr、traceback、連線錯誤留在後台。
- 執行失敗就停止發布，不用漂亮格式掩蓋失敗。
- 發布後必須讀回目標訊息或取得可驗證 message ID。

## 卡片規格

目前卡片 renderer 位於任務 artifact：

```text
D:/Workspace/artifacts/discord-digest-cards/release/card_pipeline.py
```

採 OpenClaw Message Presentation／Components Containers，不使用 raw Embed。renderer 至少要驗證：

- 每次最多三則。
- source URL 必須是完整 HTTPS URL。
- 禁止 userinfo、query、fragment、控制字元與 mention。
- 總長限制與 Markdown URL 不可被任意截斷。
- 欄位不合法時 fail closed。

手機版版型要求：

- 單欄。
- 深色 Discord 類背景。
- 青藍左側細線。
- 每則一個清楚標題、事實區、分析區與來源。
- 真測 `390x844` 與 `1280x900`，確認 `scrollWidth <= innerWidth`。

## 排程安全狀態

舊版裸發 stdout／stderr 的路徑已停止對外 delivery；正式重新啟用前，必須完成 renderer 接線、dry-run、端到端發布與外部 read-back。`delivery.mode=none` 是止血狀態，不是成功發布。

## 驗收證據

- `D:/Workspace/artifacts/discord-digest-cards/release/test_card_pipeline.py`
- `D:/Workspace/artifacts/discord-digest-cards/release/RESULT.md`
- `D:/Workspace/artifacts/discord-digest-cards/visual-preview/verify.json`
- 官方文件：`https://docs.openclaw.ai/plugins/message-presentation`
- Discord API 文件：`https://discord.com/developers/docs/resources/message`

## 相關頁面

- [[concepts/data-source-integrity-and-fallback.md|資料來源完整性]]
- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
