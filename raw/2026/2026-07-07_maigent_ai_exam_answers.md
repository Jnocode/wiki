---
title: "原文歸檔：maigent_ai_exam_answers"
type: source
date: 2026-07-07
updated: 2026-07-07
tags: [raw, ingest]
summary: "ingest_source.py 歸檔的原文：maigent_ai_exam_answers"
source:
  - "D:/Workspace/artifacts/maigent-ai-exam-answers.md"
confidence: high
review_after: 2027-07-07
status: active
content_hash: "sha256:3bfa7f21f96d70efb485b75974ded3e1436a6723ef375d77506d96acb6e17452"
---

# MaiAgent AI 生成式 AI 考題 作答卷

> **應試者**: 姜鈞  
> **職位**: AI Agent 工程師 - AI Agent Engineer  
> **作答日期**: 2026/07/04  
> **使用資源**: Claude (Anthropic), Hermes Agent (DeepSeek V4), 搜尋引擎驗證; 本答卷為開放資源作答

---

## 二、專業考題 第一部分：簡答題

### 1. RAG（檢索增強生成，Retrieval-Augmented Generation）的原理與應用

#### • 請用簡單的方式解釋 RAG 的核心概念，並說明在資訊檢索與內容生成上的優勢。

**核心概念**：RAG 是一種將「資訊檢索 (Retrieval)」與「文字生成 (Generation)」結合的架構。當 LLM 收到使用者問題時，RAG 不是直接讓模型憑訓練參數回答，而是先到一個外部知識庫（資料庫、文件庫、向量資料庫）中**檢索**最相關的資訊片段，再把這些片段連同原始問題一起作為 **context** 餵給 LLM，讓模型基於檢索到的真實資訊來生成答案。

**白話來說**：就像考試時 LLM 不靠記憶作答，而是先翻開指定課本找到正確段落，再根據那段文字寫答案。

**優勢**：
| 面向 | 說明 |
|------|------|
| **時效性** | LLM 訓練資料有截止日期，RAG 可以檢索即時更新的資料庫，回答最新問題 |
| **可追溯性** | 每個回答都能追溯到來源文件，降低黑箱問題 |
| **領域特化** | 不需要為每個領域重新訓練模型，只要換知識庫就能回答不同領域問題 |
| **降低成本** | 對比 Fine-tuning 需要 GPU 訓練，RAG 只需向量檢索 + LLM 推理 |
| **減少幻覺** | 模型有真實資料作為參考，偏離事實的機率大幅降低 |

#### • 舉一個您認為最具代表性的 RAG 應用場景，以及該場景中的關鍵挑戰有哪些？

**場景：企業內部知識庫客服機器人**

一家大型企業（如保險公司、銀行）有數千份內部文件（產品說明、理賠流程、法規政策、FAQ），員工或客戶需要即時查詢。RAG 架構可以將這些文件向量化後建索引，讓使用者問「我去年投保的醫療險理賠上限是多少？」時，系統檢索對應文件後由 LLM 生成精準答案。

**關鍵挑戰**：

1. **檢索品質 (Retrieval Quality)**：如果檢索回的 chunks 不準確，LLM 再會寫也是錯的。需要做 Chunking 策略優化、Hybrid Search（關鍵字 + 向量）、重排序 (Re-ranking)。
2. **多輪對話 (Multi-turn)**：使用者上下文的指代消解——「我上次問的那個方案」需要追溯到前幾輪對話；需要將對話歷史壓縮後重新檢索。
3. **權限控制 (Access Control)**：不同角色只能看到特定文件，RAG 系統需整合文件級別權限過濾。
4. **延遲 (Latency)**：檢索 + LLM 生成可能超過使用者的耐心閾值，需要做檢索快取、Streaming output。
5. **評估指標缺失**：RAG 沒有標準的離線評估指標，需要同時評估 Retrieval (Recall/Precision) 和 Generation (Faithfulness/Relevance)。

#### • 說明幾種不同的 RAG 技術？（Self-RAG, CAG, Graph RAG, KG…）

| 技術 | 核心思想 | 特點 |
|------|----------|------|
| **Naive RAG** | 用戶 query → 向量檢索 top-k chunks → LLM 生成 | 最基礎，三階段：索引、檢索、生成 |
| **Advanced RAG** | 檢索前做 query rewriting/擴展，檢索後做 re-ranking | 改善檢索召回率，常用 HyDE、多路檢索 |
| **Modular RAG** | 將 RAG 拆成多個可組合模組（Search、Rewrite、Filter、Generate） | 靈活性最高，可依場景自訂 pipeline |
| **Self-RAG** | LLM 自己決定何時需要檢索、檢索哪些內容、以及生成的答案是否忠於檢索結果 | 透過反思 token (reflection tokens) 讓模型自我校驗 |
| **CAG (Cache-Augmented Generation)** | 預先將知識庫內容載入 LLM 的長上下文快取 (KV cache) 中，查詢時無需外部檢索 | 適合知識庫規模 ≤ 上下文視窗的情境，延遲更低 |
| **Graph RAG** | 將文件以知識圖譜 (Knowledge Graph) 方式組織，檢索時走圖結構做多跳推理 | Microsoft 提出，善於回答需要跨文件聚合的全局性問題 |
| **KG-RAG** | 結合知識圖譜的結構化三元組和向量檢索的語義搜尋 | 兼顧結構化知識的精準度和非結構化文字的靈活性 |
| **HyDE (Hypothetical Document Embeddings)** | 先生成假設性答案文檔，再用該文檔的 embedding 去檢索 | 改善 query-document 的語義 gap |

