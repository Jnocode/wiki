---
title: "Wiki 雙軌同步架構：GitHub Pages 與 Synology NAS 離線同步"
type: "concept"
date: "2026-09-13"
updated: "2026-09-13"
tags: ["wiki", "nas", "synology", "sync", "meilisearch"]
summary: "落實本地 Markdown 知識庫、Synology NAS (PostgreSQL + Meilisearch) 與 GitHub Pages 之三向同步與健康監控。"
status: "active"
---

# Wiki 雙軌同步架構：GitHub Pages 與 Synology NAS 離線同步

> 紀錄日期：2026-09-13  
> 核心主題：全域知識資產備份、NAS 向量搜尋與外部門戶同步  

## 1. 核心架構
- **SSH Pipeline 傳輸**：透過本地綁定網卡向 Synology NAS (192.168.1.107) 即時同步 100+ 條目與索引。
- **外部唯讀鏡像**：自動編譯首頁、熱點快取與閱讀器推送至 GitHub Pages，確保無 VPN 狀態下手機亦可即時讀取。