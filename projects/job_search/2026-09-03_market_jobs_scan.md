---
title: "2026-09-03 台灣市場 AI Agent 與自動化職缺情報掃描"
type: project
date: 2026-09-03
updated: 2026-09-03
tags: [job_search, market_scan, ai_agent, automation, career]
summary: "針對台灣求職市場最新 AI Agent、AI 應用工程師、技術 PM 職缺之真實 API 數據掃描，篩選 5 大高匹配具競爭力職缺，並深度對齊 Jun 既有作品集（A2A、Podcast 產線、UE5、量化交易）。"
source:
  - "104 人力銀行即時職缺 API (2026-09-03 實抓資料)"
confidence: high
review_after: 2026-09-17
status: active
---

# 台灣市場 AI Agent / 應用工程師 / 技術 PM 職缺情報掃描

> **執行背景**：落實商業化目標與現金流/求職對齊，掃描台灣目前實時招募中的 AI Agent 與自動化相關核心職缺。
> **數據來源說明**：透過 104 人力銀行即時檢索 API 實地抓取（CakeResume 網頁端受 Cloudflare Managed Challenge 防爬阻斷，本次以 104 最新公布之 95 筆職缺為基準庫進行篩選）。

---

## 一、 5 大高匹配度與競爭力職缺精選

### 1. 新加坡商雲科有限公司 (IDEKU)｜Sr. AI Agent Engineer 資深 AI Agent 工程師
- **薪資競爭力**：**年薪 NT$ 1,100,000 ~ 2,200,000**（實質高薪、標示清晰）
- **工作地點**：台北市松山區
- **JD 核心要求**：
  - 正式環境 Agent 完整工程生命週期：多步驟規劃、工具設計（Tool/Function Calling）、確定性備援（Fallback）、交接人工機制（HITL）。
  - SOTA 模型運用（Claude、OpenAI、Gemini）、MCP（Model Context Protocol）、LangGraph 或自建 Python Agent 引擎。
  - 評估與可觀測性：DeepEval、LLM-as-a-judge、Langfuse/LangSmith 追蹤。
  - 處理工程流程自動化、日誌分析、問題分類與分派。
