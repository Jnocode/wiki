---
title: "MoneyPrinterTurbo 本地化模型配置與短影音渲染除錯"
type: "concept"
date: "2026-09-14"
updated: "2026-09-14"
tags: ["video", "moneyprinterturbo", "mv", "automation", "rendering"]
summary: "記錄 2026-09-14 於本機配置 MoneyPrinterTurbo 本地模型、歌詞畫面修正與 render_mv.sh 執行流程踩坑。"
status: "active"
---

# MoneyPrinterTurbo 本地化模型配置與短影音渲染除錯

> 紀錄日期：2026-09-14  
> 核心主題：短影音自動化管線本地化部署與渲染修復  

## 1. 核心工作與踩坑復盤

- **本地模型配置**：
  - 配置 MoneyPrinterTurbo 接入本地 LLM 與語音/字幕模型，減少外部雲端依賴。
  - 調整 `render_mv.sh` 與 `anxi_mv_project` 的歌詞畫面與 UI 替換範圍。
- **渲染與效能驗證**：
  - 驗證本機 RTX 4070 12GB 在跑影音合成與字幕對齊時的負載與記憶體邊界。
  - 確立「本機不跑重型多鏡頭影片渲染，長片與複雜動態改走雲端/混合架構」之原則。
