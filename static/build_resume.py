#!/usr/bin/env python3
"""
build_resume.py — 讀取 resume.json，動態編譯生成 HTML 履歷 (static/resume.html)
"""
import json
import os
from pathlib import Path

# 定義路徑
WIKI_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = WIKI_DIR.parent / "_non_github_local" / "Resume_Agent" / "resume.json"
HTML_OUT_PATH = WIKI_DIR / "static" / "resume.html"

def load_data():
    if not JSON_PATH.exists():
        # 備用路徑
        alt_path = WIKI_DIR / "resume.json"
        if alt_path.exists():
            with alt_path.open(encoding="utf-8") as f:
                return json.load(f)
        raise FileNotFoundError(f"找不到 resume.json：{JSON_PATH}")
    with JSON_PATH.open(encoding="utf-8") as f:
        return json.load(f)

def generate_html(data):
    # 提取欄位
    basics = data["basics"]
    skills = data["skills"]
    experience = data["experience"]
    education = data["education"]
    projects = data["projects"]
    
    # 渲染經歷 (Timeline)
    exp_html = ""
    for exp in experience:
        exp_html += f"""
    <div class="tl-item">
      <div class="tl-year">{exp["period"]}</div>
      <div class="tl-title">{exp["company"]} · {exp["title"]}</div>
      <div class="tl-desc">{exp["description"]}</div>
    </div>"""

    # 渲染學歷 (Education)
    edu_html = ""
    for edu in education:
        edu_html += f"""
    <div class="tl-item">
      <div class="tl-title">{edu}</div>
    </div>"""

    # 渲染精選亮點 (Home Highlights)
    highlights_html = ""
    icons = ["🧠", "🎙", "📈", "🎮", "🛠️"]
    for i, proj in enumerate(projects[:4]):
        icon = icons[i % len(icons)]
        highlights_html += f"""
    <div class="proj-card" style="cursor:pointer" onclick="switchSection('projects')">
      <div class="p-icon">{icon}</div>
      <div class="p-title">{proj["name"]}</div>
      <div class="p-desc">{proj["description"][:130]}...</div>
      <div class="p-meta"><span class="p-status status-done">✅ active</span></div>
    </div>"""

    # 渲染作品集頁面 (Projects detail)
    proj_detail_html = ""
    for i, proj in enumerate(projects):
        icon = icons[i % len(icons)]
        proj_detail_html += f"""
    <div class="proj-card">
      <div class="p-icon">{icon}</div>
      <div class="p-title">{proj["name"]}</div>
      <div class="p-desc">{proj["description"]}</div>
      <div class="p-meta">
        <span class="p-status status-done">{proj["role"]}</span>
      </div>
    </div>"""

    # 渲染技術棧卡片
    # 我們將 skills 分類成幾組以利卡片化呈現
    skills_chunk = ""
    for skill in skills:
        skills_chunk += f"<span>{skill}</span>"
        
    skills_html = f"""
    <div class="card">
      <div class="ctitle">🛠️ 專業核心能力 (Core Skills)</div>
      <div class="ctags" style="margin-top:0.4rem">
        {skills_chunk}
      </div>
    </div>"""

    # 完整單頁 SPA 範本
    html_template = f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{basics["name"]} Persona — AI Agent & RAG Specialist</title>
<meta name="description" content="{basics["summary"][:150]}...">
<!-- Open Graph -->
<meta property="og:title" content="{basics["name"]} — {basics["title"]}">
<meta property="og:description" content="{basics["summary"][:120]}...">
<meta property="og:type" content="website">
<meta property="og:locale" content="zh_TW">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Noto+Sans+TC:wght@300;400;500;700&display=swap" rel="stylesheet">
<style>
/* =========== SYSTEM =========== */
*,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg:#08090a;
  --surface:#0f1011;
  --card:#161b22;
  --card-hover:#1c2333;
  --border:rgba(255,255,255,0.06);
  --border-strong:rgba(255,255,255,0.10);
  --text-primary:#f0f2f5;
  --text-secondary:#b0b8c4;
  --text-tertiary:#8a8f98;
  --text-muted:#62666d;
  --accent-blue:#58a6ff;
  --accent-purple:#bc8cff;
  --accent-green:#3fb950;
  --accent-pink:#ff7b72;
  --accent-orange:#d29922;
  --accent-cyan:#79c0ff;
  --brand:#5e6ad2;
  --brand-hover:#7170ff;
  --radius:8px;
  --radius-lg:12px;
  --shadow-card:0 0 0 1px var(--border),0 4px 12px rgba(0,0,0,0.15);
  --transition:all 0.2s cubic-bezier(0.4,0,0.2,1);
}}
html{{scroll-behavior:smooth;scroll-padding-top:64px}}
body{{
  font-family:'Inter','Noto Sans TC',-apple-system,BlinkMacSystemFont,sans-serif;
  background:var(--bg);
  color:var(--text-primary);
  line-height:1.7;
  -webkit-font-smoothing:antialiased;
}}
a{{color:var(--accent-blue);text-decoration:none;transition:var(--transition)}}
a:hover{{color:var(--accent-cyan)}}

