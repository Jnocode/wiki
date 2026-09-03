---
title: "求職 Job Search"
type: project
date: 2026-07-07
updated: 2026-07-07
tags: [job_search, career]
summary: "Jun 的求職專案 MOC：申請狀態正本在 business.db 的 job_applications；此頁只放敘事與導覽。"
aliases: ["求職", "job search", "找工作"]
source:
  - "D:/Workspace/artifacts/maigent-ai-exam-answers.md"
confidence: high
review_after: 2026-08-07
status: active
---

# 求職 Job Search

## 原則

- 申請狀態（status / next_action / 日期）正本在 `business.db` 的
  `job_applications` 表；本頁不寫「大概投了幾家」這種散文狀態。
- 每筆入庫申請必須附 `source_url` 或可回溯的檔案佐證；
  無來源的記憶性資料一律不入庫（見 [[SCHEMA.md|SCHEMA]] 禁止事項 2）。

## 申請狀態（正本在 business.db，以下為唯讀渲染）

<!-- db:begin table=job_applications -->
> 唯讀渲染區塊（表 `job_applications`，共 1 列）：狀態正本在 `shared/db/business.db`；手改此區塊會被 business_sync.py 偵測為 drift 並以 DB 覆蓋。

| company | role | status | applied_at | next_action | source_url |
|---|---|---|---|---|---|
| MaiAgent | AI Agent 工程師 (AI Agent Engineer) | applied | 2026-07-04 | 等待考題審核結果 | D:/Workspace/artifacts/maigent-ai-exam-answers.md |
<!-- db:end -->

> 目前僅 1 筆有實體佐證的申請。其他口頭提過但無檔案/連結佐證的投遞
> **未入庫**（誠信原則：寧缺勿假）。找到佐證後再補列。

## 公司筆記

- [[projects/job_search/company_maigent_notes|MaiAgent 應徵筆記]]

## 相關

- 面試準備素材可引用 [[projects/podcast/ep04_notes|EP4 記憶系統]] 的實作經驗。
