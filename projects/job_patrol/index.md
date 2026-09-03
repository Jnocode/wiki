---
title: "多平台求職巡邏爬蟲與三維分類管線架構 (Job Patrol v2)"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [job_patrol, web_scraping, 104, cakeresume, career_ops, automation]
summary: "實作 JOB_PATROL_SPEC_V2 規範：建立 104 與 CakeResume 自動化爬蟲腳本，輸出 daily_top10 JSON 檔案，嚴格達成全職(4)、遠端(3)、接案(3) 三維分類配比與去重機制。"
status: active
source:
  - "agent_office/shared/JOB_PATROL_SPEC_V2.md"
  - "agent_office/tools/job-patrol/job_patrol_crawler.py"
  - "02_Job_Search/daily_top10_20260903.json"
confidence: high
review_after: 2026-10-03
---

# 求職串多平台自動化巡邏與分類管線 (t_38fbfa76)

## 1. 核心規格與分工對齊 (JOB_PATROL_SPEC_V2)

全案落實「小克負責資料抓取清洗、小衡負責驗收與 Discord 推播」之工程協作標準：
- **爬蟲腳本**：`/mnt/d/Workspace/agent_office/tools/job-patrol/job_patrol_crawler.py`
- **歷史去重**：維護 `/mnt/d/Workspace/02_Job_Search/seen_jobs.json`，防止重複推薦。
- **三維分類配比指標**：每日產出嚴格鎖定 **10 檔精選職缺**：
  - 🏢 **【全職 Full-Time】**：4 檔
  - 🌐 **【遠端 Remote】**：3 檔
  - 💼 **【接案 / 顧問 Contract】**：3 檔

---

## 2. 實作驗證數據與產出物指標 (客觀事實依據)

1. **腳本執行驗證**：
   - 指令：`python3 /mnt/d/Workspace/agent_office/tools/job-patrol/job_patrol_crawler.py`
   - **退出碼 (Exit Code)**：`0`
   - 抓取結果：跨平台候選池共採集 **63 筆** 原始職缺。

2. **產出交付物指標**：
   - 交付路徑：`/mnt/d/Workspace/02_Job_Search/daily_top10_20260903.json`
   - 總計選取數量：**10 筆**（`total_selected: 10`）
   - 配比達成率：`target_quota_met: true`
     - 全職（Full-Time）：**4 檔**（包含陳立教育 AI Application & Agent Engineer、宏羚 AI Agent Presale 等）
     - 遠端（Remote）：**3 檔**（包含樂透旅行社 AI Agent 流程優化、視宇跨境電商等）
     - 接案/顧問（Contract）：**3 檔**（包含鼎新數智 Agent Space 售前顧問、龍星企業 Agent Skill 用戶共創顧問、碩益科技 AI 流程與測試自動化顧問）
