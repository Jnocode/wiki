---
title: "Live2D 產線打磨與圖層位置 (Layer Placement) 根因修復報告"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [live2d, cubism, layer_placement, vskin, bbox, digital_asset, moc3]
summary: "深入剖析 chr001 Live2D 模型在 Viewer 錯位的根因（PNG 圖層缺少全畫布座標導致 drawImage(0,0) 疊合偏移）；確立 Source Master Clone + Placement Manifest 機制與 Cubism CLI 驗證標準。"
status: active
source:
  - "artifacts/live2d-vskin-routing/VISUAL_LAYER_GATE.md"
  - "artifacts/live2d-vskin-routing/VSKIN_CUBISM_CLI_README.md"
  - "artifacts/live2d-vskin-routing/cli_runs/chr001_weak_cli/chr001_weak_cli_export_report.json"
confidence: high
review_after: 2026-10-04
---

# Live2D 產線打磨與圖層位置 (Layer Placement) 修復 (t_cd1837f9)

## 1. 核心流程規約（嚴格杜絕逐件挖空）

全流程依循小衡制定之流水線：
$$\text{多視角設計} \longrightarrow \text{Source Master Clone 分件與差分} \longrightarrow \text{Placement Manifest 空間映射} \longrightarrow \text{Cubism CLI 自動化} \longrightarrow \text{PSD / .moc3 / VTS 交付包}$$

### 根絕逐件挖空（Cut-and-Hole）
- **禁止方式**：在平面圖中粗暴框選摳出前排物件，造成背景層破洞與羽化白邊。
- **合格方式**：以 Source Master 為基底 Clone 出各獨立圖層，並對被遮擋處進行完整筆刷閉合與結構補繪（如額頭、頸部、身軀全輪廓）。

---

## 2. 歷史踩坑深度根因排查：Viewer 錯位之謎 (VISUAL_LAYER_GATE)

查核 `artifacts/live2d-vskin-routing/VISUAL_LAYER_GATE.md` 實證記錄：
- **技術鏈指標**：
  - `TECHNICAL_CHAIN_PASS = true`
  - `VIEWER_LOAD_PASS = true`
  - `RUNTIME_MOVABLE = true`
  - `SELLABLE_VISUAL_PASS = false`（未達上架可售標準）
- **根因分析 (Root Cause)**：
  - 在重組 PSD 時，載入各分割圖層 PNG 時直接以 `(0, 0)` 繪製到 `2048×3072` 畫布上：`ctx.drawImage(image, 0, 0)`。
  - 由於各部位分割圖為裁切後的小圖（Trimmed local images），失去了原始在畫布上的空間偏移量（Placement Offsets），導致 Cubism 雖成功生成合法 Artmesh，但在視覺空間中頭身錯位（`head_body_center_dx: 471 px > 180 px [FAIL]`、`head_body_vertical_gap_px: -446 px [FAIL]`）。

---

## 3. 解決方案：Placement Manifest 與 Cubism CLI 驗證

1. **圖層定位清單 (Placement Manifest)**：
   - 分件產線在分割 PNG 時，強制輸出中繼 JSON：
     ```json
     {
       "layer_name": "head",
       "bbox": [x, y, width, height],
       "global_center": [cx, cy]
     }
     ```
   - PSD Repack 工具必須根據 `bbox[0], bbox[1]` 精確繪製回全畫布對應座標，杜絕 `(0, 0)` 盲畫。
2. **Cubism CLI 官方 Exporter 規格**：
   - 驅動環境：本機 Cubism 5.3 Official Exporter（Java bridge）。
   - 核心參數驗收：`selectedMocVersion: 5`、`importedDrawableCount: 8`、`selectedParameterCount: 27`。
   - Keyform 改善驗證通過：`ears`, `hair_front`, `mouth`, `eye_R`, `eye_L`, `head`, `body`, `hair_back` 自動化綁定。
