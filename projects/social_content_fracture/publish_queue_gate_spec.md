---
title: "多平台內容裂變之發布隊列 (Publish Queue) 與六道 Gate 驗收標準"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [content_fracture, publish_queue, quality_gate, approved_only, meta_graph_api, threads]
summary: "深入分析 content-os-20260723 實體發布隊列 publish_queue.json 之六道嚴格防護 Gate；確立 Approved-only 安全邊界，杜絕未經審核之跨平台草稿外洩或自動群發。"
status: active
source:
  - "artifacts/commercial-content-os-20260723/publish_queue.json"
  - "artifacts/workflow-sop-20260723/SOP-01-content-fracture.md"
  - "artifacts/meta-publish-readback/threads-native/COMFYUI-FRESHNESS-20260802-threads.json"
confidence: high
review_after: 2026-10-04
---

# 多平台發布隊列 (Publish Queue) 與六道 Gate 驗證 (t_f92fde19)

## 1. 核心政策：Approved-Only 發布隊列

依據實體檔案 `/mnt/d/Workspace/artifacts/commercial-content-os-20260723/publish_queue.json`：
- **發布政策**：`policy: "approved-only-with-policy-auto-approval"`
- **系統紅線**：預設永遠禁止全自動群發。所有由母內容（方格子長文、Podcast）裂變生成之各平台草稿（Threads、FB、X、YouTube、IG），必須通過嚴格檢驗進入隊列，未經人工或 Tech Lead 核准前，狀態一律鎖定為 `blocked`。

---

## 2. 六道強制防護 Gate (Required Gates)

隊列檢驗強制通過以下六道獨立閘門，任一項未通過即標記 `blocked_reasons` 並阻斷發布：

1. **`source_grounded_qa` (來源事實查證)**：草稿中所有論點、數據、引用必須具備明確一手來源檔案或公開 URL，禁止模型幻覺捏造。
2. **`sensitive_scan` (機密與隱私掃描)**：嚴禁包含內部路徑（`D:/Workspace/...`）、API Token、Cookie、個人機密或未公開內部計劃。
3. **`link_check` (外部連結可達性)**：草稿中所有引流連結必須經 HTTP 200 回讀驗證，杜絕 404 死鏈。
4. **`platform_policy_check` (平台政策規範)**：符合各平台字數限制、排版規範與防濫用條款。
5. **`maker_not_grader` (製作者不兼任驗收者)**：草稿產生者（Maker）不得自主標記通過，必須由獨立驗收者（Grader/Hermes）覆核。
6. **`rights_gate` (素材著作權門檻)**：引用的圖文、音訊素材必須確認原創性或合法商用授權。

---

## 3. 已驗證發布與 Read-back 回讀指標 (客觀事實數據)

- **回讀驗證標竿**：`artifacts/meta-publish-readback/threads-native/COMFYUI-FRESHNESS-20260802-threads.json`
- **關鍵驗證數據**：
  - 狀態：`published_verified`
  - 4 篇式 Thread 連鎖成功（母貼文 ID `18029519939843794`，回讀狀態 `pass`）。
  - 各篇間隔平滑發布（`05:18:27Z` 至 `05:22:33Z`），完全符合 Meta Graph API 頻率限制。