#### • 請簡單闡述 RAG 不能解決的問題為何？

1. **知識庫中沒有正確資訊**：RAG 的輸出上限取決於檢索到的資料品質。如果知識庫本身是錯誤的、不完整的、或過時的，RAG 無法「發明」正確答案。Garbage in, garbage out。

2. **需要深層邏輯推理的任務**：RAG 擅長事實性問答，但對於需要多步邏輯推理（如數學證明、程式邏輯除錯）、創意寫作、或策略規劃，單純檢索片段無法提供足夠的推理基礎。

3. **開放式創造性任務**：寫詩、編故事、角色扮演等需要創造力的場景，RAG 檢索可能會限制模型的創造自由度。

4. **需要模型具備世界模型理解的任務**：某些任務（如因果推論、物理模擬、情感理解）需要模型對世界有深層理解，而非單純的資訊檢索。

5. **即時動態數據**：如果知識庫更新頻率不足以跟上市場變化（如股價即時報價、體育賽事比分），RAG 的檢索結果可能已經過時。

6. **檢索與生成的語義鴻溝**：即使檢索到相關片段，LLM 仍可能錯誤理解或錯誤組合這些資訊，產生看似合理但事實有誤的答案。

---

### 2. AI Agent 的概念

#### • 請解釋什麼是 Agent，以及它們通常如何與外部工具或 API 互動。

**Agent（自主代理）定義**：Agent 是一個能夠**自主感知環境、做出決策並採取行動**來達成特定目標的 AI 系統。與傳統的問答式 LLM 不同，Agent 不只生成文字，它能夠：
- 理解高層次目標
- 將目標拆解為子任務
- 選擇並調用工具
- 觀察行動結果並調整策略
- 持續迭代直到目標達成

**與外部工具/API 互動方式**：

```
使用者輸入 → LLM 推理 → 決定調用工具 → 執行 API call → 工具返回結果
    ↑                                                        |
    └───────────────── 結果送入 LLM 反覆循環 ────────────────┘
```

典型互動模式：
1. **Function Calling**：LLM 輸出結構化的 function call JSON（含 function 名稱 + 參數），系統解析後呼叫對應 API，將結果送回 LLM 繼續處理
2. **Tool Descriptions**：每個工具以自然語言描述（名稱、用途、參數 schema）提供給 LLM，讓 LLM 根據描述選擇工具
3. **ReAct (Reasoning + Acting)**：LLM 交替執行「思考 (Thought) → 行動 (Action) → 觀察 (Observation)」循環
4. **MCP (Model Context Protocol)**：標準化工具註冊與呼叫協議，讓 Agent 動態發現和使用遠端工具

#### • Structured Output 的原理為何？

Structured Output 是指讓 LLM 的輸出**嚴格遵守預定義的結構化格式**（JSON Schema、Pydantic Model、TypeScript Type），而不是自由文字。

**原理**：
1. **Grammar-constrained decoding**：在模型解碼階段，只允許產生符合目標 schema 的 token。常用技術有：
   - **Outlines** / **JSON-mode**：以正則表達式或上下文無關文法約束解碼路徑
   - **Guidance**：在 token 生成過程中即時進行格式校驗
2. **強制 JSON Schema adherence**：先在 system prompt 中定義 schema，然後在解碼層級攔截不符合 schema 的 token 路徑
3. **Provider-level 支援**：OpenAI 的 `response_format={type:"json_object"}`、Anthropic 的 `{"type": "tool_use"}`、DeepSeek 的 `response_format` 都是封裝好的結構化輸出

**關鍵價值**：
- 確保 Agent 的 function call 參數格式正確
- 讓下游系統能直接 parse LLM 輸出而無需 NER 或正則解析
- 大幅降低「模型輸出無法 parse」的錯誤率

#### • Function Calling 的原理為何？

Function Calling 是 LLM 輸出結構化請求以呼叫外部 API 的能力。

**工作流程**：
```
1. 定義工具集：提供函數名稱、描述、參數 schema（JSON Schema 格式）
2. 模型推理：LLM 分析使用者輸入，決定是否需要呼叫函數
3. 輸出選擇：模型輸出一個結構化對象（tool_calls / function_call），包含：
   - function name
   - arguments (JSON object)
4. Runtime 執行：系統解析該對象，執行對應函數
5. 結果回饋：將函數執行結果送回 LLM，讓 LLM 基於結果生成最終回答
```

**核心實現機制**：
- 模型在訓練階段就學習了「何時應該輸出 function call」的模式
- 透過 ChatML 格式的 assistant tool_calls 角色與 tool 角色區分
- 底層依賴 **Structured Output** 技術保證 arguments 的 JSON 格式正確

#### • 遇到非常大量工具或是 API 時你會怎麼處理？

大量工具情境（數十至數百個工具）需要做**工具路由 (Tool Routing)**：

