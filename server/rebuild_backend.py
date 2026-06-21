"""Upload updated docker-compose.yml and rebuild backend on NAS."""
import paramiko
import base64
import os

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

def ssh(cmd, timeout=120):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return out, err

def upload(local, remote):
    with open(local, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d > '{remote}'", timeout=30)
    stdin.close()
    out = stdout.read().decode()
    err = stderr.read().decode()
    return out, err

# 1. Upload fixed docker-compose.yml
print("📤 Uploading docker-compose.yml with DNS...")
upload(os.path.join(r"D:\Personal_Website\wiki\server", "docker-compose.yml"),
       "/volume1/docker/wiki-server/docker-compose.yml")
print("  ✓")

# 2. Rebuild backend with DNS
print("\n🏗️  Rebuilding backend container...")
out, err = ssh(f"echo '{PASS}' | sudo -S /usr/local/bin/docker-compose -f /volume1/docker/wiki-server/docker-compose.yml build --no-cache backend 2>&1", timeout=600)
for line in out.split("\n"):
    l = line.strip()
    if l and "Password" not in l:
        print(f"  {l[:150]}")

# 3. Start all containers
print("\n🚀 Starting containers...")
out, err = ssh(f"echo '{PASS}' | sudo -S /usr/local/bin/docker-compose -f /volume1/docker/wiki-server/docker-compose.yml up -d 2>&1", timeout=60)
for line in out.split("\n"):
    l = line.strip()
    if l and "Password" not in l:
        print(f"  {l[:120]}")

# 4. Verify
print("\n🔍 Status:")
out, err = ssh(f"echo '{PASS}' | sudo -S /usr/local/bin/docker-compose -f /volume1/docker/wiki-server/docker-compose.yml ps 2>&1")
for line in out.split("\n"):
    l = line.strip()
    if l and "Password" not in l:
        print(f"  {l[:120]}")

# 5. Seed
print("\n🌱 Seeding database...")
out, err = ssh(f"cd /volume1/docker/wiki-server && echo '{PASS}' | sudo -S /usr/local/bin/docker-compose exec -T backend python seed.py 2>&1", timeout=30)
for line in out.split("\n"):
    l = line.strip()
    if l and "Password" not in l:
        print(f"  {l[:200]}")

# 6. Test
print("\n🧪 API Health:")
out, err = ssh("curl -s http://localhost:8000/api/health 2>&1")
print(f"  {out.strip()[:100]}")

client.close()
print("\n✅ Done!")
