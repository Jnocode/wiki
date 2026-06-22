---
title: "MCP (Model Context Protocol) 配置說明"
created: 2026-06-23
updated: 2026-06-23
type: entity
tags: [mcp, hermes, tool]
wikilinks: [[hermes-agent]], [[openclaw]]
---

# MCP (Model Context Protocol) 配置說明

來源: `01.技術/程式碼範例/mcp_config_explanation.md`

## 配置結構

`claude_desktop_config.json` 中的 `mcpServers` 物件定義所有 MCP 伺服器。

## 已配置的 MCP 伺服器

| 伺服器 | 啟動方式 | 用途 | 所需 KEY |
|--------|---------|------|---------|
| GitHub | npx | GitHub API 互動 | GITHUB_PERSONAL_ACCESS_TOKEN |
| Filesystem | npx | 檔案系統讀寫 | — |
| Time | python -m | 時間相關工具 | — |
| Browser Tool MCP | npx | 瀏覽器互動與審計 | — |
| Fetch MCP | node | URL 內容擷取 | — |
| Google Maps | npx | Google Maps API | GOOGLE_MAPS_API_KEY |
| Playwright | npx | 瀏覽器自動化測試 | — |
| Slack | npx | Slack API 互動 | SLACK_API_TOKEN |
| Sequential Thinking | npx | 結構化思考鏈 | — |
| Memory | npx | 記憶管理 | — |

## 格式範例

```json
{
  "mcpServers": {
    "github": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "你的_TOKEN"
      },
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

## Windows 注意事項

- 使用 `cmd` + `/c` 而非直接 `npx`（Windows 路徑處理）
- 環境變數用於傳遞敏感資訊（API Key）
- `disabled: false` 啟用，`true` 停用
- `autoApprove: []` 表示所有工具需手動核准


## 關聯頁面
- [[hermes-agent]]
- [[openclaw]]
