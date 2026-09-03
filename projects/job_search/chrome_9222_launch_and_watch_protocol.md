---
title: "Chrome 9222 專用 Profile 啟動批次檔與 CDP 接管寫入協議"
type: project
date: 2026-09-04
updated: 2026-09-04
tags: [chrome_cdp, remote_debugging, 104_login, cakeresume, resume_sync, automation_watcher]
summary: "為 Jun 建立 Windows 原生專用啟動批次檔 (launch_chrome_agent.bat)，配置遠端除錯埠 9222 與獨立 Profile 目錄；實作 watch_cdp_and_inject.py 監聽腳本，待 Jun 在 Windows 點擊登入後立即接管寫入。"
status: active
source:
  - "agent_office/tools/resume-sync/launch_chrome_agent.bat"
  - "agent_office/tools/resume-sync/watch_cdp_and_inject.py"
  - "agent_office/data/resume_sync_payload.json"
confidence: high
review_after: 2026-10-04
---

# Chrome 9222 啟動與自動接管協議報告 (t_6d404273)

## 1. 宿主機環境限制與精確解法

- **WSL2 邊界**：本執行環境為獨立 WSL2 Linux 虛擬容器，僅掛載 `D:` 磁碟，未掛載 `C:\Windows` 與 Windows `cmd.exe`，且 Windows Node `system.run` 需要使用者於工作列手動確認。
- **解鎖捷徑**：小克已在共享磁碟建立 Windows 原生一鍵啟動批次檔：
  `D:\Workspace\agent_office\tools\resume-sync\launch_chrome_agent.bat`
  （內部已預先填妥指向 `104` 與 `CakeResume` 登入頁面之雙分頁指令）。

---

## 2. 啟動指令與獨立 Profile 規格

```bat
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\Users\Jun\.chrome-agent-profile" "https://login.104.com.tw/login" "https://www.cakeresume.com/login"
```
- **安全性與隔離**：採用獨立 Profile `C:\Users\Jun\.chrome-agent-profile`，絕不污染或撞毀 Jun 日常主力 Chrome 瀏覽器。
- **除錯通訊埠**：`127.0.0.1:9222`（供小克 CDP 腳本連線接管）。

---

## 3. 接管監聽腳本 (Watch & Inject)

- **監聽工具**：`/mnt/d/Workspace/agent_office/tools/resume-sync/watch_cdp_and_inject.py`
- **退出碼**：`0`（目前偵測為等待點擊狀態）
- **後續接管流程**：
  1. Jun 雙擊執行 `launch_chrome_agent.bat`，Chrome 彈出。
  2. Jun 於畫面中完成 104 與 CakeResume 簡訊/Email 驗證碼登入。
  3. 小克監聽到 9222 連線與登入態，立即以 WebSocket CDP 注入 `resume_sync_payload.json` 內容。
  4. 自動點擊儲存並回讀 Preview URL，產出驗收報告。
