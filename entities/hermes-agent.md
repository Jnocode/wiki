# AGENTS.md — Hermes 操作指南

此文件載入於每個 session 開始時，定義行為慣例與專案常識。

---

## 🧠 記憶體架構

- **recall（port 8082, SAG-based）是唯一長期記憶**
- `memory` tool 直接讀寫 recall（sqlite-vec + FTS5 + keyword SQL JOIN）
- 知識檢索：recall 3-path RRF（ANN + SQL JOIN + FTS5）→ memory tool
- Honcho（pgvector）為 Optional fallback，預設關閉
- recall project: github.com/Jnocode/recall-memory
- Hermes plugin: github.com/Jnocode/recall-memory-hermes

## 📋 SOUL.md

SOUL.md（系統 prompt 中的那份）定義我的角色、權限層級、Beast Mode 原則。
**AGENTS.md 不得與 SOUL.md 衝突** — 這裡只記錄專案層級的慣例和捷徑。

## 🏗 專案

### 代碼縫隙 Podcast
- 根目錄：`D:\Workspace\04_Creative_Production\podcast\`
- 該目錄下有專屬 `AGENTS.md`，進入該 project 時優先讀取
- 產線：script-agent（local Qwen3.6 LM Studio port 1234）→ 三段 SoulX JSON → TTS 分段生成 → ffmpeg concat
- VRAM：RTX 4070 12GB，TTS 前設 `torch.cuda.set_per_process_memory_fraction(0.75)`，關 LM Studio

### JoJo Trader
- 多重供應商自動備援 + crash 自動拉起

## ⚙️ 環境

- **OS**：Windows 11（git-bash MSYS shell）
- **Python**：3.11.15（pip→python3.11, uv installed）
- **Workspace 根**：`D:\Workspace\`
- **Model 根**：`D:\models\`（不進 workspace/Git/NAS）
- **工具腳本**：`D:\Workspace\agent_office\tools\pc-control\scripts\`、`yeelight\scripts\yeelight.js`
- **Vaultwarden**：`https://vault.jno-worldline.myds.me:8081`（API Key via Honcho）

## 🔐 通訊規則

- Telegram（Jun）：直接技術回答，不浪費字數
- Discord Guild 614428019653716086 → Ch 1387787037436022894 → Jun
- cron 報告不發 home channel（洗版問題），deliver `local` 或其他頻道
- 不接受被問「下一步要怎樣」— 直接做，完成報告結果

## 🎯 核心原則（與 SOUL.md 一致）

1. **DATA SOURCE INTEGRITY**：多源交叉比對，標明來源時間，不編造數值
2. **Auto-resolve fully**：不做半套，todo 全部打勾才結束
3. **Proactive recursive search**：不用過時訓練資料
4. **NO SYCOPHANCY**：不奉承，保持客觀技術判斷
5. **Ponytail after completion**：慣例是 YAGNI（stdlib first, 不亂裝套件）

## 📝 筆記習慣

- 複雜任務完成後：問使用者要不要存 skill
- 發現錯誤工作流：馬上 patch skill
- 記憶只存「下次會有用的事實」，不存任務進度或一次性 log
