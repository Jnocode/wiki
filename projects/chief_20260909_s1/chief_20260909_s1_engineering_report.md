---
title: "外部工程檢查與交付紀錄 — 2026-09-09"
type: project
date: 2026-09-11
updated: 2026-09-11
tags: [distill, chief_20260909_s1]
summary: "**Verdict：BLOCKED。** 可執行 S1 已接通並實機驗證；一張人物圖到可販售 V 皮的完整產線尚未完成。G0 未核准，G1–G5 均未前進。"
status: active
source:
  - "artifacts/live2d-vskin-routing/execution/chief_20260909_s1/ENGINEERING_REPORT.md"
confidence: high
review_after: 2026-12-10
---

# 外部工程檢查與交付紀錄 — 2026-09-09

**Verdict：BLOCKED。** 可執行 S1 已接通並實機驗證；一張人物圖到可販售 V 皮的完整產線尚未完成。G0 未核准，G1–G5 均未前進。

## 四项交付的實際狀態

| 使用者目標 | 本次實際完成 | 尚未完成 |
| --- | --- | --- |
| 自動產圖工作流 | 同一 converter 執行 ComfyUI S1；嚴格 schema、模型雜湊、提交、取圖、逾時恢復、G0 自動檢查 | 任意單圖入口、穩定四視角角色一致性、精確版位與 foreground alpha |
| 自動拆圖工作流 | 保留 60-part contract、clone lineage 與上游阻擋；既有 gate regressions 實際通過 | 正式 M0/W3/差分 adapters；本角色完整且核准的 parts |
| 自動綁骨架工作流 | 保留已登錄 bridge 與 G3 模板阻擋；fixture 驗證 rig gate 仍會拒絕缺少變形器/physics | 真實合格 rig template/census、rebind、XYZ、表情與 runtime QA |
| 人類修改工程檔 | 新增操作文件；每個 run 保存可讀的 input、workflow、程式與 contract 快照 | 可交付模型師的分層 PSD、Cubism `.cmo3` 尚未生成 |

## 根因與修復

原本 `live2d_factory_convert.py` 把所有非 dry-run 操作一律停用，S1 反而依賴尚未由自己產生的 G0 source，形成循環。`--resume` 沒有讀回原 run，只會重建並覆寫報告；雖宣告 RUN_SCHEMA，實際未執行，負 seed 和重複 view 均會被接受。

目前由同一入口執行 S1。正式開始先記錄 run ID／輸入與程式快照，再檢查實際 ComfyUI 節點、checkpoint digest、CUDA、VRAM、queue、磁碟；提交意圖在 POST 前落地。恢復只查同一 prompt ID，拒絕 input/workflow/code/runtime 或產物雜湊漂移，並用 run lock 阻止同一 run 並行。

候選保存原始 PNG bytes、實際尺寸、seed、模型 hash、精確 graph、prompt ID 和來源。G0 在隔離的新目錄執行，FAIL 回寫 run；數值檢查即使成功也不授予獨立視覺核准。下游仍為 W3=0、PSD=0、Cubism=0。

## 實機證據

- r3：prompt `425eaedb-0a83-406c-8567-b5979bb1055c`；ComfyUI 56.54 秒完成，四項 G0 數值檢查失敗。一次恢復沿用原 prompt 與 bytes。
- r4：prompt `14e68a38-25eb-4183-95b8-9148ba8adf57`；同一 seed/checkpoint/workflow，改用模型建議的 tag-based captions 與明確四格描述。ComfyUI 182.29 秒完成，超過 180 秒等待值；`--resume` 取回原工作，歷史中此 run 只有一筆 prompt。
- r4 自動 G0：`A2_sheet_resolution` FAIL 的實際原因是 **2048×2048 PNG 沒有 alpha**。數值檢查沒有驗證真實視角/解剖。實看仍有重複身體與局部碎片、錯誤版位，因此 maker 自行拒絕；未冒充獨立 reviewer 或真人簽核。
- r4 輸入要求 4096×4096 design canvas，既有 workflow 實際生成 2048×2048；兩者均保留，未靜默放大或假稱達標。

主要檔案：

- [最終 run manifest](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/live_chr003_r4/run_manifest.json)
- [候選圖（不合格）](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/live_chr003_r4/design/sheet_candidate.png)
- [G0 實測報告](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/live_chr003_r4/checks/91e06033333147ae9b49a1907d6f678a/chr003/design/G0_multiview_report.json)
- [Maker 拒絕理由](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/candidate_review.json)
- [最終 hash/read-back 審計](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/final_audit.json)
- [對備份的修改 diff](D:/Workspace/artifacts/live2d-vskin-routing/execution/chief_20260909_s1/implementation.diff)

## 已執行命令與結果

以下命令均由專用 `D:\ComfyUI\ComfyUI (1)\ComfyUI\.venv\Scripts\python.exe` 執行，cwd 為本專案根目錄。

