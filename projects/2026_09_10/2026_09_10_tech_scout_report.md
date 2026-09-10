---
title: "AI／GameDev 前沿技術嗅探日報 — 2026-09-10"
type: project
date: 2026-09-11
updated: 2026-09-11
tags: [distill, 2026_09_10]
summary: "- **查證時間**：2026-09-10 07:00（UTC+8）"
status: active
source:
  - "artifacts/frontier-tech-scout/2026-09-10/tech-scout-report.md"
confidence: high
review_after: 2026-12-10
---

# AI／GameDev 前沿技術嗅探日報 — 2026-09-10

- **查證時間**：2026-09-10 07:00（UTC+8）
- **runtime 身分**：`DeepSeek-V4-Flash / custom:amd`（cron；task 模板標註之 gpt-5.6-sol pin 與實際 runtime 不符，依數據誠信原則據實標示，不冒充任何模型）
- **交付機制**：Scheduled cron 最終結果自動送達；本輪不自行呼叫 Discord API。
- **狀態契約**：4 張技術卡全部標註 `adoption_status=candidate`；Draft Skill 僅作候選，禁止自動安裝。
- **數據誠信**：官方 GitHub、Hugging Face、ltx.io、NVIDIA DevBlog、arXiv、InfoQ/Decrypt 交叉比對；「官方宣稱」與「已驗證」嚴格分開；查證不到者明說未查證。

---

## 3 點極簡總結

1. **[重大里程碑] LTX-2.5 開源權重上線 — 影片+同步音訊 22B 世界模型**：Lightricks 於 2026-08-12 釋出 LTX-2.5 open weights（HF 單月下載 164 萬次），原生 multishot 多鏡頭連續性、Gemma 4 12B text encoder、16-bit HDR、auto-duration。ComfyUI 官方支援 + API 立即可用（fast $0.09/s@720p）。本機最低 16GB VRAM（官方宣稱），4070 12GB 需靠 ComfyUI int8 variant 實測。
2. **[已驗證可用] Stable Audio 3.0 — 開源音樂/SFX 生成，Small 版免 GPU**：Stability 釋出 open-weight 三款（small-music / small-sfx 433M 可跑 CPU、medium 1.4B 6分20秒）。全授權資料訓練、Variable-length 生成、SFX 模型對 Spirits-Calling 音效設計是即插即用等級。
3. **[重大里程碑] NVIDIA ACE 遊戲 AI 端側全管線就緒**：ACE Game Agent SDK（開源 C/C++）+ UE5 plugins（ASR / SLM / TTS / Audio2Face-3D，MIT 授權，內建 Qwen 3.5 4B GGUF 與 Chatterbox Turbo 350M），NPC 對話可全端側零 API 成本；官方支援 UE 5.5–5.7，Spirits-Calling（5.8）需自行編譯。

---

## 今日採用排序

| 優先序 | 技術 | 狀態 | 直接 Consumer | 下一個可執行動作 |
|---|---|---|---|---|
| **P0** | LTX-2.5 | `[重大里程碑／已驗證可用]` | 行銷片、Podcast 影片化、Spirits-Calling 過場 | ComfyUI 裝官方 LTX nodes，API 跑 10s 1080p smoke test（≈$1.3）；另測 int8 Comfy 版 12GB 可行性 |
| **P0** | Stable Audio 3.0 | `[已驗證可用／待實測]` | Spirits-Calling SFX、Podcast 背景樂 | 本機 `uv sync` stable-audio-3，用 small-sfx 產 3–5 個測試音效，與現有素材對比 |
| **P1** | NVIDIA ACE Game Agent SDK | `[重大里程碑／待實測]` | Spirits-Calling NPC 對話管線 | 申請 UE5.7 插件包，測試專案驗證 ASR→SLM→TTS→A2F 端到端延遲 |
| **P2** | OpenClaw 2.0 (+2026.9.2) | `[重大里程碑／參考]` | Hermes 生態、skill/memory 管線設計 | 讀 Skill Workshop 文件，評估其 skill 驗證流程是否可複用至 Hermes |

---

## 技術評估卡片

### 1. LTX-2.5 — `adoption_status=candidate`

