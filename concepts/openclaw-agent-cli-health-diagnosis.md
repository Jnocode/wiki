---
title: "OpenClaw 雙 Agent CLI 調度器排查與排程健康診斷"
type: "concept"
date: "2026-09-15"
updated: "2026-09-15"
tags: ["openclaw", "cli", "dispatcher", "healthcheck", "agent"]
summary: "記錄 2026-09-15 診斷後台 CLI 調度器、小克 Discord 響應鏈路與 Cron 故障排查。"
status: "active"
---

# OpenClaw 雙 Agent CLI 調度器排查與排程健康診斷

> 紀錄日期：2026-09-15  
> 核心主題：Agent 後台常駐程序健康狀態與調度鏈路排查  

## 1. 核心排查結論

- **CLI 檢測健康狀態**：
  - 排查後台 `agent_health.db` 與調度器 watchdog 報警機制。
  - 診斷 OpenClaw Gateway 與 WSL2 連線通道，確認小克在 Discord 與 Workboard 上的即時響應心跳。
- **排程修復與邊界防禦**：
  - 針對盤後交易排程連線異常進行初步診斷。
  - 確立「調度器必須具備自癒與死鎖檢測，不可因單一卡片未結案而阻塞整條流水線」。
