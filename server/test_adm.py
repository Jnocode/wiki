import paramiko

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

stdin, stdout, stderr = client.exec_command("whoami && id && ls /volume1/ | head -10", timeout=10)
out = stdout.read().decode().strip()
err = stderr.read().decode().strip()
print("OUT:", out[:500])
print("ERR:", err[:300])
client.close()