- **定位**：open-weights 世界模型（影片＋同步音訊單 pass），22B DiT。原生 multishot（多鏡頭跨 cut 保持角色/場景/聲音一致）、Diffusion Fidelity Rendering（依場景複雜度分配算力）、auto-duration（依 prompt 預測片長）、16-bit HDR 與 RAW workflow、prompt enhancer。
- **Consumer**：行銷短片、Podcast 影片化、Spirits-Calling 過場/概念片、音效+影片同步素材。
- **ROI**：High。API 立即可用且計價低於多數競品（官方自測 10s 1080p 23.7s 生成）；開源權重可自架可微調。
- **關鍵規格（官方）**：
  - Transformer：`ltx-2.5-22b-distilled-transformer-bf16`（8-step，CFG=1）/ `ltx-2.5-22b-dev-transformer-bf16`（可訓練 base）
  - Text encoder：Gemma 4 12B 自訂版；另有 video-vae + audio-vae + 空間/時間 upsampler
  - 最低 VRAM：**16GB**（官方宣稱）；2×GB200 上 10s 720p 生成 6.8s（官方宣稱）
  - API 計價：`ltx-2-5-fast` $0.09/s@720p、$0.13/s@1080p、$0.19/s@1440p、$0.30/s@4K；`ltx-2-5-pro` $0.12/s@720p、$0.17/s@1080p
  - 授權：open weights、無強制 branding、**ARR < $10M 免費商用**
- **ComfyUI 整合**：官方支援（HF 標籤 comfyui）；釋出 `comfy-int8-convrot` 專用 distilled 檔（**僅限 ComfyUI**）；LTX-2.3 的 LoRA/IC-LoRA 大多可直接沿用（官方稱須逐個驗證）。
- **快速上手**：
  ```bash
  git clone https://github.com/Lightricks/LTX-2.git && cd LTX-2
  uv sync --extra natten
  hf download Lightricks/LTX-2.5 \
    diffusion_models/ltx-2.5-22b-distilled-transformer-bf16.safetensors \
    text_encoders/gemma4-12b-with-proj-ltx-2.5-bf16.safetensors \
    vae/video-vae.safetensors vae/audio-vae.safetensors --local-dir models/LTX-2.5
  uv run python -m ltx_pipelines.distilled \
    --transformer-path models/LTX-2.5/diffusion_models/... \
    --text-encoder-path models/LTX-2.5/text_encoders/... \
    --num-frames 121
  ```
