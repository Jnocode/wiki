---
title: "Live2D Cubism 與模型自動化產線打磨架構規範"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [live2d, cubism, pipeline, vskin, digital_asset]
summary: "落實小衡規範之「多視角設計→完整 source master clone 分件/W3差分→Cubism→PSD/moc3/VTS」自動化產線打磨與資產標準化。"
status: active
source:
  - "artifacts/live2d-vskin-routing/VSKIN_CUBISM_CLI_README.md"
  - "artifacts/digital-asset-sku-fable5-account3/live2d_mainline/layer_separation_handoff.md"
  - "artifacts/digital-asset-sku-fable5-account3/live2d_deliverable_levels_reference.md"
confidence: high
review_after: 2026-10-03
---

# Live2D Cubism 與模型自動化產線打磨專案 (t_cd1837f9)

## 1. 核心流程架構與嚴禁事項

產線嚴格遵照小衡規範，貫徹下列流水線：
`多視角設計` → `完整 source master clone 分件 / W3差分` → `Cubism 自動化管線 (vskin-cubism-cli)` → `標準 PSD / .moc3 / VTS 交付包`。

### 核心鐵律：嚴禁逐件挖空原圖
- **違規做法**：直接在單一平面圖上透過套索/摳圖「挖空」前層，導致底層出現破洞、白邊、邊緣羽化殘留，無法進行大角度視角旋轉與自然網格變形。
- **合格規範（Source Master Clone + 差分補繪）**：
  1. 採用 Source Master 克隆出各部件獨立圖層。
  2. 遮擋區域必須完整進行背景閉合與結構補繪（如：移除瀏海後，額頭與眉毛必須是完整連續的平面；移除上衣後，鎖骨與頸部必須完整）。
  3. 各圖層均需為純點陣圖層（Rasterized），不得包含文字層、調整圖層或剪裁遮罩。

## 2. 產線現狀與既有資產盤點 (真實數據依據)

1. **Cubism CLI 自動化橋接器 (vskin-cubism-cli)**：
   - 腳本位置：`D:/Workspace/artifacts/live2d-vskin-routing/scripts/vskin_cubism_cli.mjs`
   - 驅動指令：`vskin-cubism-cli.sh` / `vskin-cubism-cli.cmd`
   - 驗證案例：`chr001_weak_cli`
     - 輸出模型：`chr001_weak_cli.moc3` (11,776 bytes, SHA256: `b85d106cc48f5c896f78abc41e913e9636f45766f86bfc70c20a51e7f9b69440`)
     - 輸出封裝：`chr001_weak_cli.zip` (3,503,506 bytes, SHA256: `16cf060b7446741deb19bd218674f76205e3a0e62cc23863b7337ceb5112c44d`)
     - Keyform 自動綁定：`ears` (2), `hair_front` (2), `mouth` (2), `eye_R` (2), `eye_L` (2), `head` (3), `body` (3), `hair_back` (2)。
     - 執行狀態：`PASS`。

2. **分件規約與解析度合規門檻**：
   - 畫布規格：`4096×6144` px, RGBA 8bit, sRGB。
   - 命名規則：`{群組序號}_{部位英文}_{方位}`（`_l`, `_r`, `_c`）。
   - 標準級目標層數：`60 ± 20` 層。

## 3. 數位資產產品化標準（上架交付結構）

```text
product_delivery_package/
├── 01_runtime_vts/              # VTube Studio / Runtime 可直接載入
│   ├── model.moc3
│   ├── model.model3.json
│   ├── model.physics3.json
│   ├── model.cdi3.json
│   ├── textures/
│   └── vtube_studio_config.vtube.json
├── 02_source_psd/               # 完整分件原始檔 (不挖空)
│   └── character_full_layered_4096.psd
└── 03_docs_and_license/         # 授權與說明書
    ├── README.md
    ├── license.txt
    └── keyforms_summary.json
```
