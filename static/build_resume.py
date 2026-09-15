#!/usr/bin/env python3
"""
build_resume.py — 動態編譯頂級企業級 HR/獵頭認可之專業履歷 (static/resume.html)
標準：依據 Laszlo Bock《Work Rules!》與 Google XYZ 成果量化公式。
具備：
1. 雙模式（商用極簡白底標準版 + 現代深色科技版）
2. 完美相容 A4 紙本列印與另存 PDF (@media print 最佳化)
3. 嚴格商業對位：AI 應用架構師 & 技術專案經理 (年薪 80~95 萬定位)
4. 零自嗨詞彙（全面抹除 Persona, hobbyist 標籤）
"""
import json
import os
from pathlib import Path

WIKI_DIR = Path(__file__).resolve().parent.parent
JSON_PATH = WIKI_DIR.parent / "_non_github_local" / "Resume_Agent" / "resume.json"
HTML_OUT_PATH = WIKI_DIR / "static" / "resume.html"

def load_data():
    if not JSON_PATH.exists():
        alt_path = WIKI_DIR / "resume.json"
        if alt_path.exists():
            with alt_path.open(encoding="utf-8") as f:
                return json.load(f)
        raise FileNotFoundError(f"找不到 resume.json：{JSON_PATH}")
    with JSON_PATH.open(encoding="utf-8") as f:
        return json.load(f)

