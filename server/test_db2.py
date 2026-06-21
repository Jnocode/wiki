"""Test DB connection and fix if needed."""
import paramiko

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

def ssh(cmd, timeout=15):
    stdin, stdout, stderr = client.exec_command(cmd, timeout=timeout)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return out, err

# Check if backend can resolve and connect to postgres
print("1. Backend -> postgres DNS resolution:")
out, err = ssh("docker exec wiki-api python3 -c 'import socket; print(socket.gethostbyname(\"postgres\"))'", timeout=10)
print(f"   {out.strip()}")

print("\n2. Check postgres container environment:")
out, err = ssh("docker inspect wiki-db --format '{{json .Config.Env}}' | python3 -c 'import sys,json; [print(e) for e in json.load(sys.stdin) if \"PASS\" in e or \"DB\" in e]'", timeout=10)
print(f"   {out.strip()}")

print("\n3. Check backend container environment:")
out, err = ssh("docker inspect wiki-api --format '{{json .Config.Env}}' | python3 -c 'import sys,json; [print(e) for e in json.load(sys.stdin) if \"DATABASE\" in e]'", timeout=10)
print(f"   {out.strip()}")

# The issue might be that the PG password has special chars in the URL
# Let me use raw IP connection
print("\n4. Direct TCP test from backend:")
out, err = ssh("docker exec wiki-api python3 -c 'import socket; s=socket.socket(); s.settimeout(5); s.connect((\"172.21.0.3\",5432)); s.close(); print(\"TCP OK\")'", timeout=10)
print(f"   {out.strip()[:100]}")

# Try connecting with explicit parameters (no URL)
print("\n5. Try asyncpg with explicit params:")
out, err = ssh("docker exec wiki-api python3 -c 'import asyncio,asyncpg; async def t(): c=await asyncpg.connect(host=\"172.21.0.3\",port=5432,user=\"wiki\",password=\"wiki123\",database=\"wiki\",timeout=5); print(\"DB OK\"); await c.close(); asyncio.run(t())'", timeout=15)
print(f"   {out.strip()[:200]}")

client.close()
