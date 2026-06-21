"""Test asyncpg connection from within container using a script file."""
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

# Write a test script to container
test_code = '''import asyncio, asyncpg

async def test():
    try:
        conn = await asyncpg.connect(
            host="postgres", port=5432,
            user="wiki", password="wiki123",
            database="wiki", timeout=10
        )
        v = await conn.fetchval("SELECT 1")
        print(f"CONNECTED: {v}")
        await conn.close()
    except Exception as e:
        print(f"FAILED: {type(e).__name__}: {e}")

asyncio.run(test())
'''

# Write to temp file
import base64
b64 = base64.b64encode(test_code.encode()).decode()
out, err = ssh(f"echo '{b64}' | base64 -d > /tmp/test_db.py && echo OK")
print(f"Write: {out.strip()[:50]}")

# Execute
out, err = ssh("/usr/local/bin/docker cp /tmp/test_db.py wiki-api:/tmp/ && /usr/local/bin/docker exec wiki-api python3 /tmp/test_db.py 2>&1", timeout=20)
print(f"Result: {out.strip()}")
if err.strip():
    print(f"ERR: {err.strip()[:200]}")

client.close()
