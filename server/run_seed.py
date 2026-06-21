"""Run seed.py on NAS and wait for completion."""
import paramiko
import select

HOST = "192.168.1.107"
PORT = 7414
USER = "JnoWorldLine"
PASS = "J3En@3dzx.aegEg3sTCT"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

stdin, stdout, stderr = client.exec_command("/usr/local/bin/docker exec wiki-api python seed.py 2>&1")
stdin.close()

# Stream output
while not stdout.channel.exit_status_ready():
    r, w, e = select.select([stdout.channel], [], [], 0.5)
    if r and stdout.channel.recv_ready():
        data = stdout.channel.recv(4096)
        if data:
            print(data.decode(errors="replace"), end="")

remaining = stdout.read().decode(errors="replace")
if remaining:
    print(remaining)

print(f"\nExit: {stdout.channel.recv_exit_status()}")
client.close()
