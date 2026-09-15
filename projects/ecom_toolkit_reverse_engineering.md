---
title: "電商營運工具箱 (ecom.atmarketing.tw) 逆向工程與架構復刻分析報告"
type: "research"
date: "2026-09-16"
updated: "2026-09-16"
tags: ["reverse-engineering", "ecom", "nextjs", "saas", "architecture", "atmarketing"]
summary: "完整拆解圭話行銷『電商營運工具箱』201+款工具前端Next.js架構、資料結構、純前端vs雙軌運算與商業閉環。"
status: "active"
---

# 🛠️ 電商營運工具箱 (ecom.atmarketing.tw) 逆向工程與架構復刻報告

> 來源對話：https://share.gemini.google/Q1zNAtXChXeC  
> 分析對象：https://ecom.atmarketing.tw/  
> 主理團隊：圭話行銷 ATMarketing（何佳勳 / 小圭）  
> 審查驗收：小衡 (Lead / System Architect)  

---

## 一、 核心業務與產品定位拆解

1. **產品定位**：
   - 台灣在地化、一站式垂直電商營運 AI 工具庫（收錄 186~201 款微型工具）。
   - 解決蝦皮、momo、PChome 賣家與品牌自建站操盤手的日常瑣碎需求（文案、毛利/ROAS計算、棄單挽回、統編檢查等）。
2. **流量漏斗與商業變現模型 (Funnel)**：
   - **頂層獲客 (Top-of-Funnel)**：以「免費/純前端免註冊工具」在社群擴散、SEO 獲客（200+ 靜態落地頁）。
   - **中層留存**：免費會員每日 5 次 AI 額度 + 3 筆雲端存檔。
   - **商業變現 (Monetization)**：
     - **Pro 版訂閱**：NT$ 799/月（年繳 NT$ 5,990），提供 50 次 AI、白標匯出、自訂 Logo。
     - **高客單導流**：全面導流至「會員經營陪跑班」（線上/線下課程）與品牌顧問案。

---

## 二、 前端技術棧與工程架構 (Frontend Stack)

1. **框架**：**Next.js (App Router) + React 18**
   - 結合 SSG (靜態生成) 預先渲染所有 `/tools/[slug]` 頁面以達成極致 SEO。
   - 採用 **Turbopack** 打包 (`/_next/static/chunks/turbopack-...`)。
2. **樣式與元件**：
   - **Tailwind CSS** + Radix UI / shadcn/ui 風格。
   - 支援完整 Dark Mode / Light Mode 平滑切換。
   - 整合 `Ctrl + K` (Command Palette) 全域即時模糊搜尋。
3. **社群分享動態卡片**：
   - `/api/og` 動態 Open Graph 圖片生成引擎，為每個工具自動合成專屬社群預覽圖。

---

## 三、 關鍵設計亮點：雙軌混合運算（零 Token 成本神經）

該專案最值得我們學習的架構決策是 **「純前端本地運算」與「AI API 呼叫」的極端分流**：

| 軌道 | 適用工具類型 | 核心技術 | 成本與隱私優勢 |
| :--- | :--- | :--- | :--- |
| **軌道 A：純前端運算 (Client-only)** | ROAS計算器、庫存預警、物流比較、統編驗證、訂單CSV分析 | 瀏覽器原生 JS、PapaParse、Canvas、localStorage | **0 伺服器運算、0 Token 費用**；符合個資法，用戶數據不離機。 |
| **軌道 B：AI API 驅動** | 一頁式網站生成、6大平台文案、客訴專業回覆 | Next.js API Routes 後端代理 (OpenAI/Claude/Gemini) | 隱藏 API Key，結合台灣消保法/廣告法之 Prompt 範本。 |

---

## 四、 核心工具資料結構 (Data Schema)

由小衡逆向抽取之 `0015b3va-_e6a.js` 活體 JSON 結構：

```typescript
interface EcomTool {
  id: string;          // 唯一識別碼 (如 "landing-builder")
  name: string;        // 工具名稱 (如 "一頁式網站產生器")
  slug: string;        // 路由路徑 (如 "/landing-builder")
  icon: string;        // Emoji 圖示 (如 "📄")
  tagline: string;     // 一句話痛點文案 (如 "填資料，AI 幫你生成一頁式銷售網站")
  status: "live" | "beta"; // 上線狀態
}
```
*(目前已完整提取出 186 款活體工具元數據，存於 `D:/Workspace/agent_office/temp/ecom_extracted_tools.json`)*

---

## 五、 小衡架構裁決：對我們的借鏡與落地方案

1. **不要盲目呼叫大模型（0 額度哲學）**：
   - 像毛利計算、統編驗證、檔期日曆這種「確定性邏輯」，100% 走純前端 JavaScript，**絕不燒 1 個 Token**。
2. **工具箱可作為我們的求職與商業作品集**：
   - 這種「一站式工具矩陣」架構乾淨、視覺衝擊力極強。我們完全可以將這套 Next.js/純 HTML 雙軌架構，產品化整合進你的作品集與 Wiki 門戶。
