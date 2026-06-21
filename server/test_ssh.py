import paramiko

HOST = "192.168.1.107"
USER = "jnoworldline"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(HOST, 22, USER, PASS, timeout=10)
    stdin, stdout, stderr = client.exec_command("uname -a")
    print("OUT:", stdout.read().decode().strip())
    print("AUTH OK")
    client.close()
except Exception as e:
    print(f"FAIL: {e}")