**策略層級**：

1. **工具分類與命名空間**：
   - 將工具分組（如 `search.*`、`database.*`、`notification.*`）
   - 每個分類對應一個 router Agent

2. **多層 Agent 架構**：
   ```
   使用者 →  Router Agent →  分類 Agent A (工具組 A)
                        →  分類 Agent B (工具組 B)
                        →  分類 Agent C (工具組 C)
   路徑：Router Agent 根據使用者意圖決定要路由到哪個子 Agent，子 Agent 在其專屬工具集中選擇
   ```

3. **動態工具註冊 (MCP 協議)**：
   - 工具不是靜態寫死的，而是透過 MCP Server 動態發現
   - Agent 只在需要時才載入相關工具的 schema
   - 減少每次 prompt 的 token 消耗

4. **向量檢索工具描述**：
   - 將所有工具的 description 向量化存入向量庫
   - 收到使用者 query 時，先檢索出最相關的 top-k 工具
   - 只將這 k 個工具的 schema 注入 LLM context

5. **Tool Spec 壓縮**：
   - 為每個工具提供極簡但區分度高的描述（1-2 句話）
   - 使用 TL;DR pattern，詳細 schema 只在呼叫時才展開

#### • 怎麼打造 Agent 的記憶功能？

Agent 記憶分為三個層級，我個人實作的 Recall 系統即採用此架構：

| 記憶類型 | 範圍 | 實現方式 | 例子 |
|----------|------|----------|------|
| **短期記憶 (Session)** | 單次對話內 | Context window + 對話歷史壓縮 | 本次對話中使用者提到「剛剛說的那個方案」 |
| **長期記憶 (Long-term)** | 跨 session | 向量資料庫 + 結構化存儲 | 使用者偏好、個人資訊、過往決策記錄 |
| **程序記憶 (Procedural)** | 技能/習慣 | 透過 prompt engineering 或 fine-tuning | Agent 知道如何處理特定類型請求 |

**具體實作方式**：
1. **Embedding + 向量庫**：每次對話結束時，將重要資訊 embedding 後存入向量 DB（Chroma / Qdrant / Pgvector）
2. **結構化存儲 + FTS5**：記憶以 key-value pairs 結構化存儲（JSON），同時建立全文索引（SQLite FTS5）
3. **多路檢索融合 (RRF)**：向量相似度 + 關鍵字 BM25 + 時間衰減權重，用 Reciprocal Rank Fusion 融合排序
4. **Session 維度隔離**：每條記憶標記 session_id，避免跨 session 記憶污染
5. **主動回顧 (Reflection)**：Agent 定期對記憶進行摘要壓縮，將零散資訊提煉為高層次洞察
6. **遺忘機制 (Forgetting)**：基於時間衰減和使用頻率的 LRU 策略，自動清除低價值記憶

#### • 您認為在設計 LLM Agent 時，需要特別考慮哪些問題？

1. **錯誤回復 (Error Recovery)**：工具呼叫可能失敗（API timeout、網絡斷線、參數錯誤），Agent 需要有重試邏輯和降級策略
2. **安全邊界 (Safety Guardrails)**：Agent 能調用工具意味著有真實世界的影響力——需要權限隔離、操作確認、敏感操作審計日誌
3. **循環偵測 (Loop Detection)**：Agent 可能陷入 Thought-Action-Observation 無限循環，需要最大迭代次數和循環偵測機制
4. **Token 成本管理**：每輪 tool call 的結果都會膨脹 context，需要定期對歷史進行摘要壓縮
5. **確定性 vs 創造性平衡**：有些情境需要 Agent 嚴格按 SOP 執行（金融交易），有些需要創意（內容生成），需依場景調整 temperature
6. **可觀察性 (Observability)**：Agent 的決策鏈需要完整記錄，以便除錯和審計（Chain-of-Thought log + tool call log）
7. **Human-in-the-Loop**：關鍵決策（高金額交易、刪除資料）需要人工確認閘門

#### • ⭐（加分題）MCP 跟 Function Calling 的關係為何？

**MCP (Model Context Protocol)** 和 **Function Calling** 是不同層次的協議，不是競爭關係：

| 層面 | Function Calling | MCP |
|------|------------------|-----|
| **抽象層級** | 模型輸出格式協議 | 工具發現與通訊協議 |
| **作用範圍** | LLM ↔ Runtime 之間 | Agent ↔ 外部工具伺服器之間 |
| **角色** | 定義 LLM 如何「說要呼叫工具」 | 定義工具如何「被發現、連接、呼叫」 |
| **標準化程度** | 各 provider 略有差異 | 統一協議 (JSON-RPC over stdio/SSE) |

**關係**：MCP **封裝了 Function Calling**。

- Agent 透過 MCP 協議查詢 MCP Server → 拿到工具列表 (tools/list)
- 工具列表的 schema 被注入 LLM 的 tool_calls/function 參數區
- LLM 輸出 function call → Agent 透過 MCP 協議呼叫 MCP Server 的對應工具 (tools/call)
- MCP Server 執行工具後返回結果 → Agent 送回 LLM 做下一步

