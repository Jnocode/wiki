# Wiki Server — Full-stack 知識庫後端

部署於 Synology NAS Web Station。

## 架構

```
外部 → Web Station (Nginx) ─┬─ 前端靜態 (VitePress)
                            ├─ /api/* → FastAPI (Container)
                            └─ /search → Meilisearch (Container)
```

## 前置條件

- DSM 7.2+ 已安裝 **Container Manager**
- DSM 已安裝 **Web Station**
- DSM 已安裝 **PostgreSQL 16**（或 Container 跑）

## 一鍵部署

```bash
ssh admin@nas_ip -p 22
cd /volume1/docker/wiki-server
docker compose up -d
```

然後在 Web Station 新增「入口網站」指向 `/volume1/web/wiki/`，
並設定反向代理 `/api` → `http://localhost:8000`。

## 初始化

```bash
# 將 wiki 內容匯入 DB 和 Meilisearch 索引
docker compose exec backend python seed.py
```
