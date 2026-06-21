"""Check postgres actual binding and test from different angles."""
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

# Check what port postgres is actually listening on
print("=== PG listening ports (from inside PG container) ===")
out, err = ssh("docker exec wiki-db ss -tlnp 2>&1")
print(out)

# Check iptables on the Docker host
print("\n=== Docker iptables ===")
out, err = ssh("sudo iptables -L DOCKER -n 2>&1 | head -20")
print(out[:500])

# Can we reach port 5432 from the host itself?
print("\n=== From NAS host to container ===")
out, err = ssh("curl -s http://172.22.0.2:5432 2>&1 | head -2")
print(f"  HTTP to 5432: {out.strip()[:100]}")
out, err = ssh("timeout 3 bash -c 'echo > /dev/tcp/172.22.0.2/5432 && echo TCP_OK' 2>&1 || echo TCP_FAIL")
print(f"  Bash TCP: {out.strip()[:100]}")

# Check postgres config
print("\n=== PG config ===")
out, err = ssh("docker exec wiki-db cat /var/lib/postgresql/data/postgresql.conf 2>/dev/null | grep -i listen")
print(out[:200])

# Check pg_hba
print("\n=== pg_hba ===")
out, err = ssh("docker exec wiki-db cat /var/lib/postgresql/data/pg_hba.conf 2>/dev/null | grep -v '^#' | grep -v '^$'")
print(out[:500])

client.close()
