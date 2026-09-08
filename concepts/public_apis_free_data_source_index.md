---
title: "Public APIs 免費 API 資源庫 — 資料源目錄索引"
type: concept
date: 2026-09-08
updated: 2026-09-09
tags: [api, resource_index, github, data_source, development]
summary: "GitHub public-apis/public-apis 免費 API 目錄；工具缺外部資料源時先查分類與官方文件，再決定是否接入。"
source: ["agent_office/shared/brain/01_tech/public_apis_free_data_source_index.md"]
confidence: high
review_after: 2026-10-09
status: active
---
# Public APIs 免費 API 資源庫 — 資料源目錄索引

## 1. 定位

`public-apis/public-apis` 是 GitHub 社群整理的公開 API 目錄，集中列出不同領域的資料服務、驗證需求、HTTPS 與 CORS 狀態。它是**資料源索引**，不是任何 API 的服務等級或穩定性保證。

## 2. 外部數據驗證

以下數據由 GitHub API 一手端點於 **2026-09-08 18:10:19（台北時間）**查詢：

來源：`https://api.github.com/repos/public-apis/public-apis`

- Stars：**477,291**
- Forks：**52,676**
- Open issues：**1,904**
- 授權：**MIT License**
- 專案狀態：**未封存**
- 最後 push：**2026-09-05 21:46:01 UTC**

數字會變動；再次引用時必須重新查詢 GitHub API，不能把本頁數字當成即時值。

## 3. 對我們的實用價值

- **求職作品集與 AI demo：高**
  - 可快速尋找 Weather、News、Images、Geography、Games 等原型資料源。
  - 適合展示外部 API 串接、錯誤處理、快取與 fallback，不等於可直接用於正式商業服務。
- **量化備援：中**
  - Finance、Cryptocurrency、Exchange Rates 可作海外或概念驗證備援。
  - 台股正式數據仍以 TWSE 等權威來源為主，不能以本目錄取代。
- **Podcast 素材：低至中**
  - News、Music、Audio 可作素材探索入口；正式內容仍需多源查證與版權確認。
- **自動化補充：中**
  - Development、Open Data 類別可協助尋找小型工具 API，但必須先做文件、限制與可用性預檢。

## 4. 接入前門禁

1. 先從目錄取得候選 API，再開啟該 API 的**官方文件**確認端點、授權、價格與服務限制。
2. 驗證 rate limit、配額、CORS、HTTPS、資料更新頻率與服務可用性。
3. 不把「免費」解讀為無限流量，也不把目錄中的描述解讀為官方承諾。
4. API key 只能走受保護的環境變數或本機秘密管理，不得寫入 Wiki、程式碼、commit 或排程 payload。
5. 正式流程要有 timeout、重試上限、快取、來源標記與失敗時的明確 `DATA_UNAVAILABLE`。

## 5. 使用路徑

- 目錄：<https://github.com/public-apis/public-apis>
- 操作順序：分類搜尋 → 閱讀條目 → 開官方文件 → 小型 smoke test → 再接入正式流程。

## 相關頁面

- [[concepts/data-source-integrity-and-fallback.md|資料來源完整性]]
- [[concepts/workspace-architecture.md|Workspace 架構]]