def generate_html(data):
    basics = data["basics"]
    skills = data["skills"]
    experience = data["experience"]
    education = data["education"]
    projects = data["projects"]
    
    # 經歷渲染
    exp_html = ""
    for exp in experience:
        exp_html += f"""
        <div class="timeline-item">
          <div class="item-header">
            <div class="company-role">
              <span class="role-title">{exp["title"]}</span>
              <span class="company-name">{exp["company"]}</span>
            </div>
            <span class="period">{exp["period"]}</span>
          </div>
          <p class="description">{exp["description"]}</p>
        </div>"""

    # 學歷證照渲染
    edu_html = ""
    for edu in education:
        edu_html += f"""
        <div class="edu-item">
          <div class="edu-bullet"></div>
          <div class="edu-text">{edu}</div>
        </div>"""

    # 核心技能分組
    skill_groups = {
        "🤖 AI 架構與檢索增強 (RAG)": [s for s in skills if any(k in s for k in ["AI", "RAG", "Vector", "Embedding", "檢索", "Local AI"])],
        "🐍 軟體工程與自動化開發": [s for s in skills if any(k in s for k in ["Python", "FastAPI", "AsyncIO", "Browser", "Playwright", "Camoufox"])],
        "🐳 系統運維、CI/CD 與防禦性架構": [s for s in skills if any(k in s for k in ["DevOps", "Docker", "Actions", "Cron", "架構", "熔斷", "防禦"])],
        "📊 專案管理、流程工程與敏捷交付": [s for s in skills if any(k in s for k in ["APMP", "專案管理", "Agile", "Scrum", "SOP", "XYZ", "流程"])]
    }
    
    skills_cards_html = ""
    for group_name, s_list in skill_groups.items():
        tags = "".join(f'<span class="skill-tag">{s}</span>' for s in s_list)
        skills_cards_html += f"""
        <div class="skill-group-card">
          <h4 class="skill-group-title">{group_name}</h4>
          <div class="skill-tags-wrapper">{tags}</div>
        </div>"""

    # 旗艦專案渲染 (Google XYZ 嚴格拆解)
    proj_html = ""
    for proj in projects:
        proj_html += f"""
        <div class="project-card">
          <div class="project-header">
            <div class="project-title">{proj["name"]}</div>
            <span class="project-role">{proj["role"]}</span>
          </div>
          <div class="project-body">{proj["description"]}</div>
        </div>"""

    return f"""<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{basics["name"]} — {basics["title"]}</title>
<meta name="description" content="{basics["summary"][:160]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+TC:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #ffffff;
    --surface: #f8fafc;
    --card: #ffffff;
    --border: #e2e8f0;
    --border-strong: #cbd5e1;
    --text-main: #0f172a;
    --text-muted: #475569;
    --text-light: #64748b;
    --primary: #2563eb;
    --primary-dark: #1d4ed8;
    --accent: #059669;
    --tag-bg: #f1f5f9;
    --tag-text: #334155;
    --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
  }}

  body.dark-mode {{
    --bg: #0f172a;
    --surface: #1e293b;
    --card: #1e293b;
    --border: #334155;
    --border-strong: #475569;
    --text-main: #f8fafc;
    --text-muted: #94a3b8;
    --text-light: #cbd5e1;
    --primary: #38bdf8;
    --primary-dark: #0284c7;
    --accent: #34d399;
    --tag-bg: #334155;
    --tag-text: #e2e8f0;
    --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
  }}

  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    font-family: 'Inter', 'Noto Sans TC', -apple-system, sans-serif;
    background: var(--bg);
    color: var(--text-main);
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
    transition: background 0.2s, color 0.2s;
  }}

  /* 控制工具列 */
  .action-bar {{
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    padding: 0.6rem 1.5rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    position: sticky;
    top: 0;
    z-index: 100;
  }}
  .action-links a {{
    color: var(--primary);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    margin-right: 1.2rem;
  }}
  .action-btns {{ display: flex; gap: 0.6rem; }}
  .btn {{
    padding: 0.45rem 0.9rem;
    border-radius: 6px;
    font-size: 0.82rem;
    font-weight: 600;
    cursor: pointer;
    border: 1px solid var(--border-strong);
    background: var(--card);
    color: var(--text-main);
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
  }}
  .btn-primary {{
    background: var(--primary);
    color: #ffffff;
    border-color: var(--primary);
  }}
  .btn-primary:hover {{ background: var(--primary-dark); }}

  /* A4 版型容器 */
  .resume-container {{
    max-width: 960px;
    margin: 2rem auto;
    padding: 0 1.5rem;
  }}

  /* 表頭與聯絡資訊 */
  .header-card {{
    border-bottom: 2px solid var(--border-strong);
    padding-bottom: 1.5rem;
    margin-bottom: 2rem;
  }}
  .name-block {{
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    flex-wrap: wrap;
    gap: 1rem;
    margin-bottom: 0.75rem;
  }}
  .candidate-name {{
    font-size: 2.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: var(--text-main);
  }}
  .candidate-title {{
    font-size: 1.2rem;
    color: var(--primary);
    font-weight: 600;
    margin-top: 0.2rem;
  }}
  .contact-grid {{
    display: flex;
    flex-wrap: wrap;
    gap: 1rem 1.5rem;
    font-size: 0.88rem;
    color: var(--text-muted);
    margin-top: 0.8rem;
  }}
  .contact-item {{ display: flex; align-items: center; gap: 0.35rem; }}
  .contact-item a {{ color: var(--primary); text-decoration: none; }}

  /* 個人簡介 */
  .summary-box {{
    background: var(--surface);
    border-left: 4px solid var(--primary);
    padding: 1rem 1.25rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.92rem;
    line-height: 1.65;
    color: var(--text-muted);
    margin-bottom: 2.2rem;
  }}

  /* 區塊標題 */
  .section {{
    margin-bottom: 2.2rem;
  }}
  .section-title {{
    font-size: 1.15rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-main);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.4rem;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }}

  /* 專業技能組件 */
  .skills-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 1rem;
  }}
  .skill-group-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1rem;
  }}
  .skill-group-title {{
    font-size: 0.88rem;
    font-weight: 600;
    margin-bottom: 0.6rem;
    color: var(--text-main);
  }}
  .skill-tags-wrapper {{
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
  }}
  .skill-tag {{
    font-size: 0.76rem;
    background: var(--tag-bg);
    color: var(--tag-text);
    padding: 0.2rem 0.55rem;
    border-radius: 4px;
    font-weight: 500;
  }}

  /* 經歷時間線 */
  .timeline {{
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }}
  .timeline-item {{
    border-left: 2px solid var(--border-strong);
    padding-left: 1.2rem;
    position: relative;
  }}
  .timeline-item::before {{
    content: '';
    position: absolute;
    left: -6px;
    top: 5px;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    background: var(--primary);
  }}
  .item-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    flex-wrap: wrap;
    margin-bottom: 0.35rem;
  }}
  .role-title {{
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--text-main);
    margin-right: 0.5rem;
  }}
  .company-name {{
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--text-muted);
  }}
  .period {{
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--primary);
    font-family: 'JetBrains Mono', monospace;
  }}
  .description {{
    font-size: 0.88rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin-top: 0.3rem;
  }}

  /* 專案卡片 */
  .projects-container {{
    display: flex;
    flex-direction: column;
    gap: 1.2rem;
  }}
  .project-card {{
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem 1.25rem;
  }}
  .project-header {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }}
  .project-title {{
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-main);
  }}
  .project-role {{
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--primary);
    background: var(--tag-bg);
    padding: 0.15rem 0.5rem;
    border-radius: 4px;
    border: 1px solid var(--border);
  }}
  .project-body {{
    font-size: 0.86rem;
    color: var(--text-muted);
    line-height: 1.55;
  }}

  /* 學歷與證照 */
  .edu-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 0.75rem;
  }}
  .edu-item {{
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: var(--surface);
    padding: 0.6rem 0.9rem;
    border-radius: 6px;
    border: 1px solid var(--border);
  }}
  .edu-bullet {{
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent);
  }}
  .edu-text {{
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--text-main);
  }}

  /* 列印專用 CSS (@media print) */
  @media print {{
    .action-bar {{ display: none !important; }}
    body {{ background: #ffffff !important; color: #000000 !important; font-size: 12px !important; }}
    .resume-container {{ max-width: 100% !important; margin: 0 !important; padding: 0 !important; }}
    .header-card {{ border-bottom: 2px solid #000000 !important; margin-bottom: 1rem !important; padding-bottom: 0.5rem !important; }}
    .candidate-name {{ font-size: 1.8rem !important; color: #000000 !important; }}
    .candidate-title {{ color: #1d4ed8 !important; font-size: 1.1rem !important; }}
    .summary-box {{ background: #f8fafc !important; border-left: 3px solid #1d4ed8 !important; color: #1e293b !important; padding: 0.6rem !important; margin-bottom: 1rem !important; }}
    .section {{ margin-bottom: 1.2rem !important; page-break-inside: avoid; }}
    .section-title {{ border-bottom: 1px solid #94a3b8 !important; font-size: 1rem !important; margin-bottom: 0.6rem !important; }}
    .skill-group-card, .project-card, .edu-item {{ background: #ffffff !important; border: 1px solid #cbd5e1 !important; padding: 0.6rem !important; }}
    .skill-tag {{ background: #f1f5f9 !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; }}
    .timeline-item {{ border-left: 2px solid #000000 !important; padding-left: 0.8rem !important; }}
    .timeline-item::before {{ background: #000000 !important; }}
  }}
</style>
</head>
<body>

<div class="action-bar">
  <div class="action-links">
    <a href="../index.html">Wiki 首頁</a>
    <a href="../kanban.html">即時看板</a>
    <a href="ecom_tools.html">⚡ 電商工具箱</a>
  </div>
  <div class="action-btns">
    <button class="btn" onclick="toggleTheme()">🌓 切換深淺模式</button>
    <button class="btn btn-primary" onclick="window.print()">🖨️ 列印 / 另存 PDF</button>
  </div>
</div>

<div class="resume-container">

  <!-- 表頭與核心定位 -->
  <header class="header-card">
    <div class="name-block">
      <div>
        <h1 class="candidate-name">{basics["name"]}</h1>
        <div class="candidate-title">{basics["title"]}</div>
      </div>
    </div>
    
    <div class="contact-grid">
      <div class="contact-item">📍 {basics["location"]}</div>
      <div class="contact-item">📞 <a href="tel:{basics["phone"]}">{basics["phone"]}</a></div>
      <div class="contact-item">✉️ <a href="mailto:{basics["email"]}">{basics["email"]}</a></div>
      <div class="contact-item">🔗 <a href="https://github.com/Jnocode" target="_blank">GitHub: Jnocode</a></div>
      <div class="contact-item">💼 <a href="https://linkedin.com/in/jun-jiang-tw" target="_blank">LinkedIn Profile</a></div>
    </div>
  </header>

  <!-- 執行摘要 (Elevator Pitch) -->
  <div class="summary-box">
    {basics["summary"]}
  </div>

  <!-- 專業核心技能矩陣 -->
  <section class="section">
    <h3 class="section-title">🛠️ 專業核心能力矩陣 (Core Competencies)</h3>
    <div class="skills-grid">
      {skills_cards_html}
    </div>
  </section>

  <!-- 專業經歷 -->
  <section class="section">
    <h3 class="section-title">💼 專業工作經歷 (Professional Experience)</h3>
    <div class="timeline">
      {exp_html}
    </div>
  </section>

  <!-- 旗艦專案實績 (Google XYZ 量化) -->
  <section class="section">
    <h3 class="section-title">🚀 旗艦研發專案實績 (Selected Projects & Impact)</h3>
    <div class="projects-container">
      {proj_html}
    </div>
  </section>

  <!-- 學歷與專業認證 -->
  <section class="section">
    <h3 class="section-title">🎓 學歷背景與國際專業證照 (Education & Certifications)</h3>
    <div class="edu-grid">
      {edu_html}
    </div>
  </section>

</div>

<script>
function toggleTheme() {{
  document.body.classList.toggle('dark-mode');
  localStorage.setItem('resume_theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
}}
if (localStorage.getItem('resume_theme') === 'dark') {{
  document.body.classList.add('dark-mode');
}}
</script>
</body>
</html>
"""

def main():
    print("⏳ 讀取 resume.json 資料...")
    data = load_data()
    print("⚙️ 開始編譯正式 HR-Grade HTML 履歷...")
    html = generate_html(data)
    print(f"💾 寫入 HTML 至：{HTML_OUT_PATH}")
    HTML_OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    HTML_OUT_PATH.write_text(html, encoding="utf-8")
    print("✓ 正式企業級履歷編譯成功！")

if __name__ == "__main__":
    main()
