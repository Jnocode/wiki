---
title: "JoJo Trader 量化策略與資料品質風控合約"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [trading, quantitative, stocks_db, smc, bollinger, risk_control, backtest]
summary: "確立 stocks.db 資料品質契約（288 檔標的、data_quality_score 指標），實體成長股與景氣循環股隔離機制，SMC 與布林通道量化回測風控標準。"
status: active
source:
  - "03_Dev_Projects/jojo_trading/data/stocks.db"
  - "03_Dev_Projects/jojo_trading/artifacts/verify_data_quality_api.py"
confidence: high
review_after: 2026-10-03
---

# JoJo Trader 量化策略與選股風控架構 (t_dc55fa29)

## 1. stocks.db 資料品質合約 (Data Quality Contract)

實體資料庫正本路徑：`/mnt/d/Workspace/03_Dev_Projects/jojo_trading/data/stocks.db`

### 實體結構與資料指標
- 資料表：`stocks` (共計 **288** 筆標的，包含台泥 1101、亞泥 1102、台積電 2330 等)。
- 核心欄位規格：
  - `code`：股票代碼
  - `name`：公司全稱
  - `sector`：產業別（如水泥、半導體）
  - `price` / `intrinsic_value` / `potential_return`：現價、內在價值與潛在報酬
  - `market_cap` / `fcf`：市值與自由現金流
  - `data_quality_score`：資料品質評分（當前基準線：70.0）
  - `data_source`：資料來源標註（如 `auto_fetcher`）
  - `last_updated` / `is_active`：更新時間與啟用態

---

## 2. 景氣循環股與實體成長股嚴格隔離機制

在傳統本益比與現金流折現 (DCF) 模型中，景氣循環股在景氣頂峰時 PE 最低、獲利最高，容易產生價值陷阱（Value Trap）；而景氣谷底時 PE 最高或虧損，容易誤判為劣質標的。

### 隔離風控規格
1. **產業分類隔離**：
   - **景氣循環股**（水泥、航運、塑化、鋼鐵、記憶體）：禁止使用單一年度 DCF 計算內在價值，需採用過去完整景氣循環（5~10年）常態化獲利或股價淨值比 (P/B Band) 評價。
   - **實體成長股**（先進半導體、軟體服務、高附加價值精密製造）：採用 FCF Growth + ROIC 複合折現模型評估。
2. **負報酬警示與風控閥值**：
   - 現行 DB 數據中，1101 潛在報酬計算為 -98.74%、1102 為 -41.53%，均精準反映出將循環股套用標準 DCF 時產生的扭曲，需透過 `sector` 分流機制實施強制風控覆蓋。

---

## 3. SMC 與布林通道量化回測架構

結合 Smart Money Concepts (SMC) 與波動率位階的雙重過濾策略：

1. **SMC 結構突破 (Pivot + EMA + ATR)**：
   - **Pivot Points**：動態識別高低點擺動高位（Swing High）與擺動低位（Swing Low），確認市場結構改變（ChoCH / BOS）。
   - **EMA 趨勢濾網**：多頭排列基準（$EMA_{20} > EMA_{50}$），價格回踩訂單塊（Order Block）或 FVG（Fair Value Gap）時進場。
   - **ATR 動態風控**：停損點設於結構低點外側 $1.5 \times ATR$ 區間，杜絕雜訊掃損。
2. **布林通道位階風控 (Bollinger Band Range)**：
   - 通道帶寬收縮（Squeeze）作為波動率預警；在帶寬極度壓縮後突破上軌時發起進場信號。
   - 價格觸及上軌 +2σ 且乖離過大時分批止盈，杜絕追高風險。
