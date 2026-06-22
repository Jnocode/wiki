---
title: "混合部署方案"
created: 2026-06-23
updated: 2026-06-23
type: entity
tags: [deploy, nas, docker]
wikilinks: [[[agent-office-shared]], [[hermes-agent]]]
---

# WSL/Windows 混合部署

來源: `System/Hybrid-Deployment-Progress.md`

## 方案: 混合部署 (2026-02-14)

將 OpenClaw 技能拆為 WSL 端與 Windows 端。

### 已完成

**WSL 端清理:**
- 移除 `codex-cli` (109 packages)、`pi-coding-agent` (270 packages)
- 移除不適用技能: `model-usage`
- 遷移至 Windows 的技能: coding-agent, notion, trello, openai-image-gen, summarize, nano-pdf, gifgrep, blogwatcher, goplaces, local-places

**WSL 端最終技能:** (6個)
- gemini, github, healthcheck, session-logs, tmux, video-frames

### 待完成

- 驗證 Windows 端 Pi 版本
- 驗證 WSL 端 ffmpeg
- 配置 API Keys (Notion, Trello, OpenAI)
- 更新 MEMORY.md
- 建立最終配置文檔

## WSL 安裝進度

Windows→WSL 環境遷移與技能分佈的最終測試報告。


## 關聯頁面
- [[agent-office-shared]]
- [[hermes-agent]]