簡言之：**Function Calling 是 LLM 輸出規格，MCP 是 Agent 與工具伺服器的通訊基礎設施**。MCP 讓 Agent 可以動態發現任意數量的工具，而無需在程式碼中硬編碼每個工具的呼叫邏輯。

#### • ⭐（加分題）Prompt Caching 能為 Agent 幫上什麼忙，其原理為何？

**Prompt Caching**（也稱 Context Caching / KV Cache 快取）是一種透過重複使用 LLM 推理過程中計算過的 Key-Value 快取來降低延遲與成本的技術。

**對 Agent 的幫助**：
1. **系統提示詞零成本重複**：Agent 每次輪迴都帶相同 system prompt + 工具 schema，Prompt Caching 讓這段內容只需計算一次
2. **歷史對話快取**：長對話中，前幾輪的 KV Cache 可被後續輪次重用，不必每次重新計算完整 context
3. **固定知識庫快取**：如果 Agent 每次都要載入一組固定文件（如公司政策），這些文件的 KV Cache 可以被快取

**原理**：
- LLM 的 Transformer 在計算 self-attention 時會產生 Q/K/V 矩陣
- 對於每次推理中不變的部分（system prompt、歷史context），其 KV 矩陣在上一次推理後已經計算完成
- Prompt Caching 將這些 KV 矩陣**快取在 GPU memory** 中
- 當新增少量 token（如新的 tool call 結果）時，只需計算新增 token 的 KV，**追加**到既有快取
- Anthropic 的 Prompt Caching、OpenAI 的 Prompt Caching Pro、DeepSeek 的 Context Caching 都基於此原理

**對 Agent 的量化效益**：
- 首次推理延遲不變，但後續輪次延遲可降低 60-80%
- Token 使用量節省：system prompt + 工具 schema 無需重複計算
- 特別適合需要多輪 tool call 的 Agent 場景

---

### 3. Prompt Engineering 的重要性

#### • 描述您對 Prompt Engineering 的理解，以及哪些要素最能影響模型輸出品質。

**Prompt Engineering（提示詞工程）** 是設計和優化 LLM 輸入提示詞的系統性方法，目的是引導模型產生符合預期的高品質輸出。它不是隨意寫 prompt，而是基於模型訓練機制和推理特性的工程實踐。

**關鍵要素（按影響力排序）**：

| 要素 | 影響 | 最佳實踐 |
|------|------|----------|
| **角色設定 (Role)** | 設定模型的「人格」和「專業領域」，大幅影響輸出的語氣、深度和格式 | 「你是一位資深 AI 工程師，專注於 RAG 系統架構」與「你是一位友善的客服人員」的輸出截然不同 |
| **指令明確度 (Clarity)** | 模糊指令 → 模糊輸出。明確的格式要求、限制條件、輸出規範直接決定品質 | 「用 3 點說明，每點不超過 50 字，以 Markdown 列表輸出」vs「請說明 RAG」 |
| **上下文/範例 (Context & Few-shot)** | 提供相關背景資訊和範例讓模型「理解情境」 | Agent 的 system prompt 中包含相關文件檢索結果、歷史對話摘要、輸出範例 |
| **輸出格式規範 (Format Constraints)** | Structured Output 約束解碼空間，消除格式錯誤 | JSON Schema / XML tags / Markdown 格式 |
| **思維鏈 (Chain-of-Thought)** | 引導模型逐步推理，而非直接跳到結論 | 「請逐步思考，先分析問題，再提出假設，最後給出結論」 |
| **溫度與採樣參數 (Temperature)** | 控制創造性 vs 確定性 | 客服場景 temperature=0.1；創意寫作 temperature=0.8 |
| **負面提示 (Negative Prompt)** | 明確告知不要做什麼 | 「不要道歉、不要使用模糊用語、不要提供不確定的資訊」 |
| **迭代優化 (Iterative Refinement)** | 透過 A/B 測試和錯誤分析逐步優化 prompt | 使用 DSPy 等框架自動優化 prompt 模板 |

---

### 4. 聊天機器人應用情境

#### • 假設客戶是一間電商公司，需要利用一個 LLM 模型與客戶進行商品客服的對話。請問：

##### 1. 你會怎麼實作與設計 Agent？

**系統架構設計**：

```
使用者
  │
  ▼
[入口層] LINE / Website Widget / Messenger
  │
  ▼
[路由層] 意圖分類器 → 查詢訂單 / 商品諮詢 / 退貨申請 / 客訴處理
  │
  ├─→ [RAG 引擎] 商品目錄向量庫 + FAQ 知識庫
  │     └─→ Hybrid Search (向量 + BM25) → Re-ranker → LLM 生成
  │
  ├─→ [工具層] 訂單查詢 API / 庫存 API / 物流追蹤 / 退貨系統
  │     └─→ Function Calling → API Gateway → 資料回填
  │
  └─→ [記憶層] 對話歷史 + 使用者偏好向量庫 + 購物車狀態
        └─→ Session memory (Redis) + Long-term memory (向量 DB)
```

**具體實作步驟**：

