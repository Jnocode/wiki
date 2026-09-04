# D:\Workspace\03_Dev_Projects\wiki\wiki_sync.py
import os
import re
import sys
import paramiko
import frontmatter
from datetime import datetime

BRAIN_DIR = r"D:\Workspace\agent_office\shared\brain"
KEY_PATH = r"C:\Users\Jun\.ssh\id_ed25519_openclaw"
NAS_HOST = "192.168.1.107"
NAS_PORT = 7414
NAS_USER = "JnoWorldLine"

def build_sync_tarball():
    """在記憶體中打包 Wiki Markdown 檔案，回傳 (tar_bytes, count)"""
    import io
    import tarfile
    import subprocess
    
    # 0. 先行自動編譯 hot.md（吸收 claude-obsidian 的 Hot Cache 機制）
    try:
        hot_compiler = r"D:\Workspace\agent_office\shared\brain_scripts\compile_hot.py"
        if os.path.exists(hot_compiler):
            subprocess.run(["python", hot_compiler], check=True)
            print("✓ 已自動編譯最新 hot.md")
    except Exception as e:
        print(f"⚠️ 編譯 hot.md 失敗: {e}")

    # 1. 優先執行 build_resume.py 編譯最新履歷 HTML
    print("⏳ 正在本地編譯最新個人履歷...")
    try:
        build_script = r"D:\Workspace\03_Dev_Projects\wiki\static\build_resume.py"
        subprocess.run(["python", build_script], check=True)
        print("✓ 本地個人履歷編譯成功")
    except Exception as e:
        print(f"⚠️ 編譯履歷 HTML 失敗，將使用既有檔案: {e}")
        
    dirs_to_scan = {
        os.path.join(BRAIN_DIR, "concepts"): "concepts",
        os.path.join(BRAIN_DIR, "entities"): "entities",
        os.path.join(BRAIN_DIR, "projects"): "projects",
        os.path.join(BRAIN_DIR, "raw", "2026"): "raw/2026",
    }
    
    out_buf = io.BytesIO()
    count = 0
    
    with tarfile.open(fileobj=out_buf, mode="w:gz") as tar:
        for local_dir, nas_sub in dirs_to_scan.items():
            if not os.path.exists(local_dir):
                continue
            for root, _, files in os.walk(local_dir):
                for file in files:
                    if not file.endswith(".md") or file.lower() == "readme.md":
                        continue
                    local_path = os.path.join(root, file)
                    
                    # 計算在 NAS wiki/ 底下的相對路徑
                    rel_path = os.path.relpath(local_path, local_dir).replace("\\", "/")
                    arcname = f"{nas_sub}/{rel_path}"
                    
                    # 載入並處理 frontmatter
                    try:
                        with open(local_path, "r", encoding="utf-8") as f:
                            post = frontmatter.load(f)
                    except Exception as e:
                        print(f"⚠️ 解析 {file} 失敗，跳過: {e}")
                        continue
                    
                    # 自動校正 title
                    if not post.get("title"):
                        m = re.search(r"^#\s+(.+)", post.content, re.MULTILINE)
                        post["title"] = m.group(1).strip() if m else os.path.splitext(file)[0]
                    
                    # 修正 wikilinks 括號
                    post.content = post.content.replace("[[[", "[[").replace("]]]", "]]")
                    
                    # 將修改後的內容轉成 bytes
                    file_content = frontmatter.dumps(post).encode("utf-8")
                    
                    # 建立 tar 內部檔案資訊
                    info = tarfile.TarInfo(name=arcname)
                    info.size = len(file_content)
                    info.mtime = int(datetime.now().timestamp())
                    
                    # 寫入 tar 檔案
                    tar.addfile(info, io.BytesIO(file_content))
                    count += 1
                    
        local_seed = r"D:\Workspace\03_Dev_Projects\wiki\server\backend\seed.py"
        if os.path.exists(local_seed):
            tar.add(local_seed, arcname="seed.py")
            print("✓ 已將修正後的 seed.py 加入同步打包中")

        # 打包 hot.md
        local_hot = os.path.join(BRAIN_DIR, "hot.md")
        if os.path.exists(local_hot):
            tar.add(local_hot, arcname="hot.md")
            print("✓ 已將 hot.md 加入同步打包中")

        # 順便把修改後的 models.py 打包進去，方便推送到 NAS 用於 Docker 複製更新
        local_models = r"D:\Workspace\03_Dev_Projects\wiki\server\backend\models.py"
        if os.path.exists(local_models):
            tar.add(local_models, arcname="models.py")
            print("✓ 已將修正後的 models.py 加入同步打包中")
            
        # 打包重新編譯後的靜態網頁履歷 (static/resume.html)
        local_resume = r"D:\Workspace\03_Dev_Projects\wiki\static\resume.html"
        if os.path.exists(local_resume):
            tar.add(local_resume, arcname="static/resume.html")
            print("✓ 已將 static/resume.html 加入同步打包中")
            
        # 打包門戶首頁 index.html
        local_index = r"D:\Workspace\03_Dev_Projects\wiki\index.html"
        if os.path.exists(local_index):
            tar.add(local_index, arcname="index.html")
            print("✓ 已將門戶首頁 index.html 加入同步打包中")

        # 打包 Markdown 渲染器 viewer.html
        local_viewer = r"D:\Workspace\03_Dev_Projects\wiki\viewer.html"
        if os.path.exists(local_viewer):
            tar.add(local_viewer, arcname="viewer.html")
            print("✓ 已將閱讀器 viewer.html 加入同步打包中")
                    
    return out_buf.getvalue(), count

