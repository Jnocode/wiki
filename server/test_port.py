"""Check port connectivity and try alternate connection method."""
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

# Use curl but via container IP instead
print("=== Test direct IP connection ===")
out, err = ssh("/usr/local/bin/docker exec wiki-api python3 -c \"
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect(('172.21.0.3', 5432))
    print('PORT OPEN')
except Exception as e:
    print(f'CLOSED: {e}')
finally:
    s.close()
\"", timeout=15)
print(out[:200])

# Check actually what port postgres binds to
print("\n=== Check PG port ===")
out, err = ssh("/usr/local/bin/docker exec wiki-db sh -c 'ss -tlnp 2>/dev/null || netstat -tlnp 2>/dev/null || cat /proc/net/tcp' 2>&1 | head -10")
print(out[:300])

# Try with sync driver instead of asyncpg
print("\n=== Try psycopg2 (sync) as fallback ===")
out, err = ssh("/usr/local/bin/docker exec wiki-api python3 -c \"
import psycopg2
try:
    conn = psycopg2.connect(host='172.21.0.3', port=5432, dbname='wiki', user='wiki', password='wiki123', connect_timeout=5)
    print('CONNECTED')
    conn.close()
except Exception as e:
    print(f'FAIL: {e}')
\"", timeout=15)
print(out[:300])

client.close()
