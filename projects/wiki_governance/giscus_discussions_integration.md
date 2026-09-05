---
title: "Wiki Giscus 評論系統整合與倉庫層設定踩坑記"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [wiki, giscus, github_discussions, architecture, frontend]
summary: "記錄 Wiki 導入 Giscus 評論系統時遇到的排序與設定權限問題，確立 giscus.json 為倉庫級正本的除錯結論。"
status: active
source:
  - "03_Dev_Projects/wiki/giscus.json"
  - "03_Dev_Projects/wiki/index.html"
confidence: high
review_after: 2026-12-04
---

# Wiki Giscus 評論系統整合與倉庫層設定踩坑記

## 1. 需求與架構
Wiki 系統需要一個完全無伺服器、無額外資料庫、且具備真實社群互動的評論系統。我們選用以 GitHub Discussions 為後端的 Giscus：
- **訪客視角**：直接以 GitHub 帳號留言、按 Emoji 反應、參與討論。
- **後台視角**：所有數據皆為 GitHub Discussions 上的原生 Markdown，零資料庫維護成本。

## 2. 踩坑復盤：為什麼前端設定無法改變預設排序？
### 症狀
使用者要求將留言列表從預設的「最舊」改為「最新」，我們在前端嘗試加入 `data-sort="newest"`、調整 `data-input-position="top"`，但頁面重新整理後依然維持最舊在最上。

### 根因深入 (Systematic Debugging)
透過查閱 Giscus 官方開源原始碼（`Giscus.tsx`、`getConfig.ts`）：
- Giscus 的留言排序預設值**並不在前端 `<script>` 標籤中讀取**。
- Giscus 在載入時，會向目標 GitHub 倉庫根目錄請求 `giscus.json`。
- 若倉庫未提供 `giscus.json`，系統寫死預設值為 `defaultCommentOrder: "oldest"`。

### 解決方案
在 `Jnocode/wiki` 倉庫根目錄正式建立 `giscus.json`：
```json
{
  "defaultCommentOrder": "newest"
}
```
建立並推送到 GitHub 後，官方 API 立即回傳 `defaultCommentOrder: "newest"`，首頁社群討論即時恢復預期排序。
