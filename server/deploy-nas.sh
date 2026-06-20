#!/bin/bash
# deploy-nas.sh — Synology NAS 部署腳本
# 用法: ssh admin@nas_ip 'bash -s' < deploy-nas.sh
#
# 前置: Container Manager + Web Station 已安裝

set -e

WIKI_SRC="/volume1/web/wiki"
WIKI_DOCKER="/volume1/docker/wiki-server"

echo "=== 1. 建立目錄結構 ==="
mkdir -p "$WIKI_DOCKER/backend"
mkdir -p "$WIKI_DOCKER/frontend"
mkdir -p "$WIKI_SRC"

echo "=== 2. 複製 wiki 內容 ==="
# 假設 build 好的 frontend 在 frontend/.vitepress/dist
cp -r frontend/.vitepress/dist/* "$WIKI_SRC/"
cp -r ../*.md "$WIKI_SRC/" 2>/dev/null || true

echo "=== 3. 啟動容器 ==="
cd "$WIKI_DOCKER"
docker compose up -d

echo "=== 4. 初始化資料 ==="
sleep 3
docker compose exec backend python seed.py

echo "=== 5. Web Station 設定指引 ==="
cat << 'GUIDE'

手動設定 Web Station:
1. DSM → Web Station → 入口網站 → 新增
2. 文件類型: 靜態網站
3. 文件路徑: /volume1/web/wiki
4. 埠: 80 (或 443 配 Let's Encrypt)
5. 反向代理: 新增 /api → http://localhost:8000

GUIDE

echo "✅ 部署完成！"