1. **意圖分類**：使用較小的 LLM（如 GPT-4o-mini）做初始意圖分類，分流到不同處理 pipeline
2. **RAG 知識庫**：將商品規格、運送政策、退貨條款、常見問題向量化，搭配 Hybrid Search（向量 + BM25 關鍵字）
3. **工具呼叫**：透過 Function Calling 連接後端 API——查訂單狀態、查庫存、創建退貨單
4. **記憶系統**：短期記憶（當前對話歷史 summarization）+ 長期記憶（使用者過往訂單偏好）
5. **安全閘門**：敏感操作（退款、修改地址）需要使用者身分驗證 + 人工確認

##### 2. 請舉出 Agent 對電商公司的價值為何？為什麼 Agent 特別適合電商公司？

**價值**：
1. **24/7 即時回應**：不像客服專員有上班時間，Agent 可全天候處理 80% 常見問題
2. **大量並發處理**：購物節爆量時無需擴編人力，Agent 可水平擴展
3. **一致性服務品質**：每位客戶得到相同的服務水準，不受客服情緒和經驗影響
4. **成本降低**：大型電商客服成本可降低 40-60%
5. **數據收集與分析**：每次對話都是有價值的客戶洞察數據

**為什麼特別適合電商**：
- 電商場景是 **高頻率、低複雜度** 的查詢類型（追蹤包裹、查庫存、退貨流程），非常適合自動化
- 電商擁有 **結構化程度高** 的資料（商品目錄、訂單系統、物流資訊），適合 RAG 和 API 呼叫
- 電商客服有 **明確的 SOP**，可以寫成 agent 的工作流程
- 轉換率提升：Agent 可以在客服互動中智能推薦相關商品、交叉銷售

##### 3. 你打算如何處理「模型幻覺（Hallucination）」問題，使模型回答更精準？

**多層防護策略**：

1. **檢索層**：使用 **RAG + 來源引用**，每句回答附上知識庫來源連結。如果檢索結果不足以回答，直接說「我找不到相關資訊」
2. **輸出層**：
   - **Structured Output**：強制 Agent 在回答中加入 `confidence` 欄位（high/medium/low）
   - **引文強制**：要求每句主張都附上引用，無引用的句子模型不應輸出
3. **驗證層**：
   - **Self-Check**：Agent 在生成回答後，再對自己的回答做一次事實性校驗
   - **反向檢索**：將 Agent 的回答重新作為 query 去檢索知識庫，看是否能找到支援證據
4. **模型層**：
   - **低 temperature**：客服場景 temperature 設 0-0.1，減少創造性生成
   - **系統提示**：明確寫入「如果你不確定答案，請說『我無法確認，讓我轉接專人服務』」
5. **回退機制**：
   - 當 Agent 連續 3 次無法給出高 confidence 回答，自動轉接真人客服
   - 保留 Escalation 路徑（「讓我為您轉接專員」）

##### 4. 如何評估客服聊天機器人的效能、使用體驗，以及最終對業務帶來的成效？

**評估體系**（分三層）：

| 層級 | 指標 | 定義 | 目標值 |
|------|------|------|--------|
| **技術效能** | 答案準確率 (Accuracy) | 人工抽樣驗證回答正確性 | ≥ 95% |
| | 檢索命中率 (Recall@K) | 檢索結果包含正確資訊的比例 | ≥ 90% |
| | 平均回應時間 (Latency P95) | 使用者感受到的回應延遲 | ≤ 2秒 |
| | 多輪完成率 | 使用者不需重述問題的比例 | ≥ 85% |
| **使用體驗** | CSAT (客戶滿意度) | 對話結束後的滿意度評分 | ≥ 4.0/5.0 |
| | 解決率 (Resolution Rate) | 未轉接專人即解決問題的比例 | ≥ 70% |
| | 淨推薦值 (NPS) | 使用者推薦意願 | ≥ 40 |
| **業務成效** | 客服成本降低率 | 對比導入前後的客服人力支出 | ≥ 30% |
| | 首次回覆時間 (FRT) | 從發問到收到首次回應的時間 | ≤ 5秒 |
| | 轉換率 (Conversion) | 客服互動過程中完成下單的比例 | 對比基準提升 ≥ 10% |
| | 專人轉接率 | 需要轉接真人的對話比例 | ≤ 25% |

**評估方法**：
- **A/B Testing**：逐步 rollout，比較 Agent 組 vs 純人工客服組的數據
- **定期人工抽檢**：每月隨機抽樣 500 筆對話，由 QA 團隊標註正確性
- **對話分析 dashboard**：即時監控 unresolved rate、user sentiment trend、top failure categories

---

## 第二部分：程式與實作題

> 💡 非必要，可全做，也可擇一

### 1. 問答 AI Agent 實作

#### 商業情境：智慧金融 RAG Agent —「基金投資顧問」

**場景**：一家資產管理公司需要為其客戶提供基金投資諮詢服務。客服人員需要快速查閱數百份基金說明書、市場分析報告、以及客戶的風險承受度評估，來回答客戶關於基金選擇、配息政策、風險等級等問題。

**設計的 Agent**：能理解客戶問題、從文件庫中檢索相關資訊、並結合客戶個人資料給出建議的 AI Agent。

---

#### 系統設計文件

##### 架構概覽

