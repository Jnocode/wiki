"""Direct asyncpg test - pipe code into container."""
import paramiko, base64

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

code = "import asyncio,asyncpg\nasync def t():\n try:\n  c=await asyncpg.connect(host='postgres',port=5432,user='wiki',password='wiki123',database='wiki',timeout=10)\n  print('OK',await c.fetchval('SELECT 1'))\n  await c.close()\n except Exception as e:\n  print(f'FAIL: {e}')\nasyncio.run(t())\n"
b64 = base64.b64encode(code.encode()).decode()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)
stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=20)
stdin.close()
out = stdout.read().decode("utf-8", errors="replace")
err = stderr.read().decode("utf-8", errors="replace")
print("OUT:", out.strip())
print("ERR:", err.strip()[:200])
client.close()
