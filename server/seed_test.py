"""Seed database and test."""
import paramiko

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

def ssh(cmd, timeout=30):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return out, err

# Seed
print("🌱 Seeding database...")
stdin, stdout, stderr = client.exec_command("/usr/local/bin/docker exec wiki-api python seed.py 2>&1", timeout=60)
stdin.close()
out = stdout.read().decode()
err = stderr.read().decode()
for l in out.split("\n"):
    if l.strip():
        print(f"  {l.strip()[:200]}")

# Test
print("\n🧪 Testing...")
out, err = ssh("curl -s http://localhost:8000/api/health")
print(f"  Health: {out.strip()}")
out, err = ssh("curl -s 'http://localhost:8000/api/search?q=stable' | python3 -c \"import sys,json;d=json.load(sys.stdin);print(f'Search results: {d[chr(116)][chr(116)]}')\"")
print(f"  {out.strip()}")
out, err = ssh("curl -s http://localhost:8000/api/pages/ | python3 -c \"import sys,json;d=json.load(sys.stdin);print(f'Pages: {len(d)}\')\"")
print(f"  {out.strip()}")
out, err = ssh("curl -s http://localhost:8000/api/stats")
print(f"  Stats: {out.strip()[:200]}")

# Frontend files check
out, err = ssh("ls /volume1/web/wiki/ | head -10")
print(f"\n📁 /volume1/web/wiki/:")
for l in out.split("\n"):
    if l.strip():
        print(f"  {l.strip()}")

client.close()
print("\n✅ COMPLETE!")