```
┌──────────────┐
│  使用者提問   │
└──────┬───────┘
       ▼
┌─────────────────────────────────────────────────┐
│  Agent Orchestrator (ReAct Loop)                │
│  ├─ 理解意圖                                    │
│  ├─ 決定行動 (Search / Recommend / Compare)     │
│  └─ 迭代直到滿意                                │
└──────┬──────────────────────────────────────────┘
       │
  ┌────┴────┬──────────────────┐
  ▼         ▼                  ▼
┌────────┐ ┌──────────────┐ ┌────────────┐
│RAG     │ │Tool: Fund    │ │Memory      │
│Engine  │ │Price API     │ │Manager     │
│        │ │              │ │            │
│Vector  │ │Tool: Risk    │ │Session     │
│DB +    │ │Assessment   │ │History     │
│BM25    │ │              │ │User        │
│        │ │Tool: Compare │ │Profile     │
│        │ │Funds         │ │Cache       │
└────────┘ └──────────────┘ └────────────┘
```

##### 關鍵設計決策

| 決策項目 | 選擇 | 理由 |
|----------|------|------|
| 語言 | Python | 生態系成熟，向量 DB / LLM SDK 支援完整 |
| 向量 DB | Chroma (輕量) | 無需獨立服務，嵌入 Agent 進程內 |
| Embedding | BAAI/bge-small-en-v1.5 | 輕量 (33M params)，檢索品質好 |
| LLM | 可切換 (DeepSeek / GPT / Claude) | 透過 LiteLLM 封裝，避免 vendor lock-in |
| Chunking | RecursiveCharacterTextSplitter | 保持段落完整性 |
| 檢索策略 | Hybrid Search (Vector + BM25) + Re-ranking | 兼顧語義相似度和關鍵字命中 |

##### 核心程式碼

