---
title: "Hot Cache — 近 7 天動態焦點"
type: log
date: 2026-09-09
updated: 2026-09-09
tags: [hot, summary, digest]
summary: "依 Wiki 條目 frontmatter 編譯近 7 天活躍條目，共 12 項。"
status: active
---

# 🔥 Hot Cache — 近 7 天動態焦點

> 由 `compile_hot_cache.py` 根據 Wiki repo 內各條目的 `updated/date` deterministic 編譯；沒有日期的條目不納入，不以檔案時間猜測更新。

## 近期活躍焦點 (Active Threads)

- 2026-09-09 — [Workspace 工作區架構與整理規則](concepts/workspace-architecture.md)
- 2026-09-09 — [WSL Windows 與 Codex 現行環境圖](concepts/runtime-environment-map.md)
- 2026-09-09 — [Public APIs 免費 API 資源庫 — 資料源目錄索引](concepts/public_apis_free_data_source_index.md)
- 2026-09-09 — [Podcast 現行產線契約](concepts/podcast-current-production-contract.md)
- 2026-09-09 — [Discord AI 日報卡片與安全發布](concepts/discord-ai-digest-presentation.md)
- 2026-09-09 — [資料來源完整性與 Provider 備援](concepts/data-source-integrity-and-fallback.md)
- 2026-09-09 — [Codex 上下文管理與跨 Agent 帳本](concepts/codex-context-management.md)
- 2026-09-09 — [Agent 團隊協作契約](concepts/agent-collaboration-contract.md)
- 2026-09-04 — [Wiki 知識庫 NAS 與本地雙向同步與索引治理專案報告](projects/wiki_governance/index.md)
- 2026-09-04 — [Wiki Giscus 評論系統整合與倉庫層設定踩坑記](projects/wiki_governance/giscus_discussions_integration.md)
- 2026-09-04 — [Spirits-Calling 玩家向垂直切片 Playtest 實機指引與驗收標準](projects/spirits_calling/playtest_guide.md)
- 2026-09-04 — [多平台內容裂變之發布隊列 (Publish Queue) 與六道 Gate 驗收標準](projects/social_content_fracture/publish_queue_gate_spec.md)

## 條目摘要 (Verified Metadata)

- **Workspace 工作區架構與整理規則**：定義 D:\\Workspace 的資料邊界、正本判定、搬移驗證與 artifacts 生命週期。（2026-09-09）
- **WSL Windows 與 Codex 現行環境圖**：記錄目前可驗證的 Windows、Workspace、Codex 與 OpenClaw 邊界；不把歷史配置當現行路徑。（2026-09-09）
- **Public APIs 免費 API 資源庫 — 資料源目錄索引**：GitHub public-apis/public-apis 免費 API 目錄；工具缺外部資料源時先查分類與官方文件，再決定是否接入。（2026-09-09）
- **Podcast 現行產線契約**：定義目前三人主持、音訊製作、品質閘門與 SoundOn 發布的現行規則。（2026-09-09）
- **Discord AI 日報卡片與安全發布**：定義 Discord AI 日報的資料誠信、卡片版型、錯誤隔離與發布 read-back 規則。（2026-09-09）
- **資料來源完整性與 Provider 備援**：統一即時資料查證、API 失敗處理、Quota Pool 熔斷與未驗證資訊標示規則。（2026-09-09）
- **Codex 上下文管理與跨 Agent 帳本**：將 Codex 的長工作階段上下文與團隊共用 Markdown 任務帳本分層，避免把模型歷史誤當成驗收證據。（2026-09-09）
- **Agent 團隊協作契約**：定義小衡、小克與 Codex 的分工、交接、驗收與對外發布邊界。（2026-09-09）
- **Wiki 知識庫 NAS 與本地雙向同步與索引治理專案報告**：完成 agent_office/shared/brain 知識庫 60 篇 Markdown 格式全面修復，達成 100% SCHEMA.md 合規率；驗證 wiki_sync.py 雙向同步通道與 VitePress 索引建置標準。（2026-09-04）
- **Wiki Giscus 評論系統整合與倉庫層設定踩坑記**：記錄 Wiki 導入 Giscus 評論系統時遇到的排序與設定權限問題，確立 giscus.json 為倉庫級正本的除錯結論。（2026-09-04）
- **Spirits-Calling 玩家向垂直切片 Playtest 實機指引與驗收標準**：提供專案負責人 Jun 之真人 Playtest 實機操作指南：一鍵啟動腳本 playtest_p10_vertical_slice.bat、3–5 分鐘六大核心節奏反饋矩陣與驗收指標。（2026-09-04）
- **多平台內容裂變之發布隊列 (Publish Queue) 與六道 Gate 驗收標準**：深入分析 content-os-20260723 實體發布隊列 publish_queue.json 之六道嚴格防護 Gate；確立 Approved-only 安全邊界，杜絕未經審核之跨平台草稿外洩或自動群發。（2026-09-04）
