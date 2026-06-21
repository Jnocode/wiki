"""Raw TCP test from backend to PG."""
import paramiko, base64

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

code = """
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.settimeout(5)
try:
    s.connect(('172.22.0.2', 5432))
    print('TCP_CONNECTED')
    s.close()
except socket.timeout:
    print('TCP_TIMEOUT')
except Exception as e:
    print(f'TCP_ERROR: {e}')
finally:
    s.close()
"""
b64 = base64.b64encode(code.encode()).decode()
stdin, stdout, stderr = client.exec_command(f"echo '{b64}' | base64 -d | /usr/local/bin/docker exec -i wiki-api python3 2>&1", timeout=10)
stdin.close()
print(stdout.read().decode().strip())
client.close()
