"""Test direct DB connection."""
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

# Try direct psql connection from backend container
print("=== Try psql from backend ===")
out, err = ssh("/usr/local/bin/docker exec wiki-api psql postgresql://wiki:wiki123@postgres:5432/wiki -c 'SELECT 1;' 2>&1", timeout=15)
print(out[:300])

# Check postgres listening address
print("\n=== PG listen address ===")
out, err = ssh("/usr/local/bin/docker exec wiki-db grep listen_addresses /var/lib/postgresql/data/postgresql.conf 2>/dev/null || /usr/local/bin/docker exec wiki-db grep listen /etc/postgresql/postgresql.conf 2>/dev/null || /usr/local/bin/docker exec wiki-db psql -U wiki -c 'SHOW listen_addresses;' 2>&1", timeout=15)
print(out[:200])

# Test connection with python directly
print("\n=== Python direct connection test ===")
out, err = ssh("/usr/local/bin/docker exec wiki-api python3 -c \"import asyncpg,asyncio; print(asyncio.run(asyncpg.connect('postgresql://wiki:wiki123@postgres:5432/wiki', timeout=5)))\" 2>&1", timeout=15)
print(out[:300])

client.close()
