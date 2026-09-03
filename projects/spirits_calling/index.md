---
title: "Spirits-Calling UE5.8 賽博靈異垂直切片架構與結案報告"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [unreal_engine, ue5_8, roguelite, vertical_slice, spirits_calling, p10, p11]
summary: "收斂 Spirits-Calling P10/P11 核心體驗流程（冷啟動、主選單、P1探索、收集Psyche、Ghost-Hack、附身奪舍），記錄未提交改動邊界、自動化測試 5/5 全數 PASS 與雙環境驗證指標。"
status: active
source:
  - "artifacts/spirits-p10-onboarding/P10_FINAL_REPORT_2026-09-01.md"
  - "artifacts/spirits-p10-onboarding/evidence.json"
  - "03_Dev_Projects/Spirits-Calling/Docs/PROJECT_STATUS_REPORT.md"
confidence: high
review_after: 2026-10-03
---

# Spirits-Calling UE5.8 垂直切片結案報告 (t_278939a8)

## 1. 核心流程收斂 (P10 / P11 體驗鏈條)

本案垂直切片完整落實 6 階段決定性玩家體驗狀態鏈：
$$\text{冷啟動} \rightarrow \text{主選單} \rightarrow \text{P1\_SoulExplore 探索 (WASD)} \rightarrow \text{收集 Psyche 碎片} \rightarrow \text{Ghost-Hack 侵入} \rightarrow \text{附身奪舍 (Possession Handoff)}$$

### 繁體中文動態引導提示 (HUD)
1. **Move**：`【操作引導】使用 WASD / 方向鍵移動數位幽靈探索區域`
2. **CollectPsyche**：`【操作引導】靠近並收集金色心靈碎片 (Psyche Shard) 累積能量`
3. **DiscoverShell**：`【操作引導】尋找地圖中的休眠載體 (Dormant Shell) 並點擊鎖定`
4. **GhostHack**：`【操作引導】進行 Ghost-Hack 侵入程序，保持連線完成覆寫`
5. **PossessionHandoff**：`【操作引導】成功奪舍義體！已取得控制權`
6. **Complete**：`【教學完成】自由探索賽博靈界與義體戰鬥`

---

## 2. 驗收證據與關鍵指標 (客觀數據依據)

依據 `artifacts/spirits-p10-onboarding/evidence.json` 與 `P10_FINAL_REPORT_2026-09-01.md`：

1. **Unreal Automation Tests 自動化測試套件**：
   - `SpiritsCalling.P10.ColdStart.RouteValidation` [PASS]
   - `SpiritsCalling.P10.OnboardingFlow.FailureRetry` [PASS]
   - `SpiritsCalling.P10.OnboardingFlow.OrderedUnlocks` [PASS]
   - `SpiritsCalling.P10.OnboardingHUD.PromptDisplay` [PASS]
   - `SpiritsCalling.P10.OnboardingWorld.SeamDriven` [PASS]
   - **總體結果**：`5/5 Passed`，Exit Code `0`。

2. **雙環境活體驗證數據**：
   - **Dev Standalone 模式**：生成 227 KB launch log 與 1.35 KB telemetry，驗證地圖載入與 12 個 Shards 生成。
   - **Win64 Shipping Package**：
     - UAT Cook 共計 701 packages，Exit Code `0`。
     - 打包執行檔：`Spirits_Calling.exe` (161.38 MB)。
     - 透過 `-SmokeReadyFile` 與 `-P9TelemetryFile` Sidecar 遙測驗證通過。

3. **C++ 與 Map 改動邊界與工作區保護**：
   - 所有 P10 核心改動已收斂於 commit 序列（`a9e5db4` ~ `a68439c`）。
   - 工作區既有未提交之文檔與設定嚴格保護隔離，不強行 reset，避免污染歷史。

---

## 3. 下一階段 (P11) 推進路線建議

1. **危險區與警示系統 (Danger_Zone & ICE_Fog)**：擴展 P1 地圖至高警戒結界，加入賽博靈界迷霧侵蝕機制。
2. **多樣化義體技能樹**：為不同文明義體實裝專屬 Type1/Type2/Type3 技能與戰鬥靈視。
3. **Nakama 連線對接**：銜接後端 Docker Compose 架構，支援雙人 Ghost-Hack 協力。