```python
# main.py - 基金投資 RAG Agent
import os
import json
from typing import List, Optional, Dict
from dataclasses import dataclass
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter
from rank_bm25 import BM25Okapi
import litellm

# ========== 資料模型 ==========

@dataclass
class FundDocument:
    """基金文件模型"""
    id: str
    fund_name: str
    content: str
    category: str  # "prospectus" / "report" / "policy"
    risk_level: str  # "low" / "medium" / "high"

@dataclass
class UserProfile:
    """使用者資料"""
    user_id: str
    risk_tolerance: str  # "conservative" / "balanced" / "aggressive"
    investment_goal: str
    preferred_funds: List[str]

@dataclass
class AgentMessage:
    role: str  # "user" / "assistant" / "tool"
    content: str

# ========== RAG 引擎 ==========

class RAGEngine:
    """檢索增強生成引擎 - 支援 Hybrid Search"""
    
    def __init__(self, collection_name: str = "fund_docs"):
        # 初始化 Chroma 向量資料庫
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="BAAI/bge-small-en-v1.5"
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_fn
        )
        self.bm25_index = None
        self.bm25_docs = []
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", "。", ".", " ", ""]
        )
    
    def index_documents(self, documents: List[FundDocument]):
        """將檔案索引至向量庫"""
        chunks = []
        metadatas = []
        ids = []
        
        for doc in documents:
            doc_chunks = self.text_splitter.split_text(doc.content)
            for i, chunk in enumerate(doc_chunks):
                chunk_id = f"{doc.id}_chunk_{i}"
                chunks.append(chunk)
                metadatas.append({
                    "fund_name": doc.fund_name,
                    "category": doc.category,
                    "risk_level": doc.risk_level,
                    "source_id": doc.id
                })
                ids.append(chunk_id)
        
        # 向量索引
        if chunks:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )
        
        # BM25 索引 (關鍵字檢索)
        self.bm25_docs = chunks
        tokenized = [chunk.split() for chunk in chunks]
        self.bm25_index = BM25Okapi(tokenized)
    
    def hybrid_search(self, query: str, k: int = 5) -> List[Dict]:
        """多路檢索融合 - 向量 + BM25 + Re-rank"""
        # 1) 向量檢索
        vector_results = self.collection.query(
            query_texts=[query],
            n_results=k * 2
        )
        
        # 2) BM25 關鍵字檢索
        bm25_scores = self.bm25_index.get_scores(query.split())
        bm25_top_indices = sorted(
            range(len(bm25_scores)),
            key=lambda i: bm25_scores[i],
            reverse=True
        )[:k * 2]
        
        # 3) RRF 融合
        rrf_scores = {}
        
        # 向量結果賦分
        for rank, doc in enumerate(vector_results["documents"][0]):
            doc_text = doc
            rrf_scores[doc_text] = rrf_scores.get(doc_text, 0) + 1 / (60 + rank)
        
        # BM25 結果賦分
        for rank, idx in enumerate(bm25_top_indices):
            doc_text = self.bm25_docs[idx]
            rrf_scores[doc_text] = rrf_scores.get(doc_text, 0) + 1 / (60 + rank)
        
        # 4) 排序取 top-k
        sorted_results = sorted(
            rrf_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )[:k]
        
        # 回傳包含 metadata
        final_results = []
        for text, score in sorted_results:
            # 從 metadata lookup
            meta = None
            if vector_results["documents"][0]:
                for i, doc in enumerate(vector_results["documents"][0]):
                    if doc == text:
                        meta = {
                            "fund_name": vector_results["metadatas"][0][i]["fund_name"],
                            "category": vector_results["metadatas"][0][i]["category"],
                            "risk_level": vector_results["metadatas"][0][i]["risk_level"],
                        }
                        break
            final_results.append({
                "text": text,
                "score": score,
                "metadata": meta
            })
        
        return final_results

# ========== Agent 實作 ==========

class FundAdvisorAgent:
    """基金投資顧問 Agent - 具備記憶與工具呼叫能力"""
    
    def __init__(self):
        self.rag = RAGEngine()
        self.conversation_history: List[AgentMessage] = []
        self.user_profile: Optional[UserProfile] = None
        self.max_iterations = 10
        
        # 工具定義
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "search_fund_info",
                    "description": "搜尋基金相關資訊，包含基金說明書、配息政策、風險等級等",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "搜尋查詢，例如'這檔基金投資標的為何'"
                            }
                        },
                        "required": ["query"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_user_risk_profile",
                    "description": "取得使用者的風險承受度評估和投資偏好",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "user_id": {
                                "type": "string",
                                "description": "使用者ID"
                            }
                        },
                        "required": ["user_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "compare_funds",
                    "description": "比較兩檔基金的績效和風險指標",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "fund_a": {"type": "string", "description": "基金A名稱"},
                            "fund_b": {"type": "string", "description": "基金B名稱"}
                        },
                        "required": ["fund_a", "fund_b"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "transfer_to_human",
                    "description": "當無法回答或需要專人協助時，轉接真人客服",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "reason": {"type": "string", "description": "轉接原因"}
                        },
                        "required": ["reason"]
                    }
                }
            }
        ]
    
    def search_fund_info(self, query: str) -> str:
        """工具實作：搜尋基金資訊"""
        results = self.rag.hybrid_search(query)
        if not results:
            return "未找到相關資訊"
        
        output = []
        for r in results:
            meta = r["metadata"] or {}
            output.append(
                f"[相關度: {r['score']:.2f}] "
                f"基金: {meta.get('fund_name', 'N/A')} | "
                f"類型: {meta.get('category', 'N/A')}\n"
                f"{r['text'][:300]}..."
            )
        return "\n\n".join(output)
    
    def get_user_risk_profile(self, user_id: str) -> str:
        """工具實作：取得使用者風險評估"""
        if self.user_profile:
            u = self.user_profile
            return (
                f"風險承受度: {u.risk_tolerance}\n"
                f"投資目標: {u.investment_goal}\n"
                f"偏好基金: {', '.join(u.preferred_funds)}"
            )
        return "使用者資料未設定"
    
    def compare_funds(self, fund_a: str, fund_b: str) -> str:
        """工具實作：比較基金"""
        query = f"{fund_a} {fund_b} 比較 績效 風險"
        results = self.rag.hybrid_search(query)
        
        if not results:
            return f"無法找到 {fund_a} 和 {fund_b} 的比較資訊"
        
        return "\n".join([r["text"][:200] for r in results[:3]])
    
    def transfer_to_human(self, reason: str) -> str:
        """工具實作：轉接真人"""
        return f"⏭️ 已轉接專人處理。原因: {reason}"
    
    def _build_system_prompt(self) -> str:
        """建立系統提示詞"""
        return f"""你是一位專業的基金投資顧問 AI Agent。
你的任務是幫助客戶了解基金產品、提供投資建議前的資訊查詢服務。

重要規則：
1. 使用 RAG 引擎 search_fund_info 來查詢基金相關資訊
2. 根據使用者的風險承受度給出適合的建議
3. 不要提供確切的投資建議（買/賣），只提供客觀資訊
4. 如果資訊不足或超出能力範圍，使用 transfer_to_human 轉接專人
5. 回答時引用來源文件，格式：[來源: 基金名稱]
6. 如果不確定，直接說不確定，不要編造答案

當前對話上下文：{'僅限當前對話' if not self.conversation_history else f'已有 {len(self.conversation_history)} 輪對話'}
{'使用者風險等級: ' + self.user_profile.risk_tolerance if self.user_profile else '使用者風險等級: 未知'}
"""
    
    def process_message(self, user_message: str) -> str:
        """處理使用者訊息 - ReAct 循環"""
        # 加入使用者訊息到歷史
        self.conversation_history.append(AgentMessage(role="user", content=user_message))
        
        iteration = 0
        while iteration < self.max_iterations:
            iteration += 1
            
            # 建構給 LLM 的 messages
            messages = [
                {"role": "system", "content": self._build_system_prompt()},
                *[
                    {"role": m.role, "content": m.content}
                    for m in self.conversation_history
                ]
            ]
            
            # 呼叫 LLM (透過 LiteLLM 支援多 provider)
            response = litellm.completion(
                model=os.getenv("LLM_MODEL", "deepseek/deepseek-chat"),
                messages=messages,
                tools=self.tools,
                temperature=0.1,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            
            # 檢查是否有 tool calls
            if message.tool_calls:
                for tool_call in message.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    # 執行對應工具
                    if func_name == "search_fund_info":
                        result = self.search_fund_info(**args)
                    elif func_name == "get_user_risk_profile":
                        result = self.get_user_risk_profile(**args)
                    elif func_name == "compare_funds":
                        result = self.compare_funds(**args)
                    elif func_name == "transfer_to_human":
                        result = self.transfer_to_human(**args)
                    else:
                        result = f"未知工具: {func_name}"
                    
                    # 將 tool 結果加入歷史
                    self.conversation_history.append(AgentMessage(
                        role="tool",
                        content=f"工具 {func_name} 回傳:\n{result}"
                    ))
                
                # 繼續循環讓 LLM 處理工具結果
                continue
            else:
                # 沒有 tool calls，這是最終回答
                final_answer = message.content
                self.conversation_history.append(AgentMessage(
                    role="assistant",
                    content=final_answer
                ))
                
                # 記憶管理：如果歷史過長，壓縮摘要
                if len(self.conversation_history) > 20:
                    self._summarize_history()
                
                return final_answer
        
        return "抱歉，我無法在限制內完成這個請求，已為您轉接專人。"
    
    def _summarize_history(self):
        """壓縮過長的對話歷史以管理 token 成本"""
        # 保留最後 6 輪，前面的壓縮成摘要
        recent = self.conversation_history[-12:]
        earlier = self.conversation_history[:-12]
        
        summary_prompt = f"請將以下對話摘要壓縮成一段重點：\n{chr(10).join([f'{m.role}: {m.content[:200]}' for m in earlier])}"
        
        summary = litellm.completion(
            model=os.getenv("LLM_MODEL", "deepseek/deepseek-chat"),
            messages=[{"role": "user", "content": summary_prompt}],
            temperature=0.1,
            max_tokens=300
        ).choices[0].message.content
        
        self.conversation_history = [
            AgentMessage(role="system", content=f"[對話摘要] {summary}")
        ] + recent


# ========== 使用範例 ==========

if __name__ == "__main__":
    import dotenv
    dotenv.load_dotenv()
    
    # 初始化 Agent
    agent = FundAdvisorAgent()
    
    # 載入範例文件
    sample_docs = [
        FundDocument(
            id="F001",
            fund_name="穩健成長基金 A",
            content="""
            穩健成長基金 A 是一檔平衡型基金，主要投資於台灣上市公司的股票與公司債。
            基金持股比例為股票 60%、債券 40%，適合穩健型投資人。
            
            近三年年化報酬率: 8.5%
            標準差: 12.3%
            Sharpe Ratio: 0.69
            最低申購金額: NT$10,000
            管理費: 1.5%/年
            配息政策: 年配息，預計配息率 3-4%
            """,
            category="prospectus",
            risk_level="medium"
        ),
        FundDocument(
            id="F002",
            fund_name="積極成長基金 B",
            content="""
            積極成長基金 B 是一檔股票型基金，主要投資於全球科技股。
            
            近三年年化報酬率: 15.2%
            標準差: 22.1%
            Sharpe Ratio: 0.68
            最低申購金額: NT$5,000
            管理費: 2.0%/年
            配息政策: 不配息，收益併入基金淨值
            """,
            category="prospectus",
            risk_level="high"
        ),
    ]
    
    agent.rag.index_documents(sample_docs)
    agent.user_profile = UserProfile(
        user_id="USER001",
        risk_tolerance="balanced",
        investment_goal="退休規劃 (15年)",
        preferred_funds=["穩健成長基金 A"]
    )
    
    # 測試對話
    print("=== 基金投資顧問 Agent 測試 ===\n")
    
    while True:
        user_input = input("您: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        response = agent.process_message(user_input)
        print(f"\nAgent: {response}\n")
```