/* =========== NAVBAR =========== */
.navbar{{
  position:fixed;top:0;left:0;right:0;z-index:1000;
  background:rgba(8,9,10,0.85);backdrop-filter:blur(16px);
  border-bottom:1px solid var(--border);
  height:56px;display:flex;align-items:center;
  padding:0 1.5rem;
}}
.nav-inner{{
  max-width:1100px;margin:0 auto;width:100%;
  display:flex;align-items:center;justify-content:space-between;
}}
.nav-logo{{
  font-size:1.1rem;font-weight:600;
  background:linear-gradient(135deg,var(--accent-blue),var(--accent-purple));
  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
  cursor:pointer;
}}
.nav-links{{display:flex;gap:0.5rem;align-items:center}}
.nav-links a{{
  color:var(--text-tertiary);font-size:0.82rem;font-weight:500;
  padding:0.35rem 0.7rem;border-radius:6px;cursor:pointer;
  transition:var(--transition);
}}
.nav-links a:hover, .nav-links a.active{{
  color:var(--text-primary);background:rgba(255,255,255,0.04);
}}

/* =========== MAIN =========== */
main{{max-width:1100px;margin:0 auto;padding:72px 1.5rem 3rem}}
.section{{display:none;animation:fadeIn 0.3s ease}}
.section.active{{display:block}}
@keyframes fadeIn{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:translateY(0)}}}}

/* =========== HERO =========== */
.hero{{padding:4rem 0 3rem}}
.hero-badge{{
  display:inline-flex;align-items:center;gap:0.4rem;
  font-size:0.72rem;font-weight:500;color:var(--accent-blue);
  background:rgba(88,166,255,0.08);border:1px solid rgba(88,166,255,0.15);
  padding:0.25rem 0.65rem;border-radius:20px;margin-bottom:1.5rem;
}}
.hero h1{{
  font-size:3rem;font-weight:700;line-height:1.15;
  margin-bottom:1rem;
}}
.hero h1 .g1{{color:var(--accent-blue)}}
.hero h1 .g3{{color:var(--accent-purple)}}
.hero h1 .g4{{color:var(--accent-green)}}
.hero .subtitle{{
  font-size:1.05rem;color:var(--text-tertiary);max-width:800px;
  line-height:1.7;margin-bottom:2rem;
}}
.hero-cta{{display:flex;gap:0.75rem;flex-wrap:wrap}}
.hero-cta .btn{{
  display:inline-flex;align-items:center;
  padding:0.6rem 1.2rem;border-radius:var(--radius);font-size:0.88rem;font-weight:500;
  cursor:pointer;transition:var(--transition);border:none;
}}
.btn-primary{{background:var(--brand);color:#fff}}
.btn-primary:hover{{background:var(--brand-hover);transform:translateY(-1px)}}
.btn-ghost{{background:rgba(255,255,255,0.03);color:var(--text-secondary);border:1px solid var(--border-strong)}}
.btn-ghost:hover{{background:rgba(255,255,255,0.06);color:var(--text-primary)}}

.hero-tags{{display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:2.5rem}}
.hero-tags span{{
  font-size:0.78rem;font-weight:500;padding:0.25rem 0.75rem;
  border-radius:20px;border:1px solid var(--border-strong);
  color:var(--text-secondary);background:rgba(255,255,255,0.02);
}}

/* =========== TIMELINE & CARDS =========== */
.section-header{{margin-bottom:2rem;padding-bottom:1rem;border-bottom:1px solid var(--border)}}
.section-header h2{{font-size:1.5rem;font-weight:600}}
.section-header p{{color:var(--text-tertiary);font-size:0.9rem;margin-top:0.3rem}}

.card-grid-2{{display:grid;gap:0.75rem;grid-template-columns:repeat(auto-fill,minmax(320px,1fr))}}
.card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius);padding:1.25rem}}
.ctags{{display:flex;gap:0.4rem;flex-wrap:wrap;margin-top:0.4rem}}
.ctags span{{
  font-size:0.75rem;padding:0.2rem 0.6rem;border-radius:4px;
  background:rgba(255,255,255,0.04);border:1px solid var(--border);
  color:var(--text-secondary);
}}

.timeline{{position:relative;padding-left:2rem}}
.timeline::before{{
  content:'';position:absolute;left:7px;top:8px;bottom:8px;
  width:1px;background:var(--border-strong);
}}
.tl-item{{position:relative;margin-bottom:1.5rem;padding-left:1.5rem}}
.tl-item::before{{
  content:'';position:absolute;left:-1.65rem;top:0.5rem;
  width:9px;height:9px;border-radius:50%;
  background:var(--accent-blue);border:2px solid var(--bg);
}}
.tl-year{{font-size:0.72rem;font-weight:600;color:var(--accent-blue);margin-bottom:0.2rem}}
.tl-title{{font-size:0.95rem;font-weight:600}}
.tl-desc{{font-size:0.85rem;color:var(--text-tertiary);margin-top:0.2rem}}

