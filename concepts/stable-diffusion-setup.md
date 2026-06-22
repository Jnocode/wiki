---
title: "Stable Diffusion — 工具與設定"
created: 2026-06-23
updated: 2026-06-23
type: concept
tags: [stable-diffusion, tool, creative]
wikilinks: [[model-training]], [[creative-works]]
---

# Stable Diffusion — 工具與設定

來源: `01.技術/Stable Diffusion/`

## 提示詞結構 (依優先度)

1. 構圖、視角、藝術風格
2. 角色、衣服、氣質
3. 背景、地點、物品
4. 其他想放但不重要

## 常用插件列表

| 插件 | 用途 |
|------|------|
| ControlNet | 精確控制生成 (姿態、深度、邊緣) |
| ADetailer | 臉部修復/細節增強 |
| AnimateDiff | 動畫生成 |
| Civitai Helper | 模型管理 |
| TagComplete | 標籤自動完成 |
| Dynamic Prompts | 動態提示詞 |
| Prompt All in One | 提示詞管理 |
| EasyPhoto | 人像生成 |
| Segment Anything | 影像分割 |
| TensorRT | 效能加速 |
| Ultimate Upscale | 放大增強 |
| FreeU | 取樣優化 |
| OpenPose Editor | 姿勢編輯 |
| WD14 Tagger | 圖片標籤回推 |
| Prompt Travel | 提示詞過渡動畫 |
| Config Presets | 配置預設值 |
| StyleSelectorXL | 風格選擇 |
| Photoshop 插件 | Auto-Photoshop-StableDiffusion-Plugin |

## 模型訓練參數

**Kohya 無學習率優化器:**

- **Adafactor** (Google): 學習較慢、不易過擬
  - LRscheduler=Adafactor, loraTX=0.5, UNET lr=1
- **DAdaptAdam** (Meta): 學習較快、容易過擬
  - Text Encoder lr=1, Network Alpha=1
  - LRscheduler=constant, warmup=0
  - 推薦: Text Encoder = UNET lr = 0.4
  - 參數: decouple=True, weight_decay=0.1, betas=0.9,0.99

**DreamBooth 訓練:** 類+標識符方式


## 關聯頁面

- [[model-training]]
- [[creative-works]]