- **驗證邊界**：HF model card（1,644,796 downloads/月、70 個 adapter/28 個 finetune/26 個量化）＋ ltx.io 官方頁 ＋ GIGAZINE（2026-08-12）三源確認。「16GB VRAM」「6.8s on 2×GB200」為**官方宣稱**；4070 12GB 本機未驗證。artifact 分數（Pro 0.28/Fast 0.39）為官方自測，非獨立 benchmark。
- **避坑**：需要 `natten` 依賴（Windows 安裝可能踩編譯）；int8 convrot 檔不可用於 ltx-pipelines/PyTorch；4K/HDR 功能需強硬體；> $10M ARR 需簽付費商用協議。
- **下一步**：ComfyUI 官方 Template 找 LTX-2.5 workflow → API 小額 smoke test（10s 1080p ≈ $1.3）→ 若品質達標，再評估 int8 本機化。
- **來源**：[ltx.io/model/ltx-2-5](https://ltx.io/model/ltx-2-5)｜[HF Lightricks/LTX-2.5](https://huggingface.co/Lightricks/LTX-2.5)｜[GIGAZINE 2026-08-12](https://gigazine.net/gsc_news/en/20260812-ltx-2-5-video-generation-ai)｜[docs.ltx.io/pricing](https://docs.ltx.io/pricing)

### 2. Stable Audio 3.0 — `adoption_status=candidate`

- **定位**：Stability AI 下一代 open-weight 音樂/SFX 生成家族（flow matching + SAME semantic-acoustic autoencoder，4096× 壓縮），全授權資料訓練（AudioSparx + Freesound CC 清理後）。
- **Consumer**：Spirits-Calling 音效設計（small-sfx）、Podcast 背景樂/BGM、遊戲 UI 音效批次生成。
- **ROI**：High。**small 版 CPU 即可跑**（433M，官方宣稱 MacBook M4 數秒內），零 GPU 依賴；medium 可產 6:20 完整曲目；Variable-length 生成避免短片段白算。
- **模型矩陣（官方）**：
  | Model | Params | 硬體 | 最長 | 用途 |
  |---|---|---|---|---|
  | small-music | 433–459M | CPU | 120s | 免 GPU 音樂 |
  | small-sfx | 433–459M | CPU | 120s | 免 GPU 音效 |
  | medium | 1.4B | CUDA/TensorRT | 380s | 高品質音樂+SFX |
  | large | 2.7B | API only | 380s | 頂級品質，無開源權重 |
- **模式**：text-to-audio、audio-to-audio 編輯、inpainting/continuation；LoRA 微調可疊加。
- **授權**：repo MIT；weights 為 Stability AI Community License（**營收 > $1M 需 Enterprise license**）。
- **快速上手**：
  ```bash
  git clone https://github.com/Stability-AI/stable-audio-3 && cd stable-audio-3
  uv sync   # uv-based 安裝
  # 模型：https://huggingface.co/collections/stabilityai/stable-audio-3
  ```
- **驗證邊界**：GitHub（720 stars，MIT）＋ TechCrunch（2026-05-20）＋ arXiv 2605.17991 確認。ComfyUI 整合僅官方新聞稿提及（"available on ComfyUI and other platforms"），**實際 node 未驗證**。中文/繁中場景（如 Podcast 配樂品味）未驗證。
- **避坑**：large 不開源；Small 版音樂與 SFX 分開訓練（small-music 混入 SFX 資料會掉音樂品質，官方明說）；Community License 有營收門檻。
- **下一步**：本機裝 stable-audio-3 → small-sfx 產 3–5 個測試音效（風、腳步、電子嗡鳴）→ 對比現有素材庫品質與延遲。
- **來源**：[GitHub](https://github.com/Stability-AI/stable-audio-3)｜[Stability AI 官網](https://stability.ai/stable-audio)｜[TechCrunch](https://techcrunch.com/2026/05/20/stability-ai-release-a-new-audio-model-that-can-create-six-minute-songs/)｜[arXiv 2605.17991](https://arxiv.org/abs/2605.17991)

### 3. NVIDIA ACE Game Agent SDK + UE5 Plugins — `adoption_status=candidate`

- **定位**：端側（on-device）遊戲 AI companion 全管線。開源 C/C++ Agent SDK（Agent/Chat/RAG API）+ UE5 plugins（ASR、SLM、TTS、Audio2Face-3D），Blueprints/C++ 雙支援，MIT 授權。
- **Consumer**：Spirits-Calling NPC 對話系統（在地化 = 零 API 成本、低延遲、可離線）。
- **ROI**：High。官方內建模型組合即開箱可用；對比雲端 NPC 服務（Inworld 等）省去每字元計費與延遲。
- **內建模型（官方）**：
  - ASR：`nemo-conformer-ctc-120m`（EN 內建，另 7 語言可下載）
  - SLM：`Qwen 3.5 4B` GGUF（本地 text generation + function calling）
  - TTS：`Chatterbox Turbo 350M`（與昨日 Chatterbox 卡同家族，交叉印證其生態地位）
  - 唇形：Audio2Face-3D（regression 2.3 / diffusion 3.0，ONNX-TRT open weights）
  - 底層：NVIDIA In-Game Inferencing (NVIGI) SDK 1.6
- **引擎支援**：官方 plugin 版本 UE 5.5 / 5.6 / 5.7；**UE 5.8（Spirits-Calling 版本）未列官方支援**，需自行編譯。
- **驗證邊界**：NVIDIA DevBlog（2026-06-16 Unreal Fest 2026 公布、2026-05-27）＋ ace-for-games 頁面確認。4070 12GB 實跑延遲未驗證；Qwen 3.5 4B 的 GGUF 品質未獨立驗證。
- **避坑**：舊版 OmniverseLiveLink plugin 需先移除（`.uproject` 內 descriptor 更名 `NV_ACE_Reference`）；僅 NVIDIA GPU；SDK 為 Beta。
- **下一步**：下載 UE5.7 插件包 → 空專案建 Blueprint NPC → 測 ASR→SLM→TTS→A2F 端到端延遲與品質，確認後再評估 UE5.8 編譯移植。
- **來源**：[NVIDIA DevBlog](https://developer.nvidia.com/blog/build-on-device-ai-companions-with-the-nvidia-ace-game-agent-sdk-and-unreal-engine-5-plugins/)｜[ACE for Games](https://developer.nvidia.com/ace-for-games)

### 4. OpenClaw 2.0（v2026.8.1）+ 2026.9.2 — `adoption_status=candidate`

- **定位**：個人 agent 框架史上最大改版（2026-08-31 釋出，16,000+ PR / 933 contributors）；2026-09-02 補 2026.9.2（支援 GPT-6 Astra、Meta Muse Spark 1.3）。
- **Consumer**：Hermes 生態參考（本機 AMD Token Factory 串接 Hermes/OpenClaw）；skill 驗證與記憶管線設計借鏡。
- **ROI**：Medium（參考用，不切換）。其 Skill Workshop 與背景記憶整合是 Hermes skill 管線可直接借鏡的成熟設計。
- **重點變更（官方）**：
  - Session/transcript 遷移 SQLite；`codex/`、`openai-codex/` 模型路由更名 `openai/*`
  - Multiplayer shared sessions（多人共工一個 session，OpenClaw 團隊自用此模式開發自身）
  - Memory：背景整合（provenance-qualified 進長記憶、Dream Diary、可關閉）+ 自動 self-learning 產 skill 提案
  - **Skill Workshop**：引導建立 skill → 寫入前先 validate → skill catalog 安裝/查找 → applied history 審查；壞 skill 個別回報不炸 catalog
  - 安全：approval 綁 request/session/person；session 四種權限模式（read-only/guarded/workspace/full）；共享 credential store 寫入遮罩
- **驗證邊界**：GitHub releases（v2026.8.1/2026.8.2）+ InfoQ（2026-09）+ Decrypt + CellCog 交叉確認。官方明說 3 個 migration（SQLite/OpenProse/routes），且釋出 24h 內有 day-one upgrade bugs（後續 patch 處理中）。
- **避坑**：升級前先備份 session DB；`openclaw doctor --fix` 處理多數 migration；互動式終端升級較安全。
- **下一步**：讀 Skill Workshop 文件，盤點其「寫入前 validate」流程可否映射到 Hermes skill 瘦身/雙閘門制度。
- **來源**：[GitHub releases](https://github.com/openclaw/openclaw/releases/tag/v2026.8.1)｜[docs.openclaw.ai/releases/2026.9.2](https://docs.openclaw.ai/releases/2026.9.2)｜[InfoQ](https://www.infoq.com/news/2026/09/openclaw-2-release/)

---

## 補充觀察

- **Hunyuan3D 2.5（LATTICE 10B）維持「待開源」**：查證 `Tencent-Hunyuan/Hunyuan3D-2` main README（2026-09-10）——news 只到 2025-07-26（HunyuanWorld-1.0），2.5 僅釋出技術報告（arXiv 2506.16504），Open-Source Plan 列了 Inference Code/Checkpoints/ComfyUI/Finetuning/TensorRT 但**無權重釋出公告**。開源前沿用 09-09 結論：本機 2.1 shape、高品質 PBR 走 3.0 API。
- **Wan 2.6**：僅在 LTX 官方比較圖出現（artifact score 0.65），開源權重狀態**未查證**（搜尋後端 403 干擾）；不列卡，下輪補查。
- **交叉印證**：NVIDIA ACE 內建 Chatterbox Turbo = 昨日 Chatterbox 卡生態地位獲得第二來源背書。

---

## Draft Skill 候選（不自動安裝）

- **`draft-skill-ltx25-video-audio`（新增候選）**：LTX-2.5 影片+同步音訊生成 skill。內容方向：`ltx_pipelines` CLI 參數速查、ComfyUI workflow 載入點、API 計價查表、multishot prompt 指南、輸出後製 hook（-16 LUFS、squeeze/cat 音訊拼接沿用 podcast pipeline）。
- 其餘沿用前次有效候選：`draft-skill-ace-step-api-candidate`、`draft-skill-mcp-apps-ui-candidate`、`draft-skill-ue5-mcp`。

## 與上一期差異

| 項目 | 09-09 | 09-10（本期） |
|---|---|---|
| 影片生成 | Wan 3.0（API，待 access） | 新增 **LTX-2.5**（開源權重已上線，API 現買現用）；Wan 2.6 列入未查證追蹤 |
| 音樂/SFX | 無 | 新增 **Stable Audio 3.0**（small-sfx CPU 可跑） |
| 遊戲 AI | 未覆蓋 | 新增 **NVIDIA ACE Game Agent SDK + UE5 plugins**（端側 NPC 全管線） |
| Agent 框架 | Microsoft Agent Framework GA | 新增 **OpenClaw 2.0**（+2026.9.2），列參考 |
| 3D 生成 | Meshy T2 待開源 | 補查 **Hunyuan3D 2.5** 仍待開源（狀態不變，已確認） |

---

## 產物

- `D:/Workspace/artifacts/frontier-tech-scout/2026-09-10/tech-scout-report.md`（本文件）
- `D:/Workspace/artifacts/frontier-tech-scout/2026-09-10/technology-cards.json`
- `D:/Workspace/artifacts/frontier-tech-scout/2026-09-10/draft-skill-ltx25-video-audio/SKILL.md`（候選草稿）