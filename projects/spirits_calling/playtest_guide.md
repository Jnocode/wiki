---
title: "Spirits-Calling 玩家向垂直切片 Playtest 實機指引與驗收標準"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [spirits_calling, playtest, ue5_8, onboarding, ghost_hack, shipping]
summary: "提供專案負責人 Jun 之真人 Playtest 實機操作指南：一鍵啟動腳本 playtest_p10_vertical_slice.bat、3–5 分鐘六大核心節奏反饋矩陣與驗收指標。"
status: active
source:
  - "03_Dev_Projects/Spirits-Calling/playtest_p10_vertical_slice.bat"
  - "artifacts/spirits-p10-onboarding/PLAYTEST_P10_GUIDE.md"
  - "artifacts/spirits-p10-onboarding/evidence.json"
confidence: high
review_after: 2026-10-04
---

# Spirits-Calling P10/P11 垂直切片真人 Playtest 驗收指南 (t_278939a8)

## 1. 快速啟動驗收方式

本案已配置專屬 Windows 快速啟動批次檔，可一鍵拉起遊戲視窗進行流暢驗收：
- **實體路徑**：`D:\Workspace\03_Dev_Projects\Spirits-Calling\playtest_p10_vertical_slice.bat`
- **啟動選項**：
  - `[1] 啟動 Win64 Shipping 發布版`：**最推薦**，已完成 701 packages 完整烘焙（Cooked），幀率極致穩定。
  - `[2] 啟動 Development 獨立視窗版`：包含即時 Console Log 與除錯視窗。

---

## 2. 3–5 分鐘核心體驗驗收點 (Core Loop Checklist)

依據 `artifacts/spirits-p10-onboarding/PLAYTEST_P10_GUIDE.md` 規約，真人測試需確認以下 6 大節奏點：

| 節奏階段 | 畫面表現與核心操作 | HUD 繁中提示字句 |
|---|---|---|
| **1. 冷啟動 & 運鏡** | 啟動直入關卡，3.5 秒全景運鏡無縫過渡至第三人稱 | `【操作引導】使用 WASD / 方向鍵移動數位幽靈探索區域` |
| **2. 靈界位移探索** | 數位幽靈形態浮空移動，平滑滑鼠視野旋轉 | 確認 WASD 位移後自動推進 |
| **3. 能量碎片收集** | 觸碰金色菱形光柱（Psyche Shard），能量數值即時跳動 | `【操作引導】靠近並收集金色心靈碎片 (Psyche Shard) 累積能量` |
| **4. 鎖定休眠載體** | 滑鼠左鍵點擊場景中休眠機械義體進行 Target Lock | `【操作引導】尋找地圖中的休眠載體 (Dormant Shell) 並點擊鎖定` |
| **5. Ghost-Hack 侵入** | 粒子光束連線、覆寫進度條、支援 Failure/Retry | `【操作引導】進行 Ghost-Hack 侵入程序，保持連線完成覆寫` |
| **6. 奪舍附身完成** | 鏡頭切換為實體義體，取得武器與全新戰鬥操作權限 | `【操作引導】成功奪舍義體！已取得控制權` $\rightarrow$ `【教學完成】自由探索` |

---

## 3. 自動化測試與真機運行指標 (客觀數據依據)

- **自動化測試套件**：Unreal Automation Tests **5/5 全數 PASS**，Exit Code `0`。
- **Shipping 封裝產物**：`Spirits_Calling.exe` (161.38 MB)，無缺失依賴。
- **工作區狀態**：維持原始 31 個文件/設定隔離保護，改動完全收斂於 Commit `a9e5db4` ~ `a68439c`。
