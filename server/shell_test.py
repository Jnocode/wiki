"""Interactive SSH deploy for Synology NAS."""
import paramiko
import time
import os

HOST = "192.168.1.107"
PORT = 22
USER = "jnoworldline"
PASS = "J3En@3dzx.aegEg3sTCT"
WIKI_SRC = r"D:\Personal_Website\wiki"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, PORT, USER, PASS, timeout=10, look_for_keys=False, allow_agent=False)

channel = client.invoke_shell(term='vt100', width=132, height=50)
channel.settimeout(8)
time.sleep(3)

def recv():
    data = b""
    while channel.recv_ready():
        data += channel.recv(4096)
    return data.decode(errors="replace")

def send(cmd, wait=1.5):
    channel.send(cmd + "\n")
    time.sleep(wait)
    return recv()

# Read initial banner
banner = recv()
print("=== BANNER ===")
print(banner[:800])

# Send password if prompted
if "try again" in banner.lower() or "assword" in banner.lower():
    print(">>> Sending password for PAM auth...")
    channel.send(PASS + "\n")
    time.sleep(2)
    resp = recv()
    print("AFTER PW:", resp[:500])

# Now we should have a shell prompt
# Run commands one by one
cmds = [
    "whoami",
    "id",
    "ls /volume1/ 2>&1",
    "ls /volume1/docker/ 2>&1 || mkdir -p /volume1/docker/wiki-server/backend/routers",
    "mkdir -p /volume1/docker/wiki-server/frontend/.vitepress",
    "mkdir -p /volume1/docker/wiki-server/frontend/entities",
    "mkdir -p /volume1/docker/wiki-server/frontend/concepts",
    "mkdir -p /volume1/web/wiki",
    "docker --version 2>&1 || echo NO_DOCKER",
    "docker compose version 2>&1 || echo NO_COMPOSE",
]

for cmd in cmds:
    resp = send(cmd)
    print(f"$ {cmd}")
    # Filter out echo of the command itself
    lines = [l for l in resp.split("\n") if cmd.strip() not in l]
    text = "\n".join(lines).strip()
    if text:
        print(text[:400])
    print("---")

channel.close()
client.close()
print("\n✅ Shell test complete")
