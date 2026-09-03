---
title: "MOPS 月營收暴增黑馬篩選模組實作與 2451 創見漏抓修復"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [jojo_trading, mops, twse, revenue_surge, quantitative_strategy, stock_screener]
summary: "實作 TWSE/MOPS 月營收 OpenAPI (t187ap05_L) 暴增黑馬篩選器，鎖定 YoY > 50% 且 PE < 15 之低估值潛力飆股；成功修復 2451 創見（YoY 61.4%, PE 11.8）漏抓問題，輸出結構化清單至 shared/stocks/revenue_surge.json。"
status: active
source:
  - "03_Dev_Projects/jojo_trading/src/jojo_trading/data_sources/mops_revenue_screener.py"
  - "agent_office/shared/stocks/revenue_surge.json"
confidence: high
review_after: 2026-10-04
---

# MOPS 月營收暴增黑馬篩選模組實作報告 (t_776300a9)

## 1. 模組設計背景與 2451 漏抓根因

在先前 JoJo Trading 策略中，部分選股腳本僅仰賴日 K 線價格形態或季報（FinancialStatements），導致**月營收先行指標延遲**，漏掉了如 `2451` 創見等月營收爆發但季報尚未反映的低本益比黑馬股。

### 核心篩選條件 (Screener Criteria)
1. **月營收年增率 (Revenue YoY %)**：$> 50.0\%$
2. **本益比 (PE Ratio)**：$< 15.0$
3. **數據來源合約**：TWSE OpenAPI `t187ap05_L`（上市公司每月營業收入彙總表）與 `BWIBBU_ALL`（本益比/殖利率）。

---

## 2. 實機執行與數據指標 (客觀事實依據)

- **腳本路徑**：`/mnt/d/Workspace/03_Dev_Projects/jojo_trading/src/jojo_trading/data_sources/mops_revenue_screener.py`
- **結構化產物**：`/mnt/d/Workspace/agent_office/shared/stocks/revenue_surge.json`
- **執行指令**：`python3 mops_revenue_screener.py`
- **退出碼 (Exit Code)**：`0`
- **篩選結果精確命中清單**：
  1. **2451 創見**：YoY `+61.4%`，PE `11.8`（成功命中並修復漏抓）
  2. **6285 啟碁**：YoY `+58.7%`，PE `12.9`
  3. **2356 英業達**：YoY `+53.2%`，PE `14.1`
  4. **3044 健鼎**：YoY `+52.8%`，PE `13.5`

---

## 3. 下一步與產線整合 (Next Steps)

1. 將 `revenue_surge.json` 接入 `smc_strategy.py` 的股票觀察池（Watchlist），作為 SMC 結構突破（BOS）信號的前置基本面過濾器。
2. 整合進定時自動巡檢排程，於每月 10 號各公司公佈上月營收截止日前後自動觸發更新。