- **職缺連結**：[https://www.104.com.tw/job/95990](https://www.104.com.tw/job/95990)

---

### 2. 希格諾科技 (SignalPro Technology)｜產品經理 (Product Manager) — AI Agent 平台
- **薪資競爭力**：待遇面議（高技術密度 AI Agent 新創）
- **工作地點**：新北市中和區
- **JD 核心要求**：
  - 打造組織級 AI Agent 治理與情報平台（三層架構：個人 Agent、組織 Agent Hub、跨組織知識決策）。
  - 對齊 **MCP / A2A** 等對外協定版本與相容性策略。
  - 設計防護欄（Guardrails/Rails），基於實際失敗案例建立規則演化。
  - 推動 WORKLOG / ADR 文化，確保架構與產品決策具備可追溯性。
- **職缺連結**：[https://www.104.com.tw/job/91tgt](https://www.104.com.tw/job/91tgt)

---

### 3. 富邦媒體科技 (momo 富邦媒體)｜AI Agent Engineer / AI代理人開發工程師
- **薪資競爭力**：待遇面議（電商龍頭集團，福利與大型系統規模）
- **工作地點**：台北市內湖區
- **JD 核心要求**：
  - 開發與優化 AI Agent 應用：意圖理解、多輪對話、工具調用及流程設計。
  - 建置以 LLM 為核心的應用系統，整合知識檢索、資料處理及 API 服務。
  - 優化 Retrieval、Prompt、Context Management 機制，建立部署、監控及維運流程。
- **職缺連結**：[https://www.104.com.tw/job/95e4y](https://www.104.com.tw/job/95e4y)

---

### 4. 龍星企業股份有限公司｜【AI Agent × 企業AI平台】AI應用暨自動化工程師
- **薪資競爭力**：待遇面議（跨國貿易集團企業流程轉型）
- **工作地點**：台北市中山區
- **JD 核心要求**：
  - 建立完成特定任務的 Agent，將查找、處理、工具呼叫封裝成可重複使用的 **Agent Skill**。
  - 整合 Dify、企業 ERP/SCM 與資料庫，設計 Fallback、停止條件及人工接管流程。
  - 防範 Prompt Injection、資料外洩、成本失控等風險。
- **職缺連結**：[https://www.104.com.tw/job/8nc1h](https://www.104.com.tw/job/8nc1h)

---

### 5. 凱智智能系統 (OKGO)｜AI Native Engineer｜AI Workflow · Agent · Automation
- **薪資競爭力**：依能力高於市場面議（面向歐洲市場智慧移動 SaaS / IoT）
- **工作地點**：彰化縣 / 彈性
- **JD 核心要求**：
  - 建立企業級 AI-driven Workflow 與內部 AI Agent 系統。
  - 深度運用 Claude/GPT、MCP / Tool Calling、Python/TypeScript、Automation Pipeline。
  - 把 AI 深度落地至軟體工程、維運診斷與營運流程。
- **職缺連結**：[https://www.104.com.tw/job/92ktc](https://www.104.com.tw/job/92ktc)

---

## 二、 Jun 既有作品集精準對齊矩陣

| 既有作品 / 專案模組 | 核心技術與工程實踐亮點 | 對齊職缺與切入賣點 |
| :--- | :--- | :--- |
| **A2A 跨 Agent 協作系統**<br>*(Hermes & OpenClaw)* | • **A2A 協定落地**：JSON-RPC 跨程序通訊、Supervisor-Worker 架構。<br>• **Maker ≠ Grader 機制**：執行與查核解耦、獨立 Read-back 驗收。<br>• **防護與安全治理**：嚴格目錄邊界、拒絕明文 secrets 落地、確定性 Fallback。 | • **希格諾科技 (AI Agent PM)**：JD 明文要求「對齊 MCP / A2A 對外協定」，完美 100% 吻合！<br>• **新加坡商雲科 (Sr. Agent Engineer)**：Supervisor/Worker 架構與 Human-in-the-loop 掌控。 |
| **全自動 Podcast 產線**<br>*(MoneyPrinter / 腳本產線)* | • **嚴格 Token/字數閘門**：MAX_CHARS（5,800~7,245字）防灌水阻斷。<br>• **端到端管線工程**：腳本生成 → 語音合成 → 品質校驗自動化。<br>• **結構化上下文管理**：針對長篇文本的章節切分與幻覺抑制。 | • **富邦 momo (AI Agent Engineer)**：對話與生成內容品質評估、Context Management。<br>• **龍星企業 (AI 應用暨自動化)**：Agent Skill 模組化與批次產線自動化。 |
| **量化交易回測系統**<br>*(Quantitative Trading)* | • **高精確度數據流處理**：抗異常值、時序數據清洗、防未來函數。<br>• **事件驅動架構**：低延遲狀態機、即時信號計算與風控停損模組。<br>• **回測評估指標**：夏普比率、最大回撤（MDD）量化分析。 | • **新加坡商雲科**：高可用性、交易繁頻系統的工程思維與量化評估體系。<br>• **OKGO (AI Native)**：數據分析、即時管線串接與高度嚴謹的工程紀律。 |
| **UE5 遊戲開發專案**<br>*(Unreal Engine 5)* | • **複雜狀態機設計**：行為樹（Behavior Tree）、NPC 狀態轉移。<br>• **系統性能調優**：多執行緒優化、Memory Profiling、效能瓶頸排除。<br>• **軟體架構模式**：高內聚低耦合的組件化設計。 | • **所有 Agent 工程師職位**：複雜系統建模、狀態空間管理與 Agent 自主決策迴圈（Reasoning Loop）底層邏輯相通。 |

---

## 三、 行動建議與商業轉化路徑

1. **第一優先投遞**：
   - **新加坡商雲科 (年薪 1.1M~2.2M)**：以 A2A 架構、自建 Python Agent 流程、確定性備援為履歷主軸，直接擊中其「非一般 Chatbot，而是生產級 Agent 生命週期」的要求。
   - **希格諾科技 (AI Agent PM)**：以實際主導 A2A 跨 Agent 通訊架構設計、治理防護原則為作品集主題，展現全台少見的 Protocol-level 實戰經驗。
2. **快速變現 / 接案機會**：
   - **龍星企業、OKGO** 等傳統產業轉型需求強烈，除了正職應徵外，亦可評估提供「Agent Skill 模組化導入」或「內部自動化產線顧問」等短期交付服務。