| 命令（省略共同 Python 路徑） | Exit code | 結果與證據 |
| --- | --- | --- |
| `-m unittest discover -s factory2/tests -p test_*.py -v`（修改前） | 0 | 18 tests；`baseline_tests.log` |
| `execution/chief_20260909_s1/reproduce_baseline.py`（修改前） | 0 | 非法 seed/view 被接受、異角色 resume 改寫紀錄；`baseline_reproduction.jsonl` |
| `factory2/scripts/gpu_preflight.py --out execution/chief_20260909_s1/baseline_preflight.json` | 0 | queue 空、可用 VRAM 約 10.8 GiB、D: 空間約 502 GiB |
| `factory2/scripts/live2d_factory_convert.py --input execution/chief_20260909_s1/input_chr003_r3.json --out execution/chief_20260909_s1/live_chr003_r3 --stages design --timeout 180` | 7 | 真實候選，停於 G0；`live_first_stdout.json` |
| `factory2/scripts/live2d_factory_convert.py --input execution/chief_20260909_s1/input_chr003_r4.json --out execution/chief_20260909_s1/live_chr003_r4 --stages design --timeout 180` | 7 | 真實逾時保留 prompt；`live_final_stdout.json` |
| 上述 r4 命令加 `--resume` | 7 | 原工作取回，G0 FAIL；`live_final_resume_stdout.json` |
| 上述 r4 命令改為 `--resume --dry-run` | 0 | identity/所有已追蹤產物驗證成功，不改狀態；`final_resume_dryrun.json` |
| `execution/chief_20260909_s1/run_verification.py` | 0 | 35 unittest、11 gate fixtures（0 skipped）、legacy rebuild entrypoint、Python 語法檢查；`verification_fd7c9436/summary.json` |
| `execution/chief_20260909_s1/reproduce_baseline.py`（修改後） | 0 | 子程序改為 exit 7，沒有覆寫；`reproduction_after.jsonl` |
| `execution/chief_20260909_s1/final_audit.py` | 0 | 13 個來源檔、16 個產物 hash 全部吻合，單一 prompt、零下游、狀態 read-back、whitespace 檢查 |

fixture 包含真實 PSD builder/G2 roundtrip，但使用測試圖層，不代表 chr003 PSD 通過。舊 rebuild 測試還有一項僅查檔案存在，不用於品質結論。Python 沒有現成 lint/typecheck 設定；沒有修改 TypeScript。`git diff --no-index --check` 回傳 1（存在修改），沒有 whitespace 問題訊息；另以 `final_audit.py` 驗證 whitespace。沒有 Git worktree、沒有 git init/commit/push。

## 修改與恢復

修改四個既有檔案：`factory2/scripts/live2d_factory_convert.py`、`factory2/scripts/gpu_preflight.py`、`factory2/contracts/factory_run_v1.schema.json`、`factory2/EXECUTION_STATUS.json`。修改前原始 bytes 保留於本目錄 `backups/`。r3 所用的中間程式版本另保留在 `backups/live_implementation_v1/`；r4 的精確程式版本在自己的 `inputs/`。

新增內部 adapter `factory2/scripts/factory_s1.py`、17 項測試的 `factory2/tests/test_factory_s1.py`、`factory2/requirements-core.txt`、[操作文件](D:/Workspace/artifacts/live2d-vskin-routing/factory2/README_OPERATIONS.md)、`.codex/PLAN.md` 與本次隔離的測試/執行證據。ComfyUI 使用原有安裝啟動；未替換模型、修改系統 Python 或重建其他環境。

## 剩餘風險與下一步

目前不能交付一張人物圖直接生成可販售 V 皮。最先需解決的是來源生成：加入同一角色圖像參照與明確版位/姿勢控制，以及保持輪廓細節的真實 alpha，產出新的 G0 候選。兩次對照已證明 prompt-only 不能可靠地約束四視圖；停止盲目 prompt 迭代。完成獨立 G0 review 前，下游不得執行。

仍缺正式拆件/遮擋補全與差分 adapter、合格 Cubism rig template/census、可供人工微調的 PSD/.cmo3、G4 runtime 驗證與 G5 真人簽核。現有數值 G0 的「consistency」其實只量顏色/梯度，必須保留獨立視覺閘門。

[BD2 Viewer 原始依賴](https://github.com/Jelosus2/BD2-L2D-Viewer/blob/main/package.json) 使用 Spine player 4.1.55，可作動作品質參考；Cubism/VTube Studio 相容性另驗證。ComfyUI 呼叫依 [官方範例](https://github.com/Comfy-Org/ComfyUI/blob/master/script_examples/websockets_api_example.py) 與本機 0.34.6 核對；r4 prompt 格式依 [Animagine XL 4.0 model card](https://huggingface.co/cagliostrolab/animagine-xl-4.0) 調整。
