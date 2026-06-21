"""Test with direct IP and check IPv6."""
import paramiko, base64

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

# Check if postgres resolves to IPv6
print("=== Resolve postgres (all addresses) ===")
out, err = ssh("docker exec wiki-api python3 -c 'import socket; print(socket.getaddrinfo(\"postgres\",5432))'", timeout=10)
print(out[:300])

# Try with explicit IP 172.22.0.2
code = "import asyncio,asyncpg\nasync def t():\n try:\n  c=await asyncpg.connect(host='172.22.0.2',port=5432,user='wiki',password='wiki123',database='wiki',timeout=10)\n  print('OK',await c.fetchval('SELECT 1'))\n  await c.close()\n except Exception as e:\n  print(f'{type(e).__name__}:{e}')\nasyncio.run(t())\n"
b64 = base64.b64encode(code.encode()).decode()
stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=20)
stdin.close()
out = stdout.read().decode()
print("Direct IP:", out.strip())

# Try with just `host.docker.internal` or gateway
out, err = ssh("docker exec wiki-api python3 -c 'import socket; print(socket.gethostbyname(\"host.docker.internal\"))'", timeout=10)
print("Docker internal:", out.strip()[:100])

client.close()
