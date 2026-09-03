---
title: "Jun（姜鈞）— 使用者 Persona 正本"
type: entity
date: 2026-07-07
updated: 2026-07-07
tags: [user, persona, jun]
summary: "使用者 Jun 的身份、環境與工作偏好正本；persona_writer.py（P2）唯一寫入目標。"
aliases: ["Jun", "姜鈞", "傑諾", "jnoworldline"]
source:
  - "C:/Users/Jun/.claude/CLAUDE.md"
  - "D:/Workspace/.antigravity/rules.md"
  - "D:/Workspace/artifacts/maigent-ai-exam-answers.md"
confidence: high
review_after: 2026-10-07
status: active
---

# Jun（姜鈞）

## 身份

- 本名姜鈞，email：jnoworldline@gmail.com（來源：CLAUDE.md 環境設定、MaiAgent 作答卷）。
- AI Agent & RAG 開發工程師（見 [[projects/job_search/index|求職]]）。
- Podcast「代碼縫隙 Code Gaps」中以人類主持人「傑諾」身分出現（見 [[projects/podcast/index|Podcast]]）。

## 核心研發專案

- **Recall — 長期語意記憶與混合檢索引擎 (open-source)**：實現 ANN 向量、FTS5 全文檢索與 SQLite 索引的三路 RRF 混合檢索，無 LLM 下查詢延遲 < 80ms。開發 `recall-vault` 品質閘門。
- **Hermes Agent 多角色協作自動化產線 (self-hosted)**：基於 Windows Git-Bash / cron 建立背景 queue-based 產線。整合本地 faster-whisper 音訊轉譯、SoVITS 語音合成、自動混音與 SoundOn 排程發布。
- **JoJo Trading Platform (量化交易系統)**：基於 AsyncIO 的多模組量化交易回測與自動下單系統。

## 環境

- 主力機：Windows 11，工作區 `D:\\Workspace`；Python 3.11 + uv；GPU RTX 4070 12GB。
- 本機磁碟：C（系統）、D（Workspace）、E（遊戲）、F（備份）；NAS：Y（影音）、Z（ai-hub）。
- 自架 Hermes Agent，長期記憶用 recall-memory-hermes plugin（唯一 provider）。

## 工作偏好（AI 應對規則）

- 回覆一律繁體中文；程式碼與術語保留原文並附中文註解。
- 數據來源誠信是最高原則：多源比對、標來源、沒有就說不知道。
- 「直接做，不問」：有下一步就行動，真的卡死才問。
- 檔案寫入後必須 read-back 驗證；不奉承（NO SYCOPHANCY）。

> [!memory] type=preference subject=jun confidence=0.95 topic=reply_language
> Jun 的回覆一律使用繁體中文；程式碼與技術術語保留原文，可附中文註解。

> [!memory] type=preference subject=jun confidence=0.9 topic=data_integrity
> Jun 要求數據來源誠信：重要事實須標來源與時間、多源交叉比對；沒有可靠來源就直說不知道，不得編造。

> [!memory] type=preference subject=jun confidence=0.85 topic=work_style
> Jun 偏好「直接做，不問」：有明確下一步就行動，卡住先查文件，真的卡死才問使用者。

## 相關頁

- [[projects/hermes_development/index|Hermes 開發]]
