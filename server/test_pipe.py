"""Simple docker exec pipe test."""
import paramiko, base64

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

# Simple test
stdin, stdout, stderr = client.exec_command("echo 'print(\"HELLO\")' | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=15)
stdin.close()
out = stdout.read().decode()
err = stderr.read().decode()
print("Simple:", repr(out.strip()), repr(err.strip()))

# Now try with base64
code = "print('PIPE_OK')"
b64 = base64.b64encode(code.encode()).decode()
stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=15)
stdin.close()
out = stdout.read().decode()
err = stderr.read().decode()
print("B64:", repr(out.strip()), repr(err.strip()))

# Now the real test with longer timeout
code2 = "import asyncio,asyncpg\nasync def t():\n try:\n  c=await asyncpg.connect(host='postgres',port=5432,user='wiki',password='wiki123',database='wiki',timeout=15)\n  print('OK',await c.fetchval('SELECT 1'))\n  await c.close()\n except Exception as e:\n  print(f'FAIL:{e}')\nasyncio.run(t())\n"
b64_2 = base64.b64encode(code2.encode()).decode()
stdin, stdout, stderr = client.exec_command(f"echo '{b64_2}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=30)
stdin.close()
out = stdout.read().decode()
err = stderr.read().decode()
print("DB:", repr(out.strip()), repr(err.strip()[:100]))

client.close()
