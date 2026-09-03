---
title: "JoJo Trader 台股 MCP Server 建置設計（TradeStation MCP 落地案）"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [MCP, jojo_trading, shioaji, architecture]
summary: "把 TradeStation MCP LLM 券商帳戶架構落地到台股端，以 JoJo Trader 既有 ShioajiConnector 為基礎，建標準 MCP Server 供自然語言查詢與受保護下單。"
status: active
source:
  - "03_Dev_Projects/jojo_trading/src/jojo_trading/core/shioaji_connector.py"
confidence: high
review_after: 2026-10-04
---

# JoJo Trader 台股 MCP Server 建置設計

## 目標
TradeStation MCP 證明「合規券商 + MCP」是未來方向。JoJo Trader 已在台股端具備核心元件（ShioajiConnector、sync_positions.py、行情快取層），本專案將這些封裝成一個標準 MCP Server，讓 LLM（Hermes/Claude/ChatGPT）透過自然語言存取台股券商資料與（受保護的）下單能力。

## 現有可重用資產（已驗證存在）
- `src/jojo_trading/core/shioaji_connector.py`：`ShioajiConnector`，公開方法含唯讀層（`get_positions`, `get_orders`, `get_kbars`, `get_latest_price`, `get_account_margin`, `get_settlements`, `get_futures_snapshot`）與下單層（`place_order`, `place_futures_order`, `cancel_order`）。
- `scripts/sync_positions.py`：固定 IP/PPPoE 自動連線 → `positions_cache` 寫入 `system_settings`。
- 行情路由層：本地 SQLite 快取 → FinMind → Yahoo，全含 `FreshSufficient/Stale/Unavailable` 語意，絕不編造數字。
- Hermes 原生 MCP client 已可用（`native-mcp` skill）；`mcp` Python 套件尚未裝（需 `pip install mcp`）。

## 架構（分層）
```
[LLM: Hermes / Claude Desktop / ChatGPT]
            │ MCP (stdio 或 streamable HTTP)
            ▼
   jojo-mcp-server  (Python, 用 mcp SDK 的 FastMCP 或 LowLevelServer)
      │
      ├── tools: 唯讀（Phase 1 開放）
      │     • get_positions          → 讀 positions_cache（優先）+ 可選即時連線
      │     • get_portfolio_summary  → 部位損益/市值/可用保證金
      │     • get_quote(symbol)      → 行情層路由（快取→FinMind→Yahoo）
      │     • get_kbars(symbol, n)   → 日線K棒，供布林/均線計算
      │     • get_orders             → 未平倉委託查詢
      │     └ analyze_stock(symbol)  → 呼叫既有 deep_stock_analyzer（總經+財報+技術）
      │
      ├── tools: 下單（Phase 2，需 Human-in-the-Loop 確認）
      │     • place_order / place_futures_order / cancel_order
      │     → 全部經「成本重算、限價範圍檢查、曝險上限」守衛 + 明確確認
      │
      └── resources（唯讀資料）: /positions, /quotes/{symbol}, /account
```

## 安全與門檻（參照 TradeStation 之 Human Confirmation）
- **憑證一律走 Windows Credential Manager**（既有 `_prefer_keyring` 模式），絕不落盤、絕不回顯。
- **Phase 1 預設唯讀**：只暴露查詢/分析類工具，不下單。
- **Phase 2 下單**：所有下單工具強制「return order preview → LLM 請使用者確認 → 使用者回傳 token 才執行」；並在 BrokerProfileManager 標記 `allow_trading` 旗標，未開旗標一律拒絕。
- 行情與財報資料維持既有 `DATA_SOURCE_INTEGRITY`：FRESH/STALE/DATA_UNAVAILABLE 語意，不編造。
- stdio transport 沿用 Hermes 環境變數過濾；連線參數在 `~/.hermes/config.yaml` 的 `mcp_servers` 註冊。

## 落地步驟
1. `pip install mcp`（JoJo 專案 venv）。
2. 新增 `scripts/jojo_mcp_server.py`（或 `src/jojo_trading/mcp/server.py`），用 FastMCP 宣告上述唯讀工具。
3. 工具實作重用 `ShioajiConnector` 唯讀方法 + `deep_stock_analyzer`。
4. Hermes `config.yaml` 註冊 `jojo_trading` server（stdio，command 指向該 script）。
5. 驗證：Hermes 啟動即發現 `mcp_jojo_trading_get_positions` 等工具；用 mock profile 跑通讀取與資料誠信標記。
6. Phase 2 才接下單，須獨立 review 通過。

## 驗收標準
- 唯讀工具全部正常回傳，資料帶 FRESH/STALE 語意。
- 無任何憑證落盤或回顯。
- 下單工具（若 Phase 2）未開 `allow_trading` 旗標時被拒。
- Hermes 重啟後 `mcp_jojo_trading_*` 工具可用於對話。