.proj-card{{background:var(--card);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1.25rem;transition:var(--transition)}}
.proj-card:hover{{border-color:var(--border-strong);background:var(--card-hover)}}
.proj-card .p-icon{{width:36px;height:36px;border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:1.1rem;margin-bottom:0.75rem;background:rgba(255,255,255,0.04);border:1px solid var(--border)}}
.proj-card .p-title{{font-size:1rem;font-weight:600;margin-bottom:0.25rem}}
.proj-card .p-desc{{font-size:0.82rem;color:var(--text-tertiary);margin-bottom:0.6rem;line-height:1.5}}
.proj-card .p-meta{{display:flex;gap:0.5rem;align-items:center}}
.proj-card .p-status{{font-size:0.68rem;font-weight:500;padding:0.1rem 0.5rem;border-radius:4px;background:rgba(88,166,255,0.12);color:var(--accent-blue)}}

footer{{margin-top:4rem;padding-top:1.5rem;border-top:1px solid var(--border);font-size:0.78rem;color:var(--text-muted);display:flex;justify-content:between}}
</style>
</head>
<body>

<nav class="navbar">
  <div class="nav-inner">
    <div class="nav-logo" onclick="switchSection('home')">{basics["name"]}<span>.profile</span></div>
    <div class="nav-links">
      <a class="active" data-section="home" onclick="switchSection('home')">🏠 首頁</a>
      <a data-section="resume" onclick="switchSection('resume')">📄 履歷</a>
      <a data-section="projects" onclick="switchSection('projects')">📂 作品集</a>
    </div>
  </div>
</nav>

<main>

<!-- ========== HOME ========== -->
<section id="home" class="section active">
  <div class="hero">
    <div class="hero-badge">⚡ AI Agent & RAG Developer · Python Expert</div>
    <h1>
      <span class="g1">{basics["name"].split()[0]}</span> <span class="g3">{basics["name"].split()[-1] if len(basics["name"].split())>1 else ""}</span><br>
      <span class="g4">AI Agent</span><span style="color:var(--text-tertiary)"> × </span><span class="g1">RAG</span>
    </h1>
    <div class="subtitle">{basics["summary"]}</div>
    <div class="hero-tags">
      <span>🐍 Python (AsyncIO)</span>
      <span>🤖 AI Agent</span>
      <span>🧠 RAG (ANN+FTS5)</span>
      <span>🎙 Podcast Automation</span>
      <span>🔧 CDP Browser Automation</span>
      <span>🐳 Docker Compose</span>
    </div>
    <div class="hero-cta">
      <button class="btn btn-primary" onclick="switchSection('resume')">📄 看履歷</button>
      <button class="btn btn-ghost" onclick="switchSection('projects')">📂 看作品集</button>
    </div>
  </div>

  <div class="section-header"><h2>🔥 精選研案亮點</h2><p>自主研發代表作</p></div>
  <div class="card-grid-2">
    {highlights_html}
  </div>
</section>

<!-- ========== RESUME ========== -->
<section id="resume" class="section">
  <div class="section-header">
    <h2>📄 經歷與技術棧</h2>
    <p>{basics["title"]} · 聯絡方式：{basics["email"]}</p>
  </div>

  <div class="section-header" style="border-bottom-color:transparent;margin-bottom:1rem"><h3 style="font-size:1.1rem">💼 工作經歷</h3></div>
  <div class="timeline" style="margin-bottom:2.5rem">
    {exp_html}
  </div>

  <div class="section-header" style="border-bottom-color:transparent;margin-bottom:1rem"><h3 style="font-size:1.1rem">🎓 教育與證照</h3></div>
  <div class="timeline" style="margin-bottom:2.5rem">
    {edu_html}
  </div>

  <div class="section-header" style="border-bottom-color:transparent;margin-bottom:1rem"><h3 style="font-size:1.1rem">🛠️ 技術實力</h3></div>
  {skills_html}
</section>

<!-- ========== PROJECTS ========== -->
<section id="projects" class="section">
  <div class="section-header">
    <h2>📂 所有開發專案</h2>
    <p>從 0 到 1 的實踐</p>
  </div>
  <div class="card-grid-2">
    {proj_detail_html}
  </div>
</section>

<footer>
  <span>Jnocode/wiki · 個人 NAS 靜態託管</span>
  <span>Powered by Python Build Engine &amp; Hermes</span>
</footer>

</main>

<script>
function switchSection(name) {{
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-links a').forEach(a => a.classList.remove('active'));
  const section = document.getElementById(name);
  if (section) section.classList.add('active');
  const link = document.querySelector(`.nav-links a[data-section="${{name}}"]`);
  if (link) link.classList.add('active');
  window.scrollTo({{top: 0, behavior: 'smooth'}});
}}
</script>
</body>
</html>
"""
    return html_template

def main():
    print("⏳ 讀取 resume.json 資料...")
    data = load_data()
    print("⚙️ 開始編譯 HTML 履歷...")
    html = generate_html(data)
    print(f"💾 寫入 HTML 至：{HTML_OUT_PATH}")
    HTML_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT_PATH.write_text(html, encoding="utf-8")
    print("✓ HTML 履歷編譯成功！")

if __name__ == "__main__":
    main()
