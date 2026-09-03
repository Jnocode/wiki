---
title: "SMC (Smart Money Concepts) 與量化風控策略引擎深度驗證"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [smc, pivot, atr, ema, quant_trading, jojo_trading, backtest]
summary: "深入驗證 jojo_trading 策略引擎中 SMCStrategy (PivotState, TrailingExtremes, Wilder ATR) 之實體代碼結構，確立市場結構突破 (BOS)、動態 ATR 風控與布林位階之回測風控規範。"
status: active
source:
  - "03_Dev_Projects/jojo_trading/src/jojo_trading/strategies/smc_strategy.py"
  - "03_Dev_Projects/jojo_trading/data/stocks.db"
confidence: high
review_after: 2026-10-04
---

# SMC 策略引擎與量化風控深度實測 (t_dc55fa29)

## 1. SMC 策略核心架構與實體程式碼

專案實體程式碼路徑：`/mnt/d/Workspace/03_Dev_Projects/jojo_trading/src/jojo_trading/strategies/smc_strategy.py`

### 關鍵狀態類別與參數規格
- **PivotState 狀態機**：
  - `current_level`：當前結構樞軸價格。
  - `last_level`：前期結構樞軸價格。
  - `crossed`：結構是否產生穿越（突破確認）。
  - `bar_index` / `bar_time`：樞軸發生的精確 K 棒索引。
- **TrailingExtremes 軌跡追蹤**：
  - `top` / `bottom`：動態追蹤擺動高點與低點區間。
- **Wilder's Smoothing ATR 動態風控**：
  - 核心平滑演算法：採用指數加權移動平均（`alpha = 1 / period`），精確對齊 TradingView Pine Script RMA/ATR 規範。
  - 預設風控乘數：`atr_length = 14`，`atr_mult = 3.0`，確保在真實市場雜訊中不易被假突破洗出場。

---

## 2. 景氣循環股 vs 實體成長股 隔離風控規格

結合資料庫 `stocks.db`（288 檔標的）與策略特徵：
1. **成長股特徵**：
   - 適合結合 **SMC 結構突破（BOS）+ EMA 趨勢濾網** 進行順勢進場。
   - 因具備實體自由現金流支撐，在突破 Swing High 且回踩確認時擁有較高盈虧比（R:R Ratio）。
2. **景氣循環股特徵**：
   - 水泥（1101/1102）、航運、記憶體等，容易在大週期頂峰呈現極高盈餘但股價即將見頂。
   - **強制風控合約**：在策略選股時，依 `stocks.sector` 實施分流；循環股全面關閉突破追價模式，強制切換為 **布林通道下軌極端超賣區間 + PB Band 估值保護** 逆勢佈局。

---

## 3. 回測系統與資料品質合約指標

- **資料庫正本**：`/mnt/d/Workspace/03_Dev_Projects/jojo_trading/data/stocks.db`
- **合約驗收準則**：
  - `data_quality_score >= 70.0` 方可納入回測候選池。
  - 歷史數據補齊：`last_updated` 需於指定時間窗口內，缺漏交易日超過 5% 強制回報 `DATA_ERROR`（對齊 `verify_data_quality_api.py` 定義之 Fail-closed 規範）。
