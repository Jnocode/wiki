---
title: Hermes Agent
created: 2026-06-20
updated: 2026-06-20
type: entity
tags: [hermes, agent, llm]
sources: []
confidence: high
---

# Hermes Agent

由 [[Nous Research]] 開發的自主 AI Agent 框架，本地部署、多工具支援。

## 核心特性
- **多模型支援**: DeepSeek V4、Qwen3.6、Anthropic Claude 等
- **工具系統**: web_search、terminal、file I/O、Discord/Telegram bridge
- **記憶系統**: Honcho（長期記憶）+ 本機 session DB
- **多 Agent**: delegate_task 可 spawn 子代理平行工作
- **Cron 排程**: 排程任務自動執行
- **Plugin 系統**: MCP、自訂技能

## 部署環境
- **主機**: Windows 10（git-bash MSYS）
- **路徑**: `~/.hermes/`
- **設定檔**: `~/.hermes/hermes-agent/config.yaml`

## 相關頁面
- [[Honcho]] — 記憶系統
- [[OpenClaw]] — 前代框架
- [[JoJo Trading]] — 量化交易專案

## 備註
2026-06-20：已上線 cron job「每日郵件掃描」，Gmail + Outlook 自動摘要分類。
