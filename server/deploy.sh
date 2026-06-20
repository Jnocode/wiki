# NAS deploy: build frontend, copy to web directory

set -e

echo "=== Building VitePress frontend ==="
cd /volume1/docker/wiki-server/frontend
npm install
npx vitepress build

echo "=== Copying to Web Station directory ==="
rm -rf /volume1/web/wiki/*
cp -r .vitepress/dist/* /volume1/web/wiki/

echo "=== Starting backend containers ==="
cd /volume1/docker/wiki-server
docker compose up -d
sleep 3
docker compose exec -T backend python seed.py

echo "✅ Done! Wiki is live at http://jno-worldline.myds.me (configure Web Station)"
