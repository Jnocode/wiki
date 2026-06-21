"""Debug asyncpg failure with more details."""
import paramiko, base64, sys

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

code = """
import asyncio,asyncpg,traceback,sys
async def t():
    try:
        c=await asyncpg.connect(host='postgres',port=5432,user='wiki',password='wiki123',database='wiki',timeout=15)
        print('OK',await c.fetchval('SELECT 1'))
        await c.close()
    except asyncio.TimeoutError:
        print('TIMEOUT after 15s')
    except Exception as e:
        print(f'TYPE:{type(e).__name__}')
        print(f'MSG:{e}')
        traceback.print_exc(file=sys.stdout)
asyncio.run(t())
"""
b64 = base64.b64encode(code.encode()).decode()

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)
stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=30)
stdin.close()
out = stdout.read().decode("utf-8", errors="replace")
err = stderr.read().decode("utf-8", errors="replace")
print(out)
print("ERR:", err[:200])
client.close()
