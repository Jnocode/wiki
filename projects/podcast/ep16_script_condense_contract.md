---
title: "Podcast EP16 腳本去蕪存菁與長度合約壓縮 (18k -> 6.2k字)"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [podcast, ep16, length_remediation, audio_contract, script_assemble, qa_gate]
summary: "執行 EP16 腳本去蕪存菁與聽感合約壓縮；保留全部 45 項 Claims 與開場 Token，總字數由 18,080 字精確降至 6,211 字（預估聽感 19.2 分鐘，完美符合 5800~7200 字區間），QA 查核 100% PASS。"
status: active
source:
  - "artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/sections/"
  - "artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/script.json"
  - "artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/assembly_report.json"
confidence: high
review_after: 2026-10-04
---

# Podcast EP16 腳本去蕪存菁與長度合約壓縮驗收報告 (t_f9af51a4)

## 1. 任務背景與契約門檻 (Contract Thresholds)

- **原先狀態**：EP16 全 13 個 sections 總計高達 **18,080 字**（預估時長 55.8 分鐘），嚴重超出聽感契約（18~25 分鐘上限），導致生產線阻斷。
- **目標合約區間**：**5,800 ~ 7,200 字**（聽感時長約 18 ~ 22 分鐘，換算率 5.4 字/秒）。
- **非協商紅線 (Hard Gates)**：
  1. `c01 ~ c45` 全部 45 個 Claims 必須 100% 完整覆蓋，0 漏失。
  2. 首 8 turns 必須包含 `{{RECORDING_DATE_TAIPEI}}` 與 AI 主持人聲明。
  3. 0 正規化重複句、0 空段落、說話者嚴格交替。

---

## 2. 實機執行與數據指標對比 (Before vs After)

- **壓縮與組裝工具**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/precise_contract_condense.py`
- **QA 驗證工具**：`python3 _tools/qa_check.py`
- **驗證退出碼 (Exit Code)**：`0`

| 項目指標 | 壓縮前 (Original) | 壓縮後 (Condensed) | 合約規範標準 | 驗收狀態 |
|---|---|---|---|---|
| **總字數 (Characters)** | 18,080 字 | **6,211 字** | 5,800 ~ 7,200 字 | **PASS (完美命中區間)** |
| **預估聽感時長** | 55.8 分鐘 | **19.2 分鐘** | 18 ~ 22 分鐘 | **PASS** |
| **對白輪次 (Turns)** | 349 輪 | **119 輪** | - | **精煉流暢** |
| **Claims 覆蓋率** | 45 / 45 | **45 / 45 (100%)** | 45 / 45 (0 遺漏) | **PASS** |
| **開場錄音 Token** | 存在 (2 處) | **存在 (2 處)** | 必須存在 | **PASS** |
| **開場 AI 主持揭露** | 存在 | **存在** | 首 8 輪內必須宣告 | **PASS** |
| **重複句違規數** | 0 | **0** | 0 | **PASS** |
| **腳本 SHA256** | 5303806e84... | **e7a7ca3abca5...** | - | **已重新簽章** |

---

## 3. 產出物路徑與結構化資產

1. **Section JSONs**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/sections/*.json`（13 個檔案全數更新）
2. **總成對白腳本**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/script.json`
3. **Markdown 排版腳本**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/script.md`
4. **單元映射表**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/unit_map.json`
5. **組裝驗證報告**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/assembly_report.json`
6. **原始檔案備份**：`/mnt/d/Workspace/artifacts/podcast-slot-dispatcher/runs/EP16-2026-08-21/sections_original_backup_20260904/`

---

## 4. 下一步計畫 (待 Hermes 驗收與進入 TTS 渲染)

1. **提交 Hermes 獨立驗收**：待 Tech Lead / Grader 針對 `assembly_report.json` 與 QA 輸出進行 Read-back 查核。
2. **推進音訊渲染**：驗收通過後，解除 EP16 阻斷狀態，正式啟動 TTS 批量語音合成與混音產線。
