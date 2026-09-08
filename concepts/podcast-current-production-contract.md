---
title: "Podcast 現行產線契約"
type: concept
date: 2026-09-08
updated: 2026-09-09
tags: [Podcast, 音訊, QA, 發布, 產線]
summary: "定義目前三人主持、音訊製作、品質閘門與 SoundOn 發布的現行規則。"
source: ["agent_office/shared/brain/04_media/podcast-current-production-contract.md"]
confidence: high
review_after: 2026-10-09
status: active
---
# Podcast 現行產線契約

> 本頁取代分散在舊腳本與舊主持配置中的現行規則；舊頁保留作歷史資料。

## 主持配置

- **S1 小克**：實作與資料採集視角。
- **S2 小衡**：架構、驗收與決策視角。
- **S3 傑諾**：短句、節奏與人類經驗視角。

三人不是三個重複播報器；內容要靠立場衝突產生資訊密度，禁止公關稿腔與硬笑。

## 產線閘門

1. 先確認來源與資料新穎度，再寫腳本。
2. 專名採「中文＋英文」雙軌，避免聽眾失去定位。
3. 新主持前 30 秒補足認知斷層。
4. SoulX 不得直接進入台詞；多音字與專名先做發音 QA。
5. 追加內容採疊加加長，不覆蓋既有成品。
6. 音訊拼接前對 wav 做 shape／sample rate 檢查，必要時 `squeeze(0)` 後再沿時間維度串接。
7. 成品需檢查音量目標約 `-16 ± 1 LUFS`、破音、截斷、空白段與主持身份。
8. Maker 產出後由獨立 Reviewer 驗收；不能由同一流程自我宣告通過。

## 發布

Podcast 正式流程集中於指定 Discord podcast thread；Cron deliver 不得跨 thread。SoundOn 或其他外部平台發布後必須 read-back，取得可驗證 URL 或平台狀態才算完成。

## 參考實作

- `agent_office/scripts/content_os_scripts/podcast_show_contract.py`
- `agent_office/scripts/content_os_scripts/`
- Podcast QA thread：由當前任務路由表維護，不在本頁硬編碼短期訊息 ID。

## 相關頁面

- [[concepts/agent-collaboration-contract.md|Agent 協作契約]]
- [[concepts/data-source-integrity-and-fallback.md|資料來源完整性]]
