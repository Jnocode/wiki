---
title: "WSL Windows 與 Codex 現行環境圖"
type: concept
date: 2026-09-08
updated: 2026-09-08
tags: [Windows, WSL, Codex, Runtime, 環境]
summary: "記錄目前可驗證的 Windows、Workspace、Codex 與 OpenClaw 邊界；不把歷史配置當現行路徑。"
source: ["agent_office/shared/brain/90_system/runtime-environment-map.md"]
confidence: high
review_after: 2026-10-08
status: active
---
# WSL Windows 與 Codex 現行環境圖

## 已確認環境

- 主機：Windows 11。
- 工作區：`D:/Workspace`。
- 團隊共用 brain 正本候選：`D:/Workspace/03_Dev_Projects/agent_office/shared/brain/`。
- 任務上下文：`D:/Workspace/03_Dev_Projects/agent_office/shared/context/`。
- Codex 使用者設定：`C:/Users/Jun/.codex/config.toml`。
- Codex CLI：`0.153.4`。
- Codex 執行檔存在於 `C:/Users/Jun/AppData/Local/OpenAI/Codex/bin`，但目前未擅自修改系統 PATH。

## Codex 設定

目前啟用：

```toml
[features.context_management]
experimental_mode = true
```

設定檔修改前已有備份；秘密值與完整設定內容不複製到 Wiki。

## 路徑規則

- Windows 原生工具使用 `C:/...` 或 `D:/...` 路徑。
- Hermes terminal 在 Windows 上使用 POSIX shell 語法；不要把 PowerShell cmdlet 當成 bash 指令。
- 長期工作產物寫入 `D:/Workspace/artifacts/<task-name>/`。
- shared brain 只保存 Markdown 知識與索引，不放二進位檔。
- 常駐服務不得使用 Hermes 應用 venv；需使用服務自己的 runtime。

## GitHub Pages 發布鏈

- Canonical source：`D:/Workspace/03_Dev_Projects/agent_office/shared/brain/`。
- GitHub Pages repo：`D:/Workspace/03_Dev_Projects/wiki/`，遠端 `Jnocode/wiki`。
- 小克 OpenClaw cron：`xiaoke-wiki-github-pages-publish`。
- Job ID：`908219e2-4a15-468e-b080-643ab52f5ef6`。
- 排程：每日 02:15，時區 `Asia/Taipei`。
- 執行器：`publish_shared_brain_to_github.py`，只同步限定 Wiki projection，push 後做公開 URL read-back。
- `delivery.mode=none`：這是背景同步，不應把 Git 輸出刷到 Discord。

## 未完成事項

- `D:/Workspace/agent_office` 與 `D:/Workspace/03_Dev_Projects/agent_office` 的引用、排程與服務依賴仍需完整盤點。
- 在正本判定完成前，不搬移、不刪除、不改服務啟動路徑。
- 任何 runtime 路徑變更都要先備份並執行 smoke test。

## 舊頁處理

`90_system/WSL-Windows-Skill-Distribution-FINAL.md` 是歷史資料／待複核頁，不是目前配置正本。

## 相關頁面

- [[concepts/workspace-architecture.md|Workspace 架構]]
- [[concepts/codex-context-management.md|Codex 上下文管理]]
