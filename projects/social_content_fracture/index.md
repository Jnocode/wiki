---
title: "多平台內容裂變與受保護社群引流發布管線架構"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [content_fracture, threads, meta_graph_api, vocus, discord, social_media, automation]
summary: "落實「方格子長文正本→Discord 留存→社群引流」全管線 SOP-01，修復 Threads 長效 Token 驗證，建立 Approved-only 受保護發布隊列與 Read-back 回讀驗收機制。"
status: active
source:
  - "artifacts/workflow-sop-20260723/SOP-01-content-fracture.md"
  - "artifacts/meta-auth-audit-20260719/threads_token_generator_setup.json"
  - "artifacts/meta-publish-readback/threads-native/COMFYUI-FRESHNESS-20260802-threads.json"
confidence: high
review_after: 2026-10-03
---

# 多平台內容裂變與社群發布管線架構 (t_f92fde19)

## 1. 內容裂變核心流向 (SOP-01 規約)

全案遵循嚴格的三級傳播架構：
$$\text{方格子 (vocus) 長文正本} \longrightarrow \text{Discord 社群留存/深度討論} \longrightarrow \text{社群平台原生引流 (Threads / FB / X)}$$

### 跨平台原生改寫原則
- **方格子 (vocus)**：正本母內容，詳盡技術脈絡、架構圖解與完整論據。
- **Discord**：核心社群留存，提供技術同儕交流、除錯支援與討論入口。
- **Threads**：短觀點、痛點直擊、互動提問，引導至留言區或首篇串文連結。
- **Facebook**：長摘要、商業/實務痛點分析、社群引流討論。
- **X (Twitter)**：精簡結論 Thread，強調關鍵技術亮點。

---

## 2. Threads Token 與 Meta Graph API 憑證生命週期

依據 `artifacts/meta-auth-audit-20260719/` 審計數據：
1. **Token 驗證狀態**：
   - 帳號識別：`username_readback: "codegaps"`。
   - 身份核對：`identity_http_status: 200`，`identity_id_matches_user_id: true`。
   - 長效 Token 機制：經由官方 Exchange 取得 60 天 Long-Lived User Token，並安全沉澱於系統環境變數註冊表中，日誌中標註 `never_logged`，杜絕明文外洩。
2. **安全發布隊列 (Approved-Only Queue)**：
   - 系統預設**絕對禁止全自動群發**。
   - 流程必須通過機械 Gate（無內部憑證、無內部路徑、外部連結 HTTP 200 驗證、無違規灌水）。
   - 只有經過人工/Orchestrator 終審標記為 `approved` 的單篇內容，發布器方可自隊列取件執行。

---

## 3. 已驗證之原生發布與 Read-back 回讀指標 (客觀數據依據)

查核 `COMFYUI-FRESHNESS-20260802-threads.json` 真實發布紀錄：
- **發布狀態**：`published_verified`
- **串文結構**：4 篇式原生 Thread 連鎖發布（1 篇母貼文 + 3 篇接續回覆）。
- **真實公開 Post ID 與回讀驗證**：
  1. Post 1 (母貼文)：ID `18029519939843794`，Permalink: `https://www.threads.com/@codegaps/post/DbhpVAok2wg`，Readback: `pass`
  2. Post 2 (回覆 1)：ID `17950073370233980`，Permalink: `https://www.threads.com/@codegaps/post/DbhpV8Rkya4`，Readback: `pass`
  3. Post 3 (回覆 2)：ID `17962302273139599`，Permalink: `https://www.threads.com/@codegaps/post/DbhpXKmkzI4`，Readback: `pass`
  4. Post 4 (回覆 3)：ID `18100570547612615`，Permalink: `https://www.threads.com/@codegaps/post/Dbhpy_1EwDi`，Readback: `pass`
- **發布時戳**：`2026-08-02T05:18:27Z` 至 `2026-08-02T05:22:33Z`，間隔平滑無觸發頻率限制。