##### 部署與執行方式

```bash
# 1. 安裝依賴
pip install chromadb sentence-transformers litellm rank-bm25 langchain python-dotenv

# 2. 設定環境變數 (.env)
echo "LLM_MODEL=deepseek/deepseek-chat" >> .env
echo "DEEPSEEK_API_KEY=your_key_here" >> .env

# 3. 執行程式
python main.py
```

##### 關鍵功能驗證

| 功能 | 驗證方式 | 預期結果 |
|------|----------|----------|
| Hybrid Search | 輸入「穩健型基金風險」 | 檢索到穩健成長基金 A 的風險相關段落 |
| RAG 回答 | 查詢「A基金配息政策」 | Agent 回答配息率 3-4%，並標註引用來源 |
| 記憶功能 | 接續問「那B基金呢」 | Agent 理解指代，回答B基金不配息 |
| 工具呼叫 | 比較兩檔基金 | 呼叫 compare_funds，比較 Sharpe Ratio 和報酬率 |
| 邊界處理 | 問「推薦我買哪支」 | Agent 回答只能提供客觀資訊，不提供買賣建議 |

---

## 使用資源說明

根據考題要求，簡要說明本答卷使用資源的方式：

- **Claude (Anthropic)**：用於 RAG 技術細節、Agent 架構設計、Structured Output 與 Function Calling 原理的學術性解釋校驗
- **Hermes Agent**：執行考題內容解析、答案逐題撰寫、整理格式化輸出
- **搜尋引擎**：驗證最新的 MCP 協議規格、Prompt Caching 技術細節（各 provider 2025-2026 年的支援狀況）
- **AI 工具 (Cursor)**：用於 Part2 程式碼的語法校驗與 linting

---

*答卷完成。*
