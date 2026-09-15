---
title: "Recall 核心記憶庫 CI/CD 管線重構與跨平台相容性驗證"
type: "concept"
date: "2026-09-12"
updated: "2026-09-12"
tags: ["recall", "ci-cd", "github-actions", "pytest"]
summary: "修復 Recall 專案遠端 GitHub Actions 測試矩陣、Windows tar 解壓縮路徑與 venv 隔離問題。"
status: "active"
---

# Recall 核心記憶庫 CI/CD 管線重構與跨平台相容性驗證

> 紀錄日期：2026-09-12  
> 核心主題：開源專案 CI/CD 自動化測試與環境防禦  

## 1. 核心修復
- **CI 測試矩陣修復**：解決 Windows 與 Linux 環境下 symlink 與虛擬環境路徑解析差異，達成全矩陣綠燈。
- **依賴邊界隔離**：確保 `test_p0_improvements.py` 在乾淨環境下零殘留執行。