def get_local_bind_ip(target_host):
    """偵測與 target_host 同網段的本地 IP，若無則返回 None"""
    import socket
    try:
        # 建立一個測試用的 socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((target_host, 80))
        ip = s.getsockname()[0]
        s.close()
        # 針對 Jun 的多網卡特例：192.168.1.109 可用，106 被封鎖
        # 若偵測到 106，我們優先強制改用 109 試試，或依序輪詢 192.168.1.x
        return ip
    except Exception:
        return None

def main():
    print(f"[{datetime.now()}] 啟動 Wiki 自動同步...")
    import socket
    
    k = paramiko.Ed25519Key.from_private_key_file(KEY_PATH)
    
    # 輪詢合適的本地 IP 進行 socket 綁定，避免 Windows 路由走錯網卡被 NAS 封鎖
    local_ips = ["192.168.1.109", "192.168.1.106"]
    detected_ip = get_local_bind_ip(NAS_HOST)
    if detected_ip and detected_ip not in local_ips:
        local_ips.insert(0, detected_ip)
        
    sock = None
    connected_ip = None
    for lip in local_ips:
        try:
            print(f"嘗試綁定本地網卡 IP 連線: {lip}...")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5.0)
            s.bind((lip, 0))
            s.connect((NAS_HOST, NAS_PORT))
            sock = s
            connected_ip = lip
            print(f"✓ 成功透過 {lip} 建立 TCP 連線")
            break
        except Exception as e:
            print(f"  透過 {lip} 連線失敗: {e}")
            
    transport = None
    try:
        if sock:
            transport = paramiko.Transport(sock)
            transport.connect(username=NAS_USER, pkey=k)
            print("✓ SSH 握手與身份驗證成功")
        else:
            print("無法綁定特定內網 IP，嘗試使用預設路由連線...")
            transport = paramiko.Transport((NAS_HOST, NAS_PORT))
            transport.connect(username=NAS_USER, pkey=k)
            
        # 建立並打包 tarball
        tar_bytes, count = build_sync_tarball()
        print(f"✓ 本地打包完成，共準備 {count} 個 Markdown 檔案 ({len(tar_bytes)/1024:.2f} KB)")
        
        # 開啟 SSH 通道傳送並解壓
        print("正在透過 SSH 管道傳送並解壓 Wiki 檔案至 NAS...")
        channel = transport.open_session()
        # tar -xzf - -C /volume1/web/wiki/ 
        # - 是指從標準輸入讀取；-C 是解壓目標目錄
        channel.exec_command("tar -xzf - -C /volume1/web/wiki/")
        
        # 傳送二進位數據
        channel.sendall(tar_bytes)
        channel.shutdown_write() # 告訴遠端 stdin 已經結束
        
        # 等待命令結束並讀取 stdout/stderr
        out = []
        err = []
        while not channel.exit_status_ready():
            if channel.recv_ready():
                out.append(channel.recv(1024).decode())
            if channel.recv_stderr_ready():
                err.append(channel.recv_stderr(1024).decode())
                
        # 讀取剩餘數據
        while channel.recv_ready():
            out.append(channel.recv(1024).decode())
        while channel.recv_stderr_ready():
            err.append(channel.recv_stderr(1024).decode())
            
        tar_exit_code = channel.recv_exit_status()
        if tar_exit_code != 0:
            raise Exception(f"遠端解壓縮失敗 (Exit Code: {tar_exit_code}), Stderr: {''.join(err).strip()}")
        print("✓ 遠端解壓縮完成")
        
        # 執行 models.py 熱更新、容器重啟與索引重建
        print("正在遠端 NAS 更新 wiki-api 容器 models.py 並重啟...")
        channel = transport.open_session()
        cmd = (
            "export PATH=$PATH:/usr/local/bin:/usr/bin; "
            "if [ -f /volume1/web/wiki/models.py ]; then "
            "  sudo docker cp /volume1/web/wiki/models.py wiki-api:/app/models.py && "
            "  echo '✓ 已複製 models.py 至容器'; "
            "fi; "
            "if [ -f /volume1/web/wiki/seed.py ]; then "
            "  sudo docker cp /volume1/web/wiki/seed.py wiki-api:/app/seed.py && "
            "  echo '✓ 已複製 seed.py 至容器'; "
            "fi; "
            "sudo docker restart wiki-api && "
            "echo '✓ 已重啟 wiki-api 容器' && "
            "sleep 3; "
            "sudo docker exec wiki-api python3 seed.py"
        )
        channel.exec_command(cmd)
        
        # 等待命令結束並讀取 stdout/stderr
        out = []
        err = []
        while not channel.exit_status_ready():
            if channel.recv_ready():
                out.append(channel.recv(1024).decode())
            if channel.recv_stderr_ready():
                err.append(channel.recv_stderr(1024).decode())
                
        # 讀取剩餘數據
        while channel.recv_ready():
            out.append(channel.recv(1024).decode())
        while channel.recv_stderr_ready():
            err.append(channel.recv_stderr(1024).decode())
            
        out_str = "".join(out).strip()
        err_str = "".join(err).strip()
        
        print(f"✓ NAS 索引重建完成 (Exit Code: {channel.recv_exit_status()})")
        if out_str:
            print("  Stdout:", out_str)
        if err_str:
            print("  Stderr:", err_str)
        return 0
            
    except Exception as e:
        print(f"❌ 同步失敗: {type(e).__name__}: {e}")
        return 1
    finally:
        if transport:
            transport.close()

if __name__ == "__main__":
    raise SystemExit(main())
