---
title: "EP5 筆記：AI 開發工具的真實面貌"
type: project
date: 2026-07-07
updated: 2026-07-07
tags: [podcast, code_gaps, ep5, ai_tools, moe]
summary: "EP5 完稿筆記：NAS 部署翻車實錄、MoE 的 VRAM 迷思（省會議費不省住宿費）、模型命名混亂自保守則。"
aliases: ["EP5", "ep5"]
source:
  - "raw/2026/2026-07-07_ep5_ai_dev_tools_script.md"
confidence: high
review_after: 2026-10-07
status: active
---

# EP5：AI 開發工具的真實面貌

> 原文逐字稿：`raw/2026/2026-07-07_ep5_ai_dev_tools_script.md`
> （原稿在 `agent_office/temp/EP5/part1-4.md`，歸檔時合併為單檔）。
> 集數狀態正本在 `business.db` 的 `podcast_episodes`（ep_no=5）。

## 稿件結構

INTRO → 上半部（NAS/Docker 部署翻車雜談）→ 下半部（MoE VRAM 迷思、模型命名混亂）→ 收尾守則。

## 核心內容（蒸餾）

1. **翻車實錄**：在 Synology NAS 用 Container Manager 部署資料庫給 AI 記憶系統用，
   「一小時搞定」變兩個晚上——綠燈 ≠ 能用（「工程師最不該相信的東西第一名」）。
2. **MoE VRAM 迷思**：MoE 每次只啟用少數專家（如 35B-A3B 只算 3B），省的是**計算**
   （會議費），不省 **VRAM**（住宿費）——一百個顧問的飯店錢照付。
3. **命名地獄**：dense 32B 與 MoE 30B-A3B 是兩種生物；Base/Instruct/Thinking 後綴
   （生肉/熟肉）；量化後綴 Q4_K_M/Q8_0 與 GGUF/AWQ/GPTQ 封裝格式。
4. **AI 也會編模型名**：模型名稱/參數量/發布日是幻覺重災區——越具體越自信的即時資訊越要查證。
5. **自保守則**：模型全名複製貼上不憑記憶打；下載前對齊系列/大小/架構/版本/量化/格式六個選擇題。

## 相關頁

- [[projects/podcast/index|Podcast MOC]]
- [[projects/podcast/ep04_notes|EP4：AI 的記憶系統]]
