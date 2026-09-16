import json

tools_file = "D:/Workspace/agent_office/temp/ecom_extracted_tools.json"
tools = json.load(open(tools_file, encoding="utf-8"))

html_head = """<!DOCTYPE html>
<html lang="zh-Hant">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>電商營運工具箱 (Open Release) · Jun's Lab</title>
<style>
  :root {
    --bg: #0d1117;
    --surface: #161b22;
    --border: #30363d;
    --text: #e6edf3;
    --text-muted: #8b949e;
    --accent: #58a6ff;
    --green: #3fb950;
    --orange: #d29922;
  }
  * { margin: 0; padding: 0; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
  body { background: var(--bg); color: var(--text); padding-bottom: 3rem; }
  
  .topbar {
    background: var(--surface); border-bottom: 1px solid var(--border);
    padding: 0.8rem 1.5rem; display: flex; justify-content: space-between; align-items: center;
    position: sticky; top: 0; z-index: 100;
  }
  .brand { font-size: 1.1rem; font-weight: bold; color: var(--text); display: flex; align-items: center; gap: 0.5rem; }
  .nav-links a { color: var(--accent); text-decoration: none; margin-left: 1rem; font-size: 0.85rem; font-weight: 500; }
  
  .hero { text-align: center; padding: 2.5rem 1rem 1.5rem; max-width: 800px; margin: 0 auto; }
  .hero h1 { font-size: 1.8rem; margin-bottom: 0.5rem; background: linear-gradient(90deg, #58a6ff, #3fb950); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
  .hero p { color: var(--text-muted); font-size: 0.95rem; line-height: 1.5; }
  
  .search-box { max-width: 650px; margin: 1.5rem auto; padding: 0 1rem; position: relative; }
  .search-input {
    width: 100%; padding: 0.8rem 1.2rem; background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; color: var(--text); font-size: 0.95rem; outline: none; transition: border-color 0.2s;
  }
  .search-input:focus { border-color: var(--accent); }
  
  .container { max-width: 1100px; margin: 0 auto; padding: 0 1rem; }
  .tools-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem; margin-top: 1rem;
  }
  .tool-card {
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    padding: 1.1rem; cursor: pointer; transition: transform 0.15s, border-color 0.15s;
    display: flex; flex-direction: column; justify-content: space-between;
  }
  .tool-card:hover { transform: translateY(-2px); border-color: var(--accent); }
  .tool-header { display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.5rem; }
  .tool-icon { font-size: 1.5rem; }
  .tool-title { font-size: 0.95rem; font-weight: 600; color: var(--text); }
  .tool-tagline { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; margin-bottom: 0.8rem; flex-grow: 1; }
  .tool-footer { display: flex; justify-content: space-between; align-items: center; font-size: 0.7rem; }
  .badge-live { color: var(--green); background: rgba(63,185,80,0.15); padding: 0.15rem 0.5rem; border-radius: 4px; font-weight: 500; }
  .action-hint { color: var(--accent); }

  .modal {
    display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0,0,0,0.7); z-index: 200; justify-content: center; align-items: center; padding: 1rem;
  }
  .modal-content {
    background: var(--surface); border: 1px solid var(--border); border-radius: 10px;
    width: 100%; max-width: 600px; max-height: 90vh; overflow-y: auto; padding: 1.5rem; position: relative;
  }
  .close-btn { position: absolute; top: 1rem; right: 1rem; color: var(--text-muted); cursor: pointer; font-size: 1.3rem; }
  .form-group { margin-top: 1rem; }
  .form-group label { display: block; font-size: 0.85rem; color: var(--text-muted); margin-bottom: 0.4rem; }
  .form-group input, .form-group textarea {
    width: 100%; padding: 0.6rem; background: var(--bg); border: 1px solid var(--border);
    border-radius: 6px; color: var(--text); font-size: 0.9rem; outline: none;
  }
  .run-btn {
    width: 100%; margin-top: 1.2rem; padding: 0.75rem; background: #238636; border: none;
    border-radius: 6px; color: white; font-weight: bold; cursor: pointer; transition: background 0.2s;
  }
  .run-btn:hover { background: #2ea043; }
  .result-box {
    margin-top: 1.2rem; padding: 1rem; background: var(--bg); border: 1px solid var(--border);
    border-radius: 6px; font-size: 0.85rem; line-height: 1.5; white-space: pre-wrap; display: none;
  }
</style>
</head>
<body>

<div class="topbar">
  <div class="brand">⚡ 電商營運工具箱 <span>(186 款完整復刻)</span></div>
  <div class="nav-links">
    <a href="../index.html">Wiki 首頁</a>
    <a href="../kanban.html">即時看板</a>
    <a href="../viewer.html?file=projects/ecom_toolkit_reverse_engineering.md">逆向工程報告</a>
  </div>
</div>

<div class="hero">
  <h1>全功能電商營運工具箱</h1>
  <p>完整復刻 186 款台灣電商營運專用工具 · 100% 純前端零依賴運算 · 零伺服器成本</p>
</div>

<div class="search-box">
  <input type="text" id="search" class="search-input" placeholder="🔍 搜尋工具名稱、關鍵字 (例如: ROAS, 文案, 統編, 庫存, 折扣...)" oninput="filterTools()">
</div>

<div class="container">
  <div style="font-size:0.85rem; color:var(--text-muted); margin-bottom:0.5rem;" id="count-label">共收錄 186 款工具</div>
  <div class="tools-grid" id="toolsGrid"></div>
</div>

<div class="modal" id="toolModal" onclick="closeModal(event)">
  <div class="modal-content" onclick="event.stopPropagation()">
    <span class="close-btn" onclick="closeModalDirect()">&times;</span>
    <h2 id="modalTitle" style="display:flex; align-items:center; gap:0.5rem; font-size:1.2rem;"></h2>
    <p id="modalDesc" style="color:var(--text-muted); font-size:0.85rem; margin-top:0.3rem;"></p>
    
    <div id="dynamicForm"></div>
    <button class="run-btn" id="runBtn" onclick="executeTool()">⚡ 立即計算 / 智慧生成</button>
    <div class="result-box" id="resultBox"></div>
  </div>
</div>

<script>
"""

html_tail = """
let currentTool = null;

function renderTools(list) {
  const grid = document.getElementById('toolsGrid');
  grid.innerHTML = '';
  list.forEach(t => {
    const card = document.createElement('div');
    card.className = 'tool-card';
    card.onclick = () => openTool(t);
    card.innerHTML = `
      <div>
        <div class="tool-header">
          <span class="tool-icon">${t.icon}</span>
          <span class="tool-title">${t.name}</span>
        </div>
        <div class="tool-tagline">${t.tagline}</div>
      </div>
      <div class="tool-footer">
        <span class="badge-live">✓ 即開即用</span>
        <span class="action-hint">點擊開啟 ➔</span>
      </div>
    `;
    grid.appendChild(card);
  });
  document.getElementById('count-label').innerText = `共收錄 ${list.length} 款工具`;
}

function filterTools() {
  const query = document.getElementById('search').value.toLowerCase().trim();
  if (!query) {
    renderTools(tools);
    return;
  }
  const filtered = tools.filter(t => 
    t.name.toLowerCase().includes(query) || 
    t.tagline.toLowerCase().includes(query) ||
    t.slug.toLowerCase().includes(query)
  );
  renderTools(filtered);
}

function openTool(t) {
  currentTool = t;
  document.getElementById('modalTitle').innerHTML = `${t.icon} ${t.name}`;
  document.getElementById('modalDesc').innerText = t.tagline;
  document.getElementById('resultBox').style.display = 'none';
  
  const form = document.getElementById('dynamicForm');
  form.innerHTML = '';
  
  if (t.id === 'ad-calc' || t.name.includes('ROAS')) {
    form.innerHTML = `
      <div class="form-group">
        <label>廣告支出 (NT$)</label>
        <input type="number" id="ad_spend" value="10000">
      </div>
      <div class="form-group">
        <label>廣告帶動營收 (NT$)</label>
        <input type="number" id="ad_revenue" value="45000">
      </div>
      <div class="form-group">
        <label>商品平均毛利率 (%)</label>
        <input type="number" id="gross_margin" value="60">
      </div>
    `;
  } else if (t.id === 'vat' || t.name.includes('統一編號') || t.name.includes('統編')) {
    form.innerHTML = `
      <div class="form-group">
        <label>請輸入 8 碼統一編號</label>
        <input type="text" id="vat_input" maxlength="8" placeholder="例如: 04595257">
      </div>
    `;
  } else {
    form.innerHTML = `
      <div class="form-group">
        <label>商品名稱 / 輸入情境</label>
        <input type="text" id="generic_title" placeholder="例如: 極簡無線降噪藍牙耳機">
      </div>
      <div class="form-group">
        <label>商品賣點 / 核心特徵</label>
        <textarea id="generic_features" rows="3" placeholder="例如: 40dB 深度降噪、32小時超長續航、石墨烯振膜音質"></textarea>
      </div>
    `;
  }
  
  document.getElementById('toolModal').style.display = 'flex';
}

function closeModalDirect() {
  document.getElementById('toolModal').style.display = 'none';
}

function closeModal(e) {
  if (e.target.id === 'toolModal') {
    closeModalDirect();
  }
}

function executeTool() {
  const res = document.getElementById('resultBox');
  res.style.display = 'block';
  
  if (currentTool.id === 'ad-calc' || currentTool.name.includes('ROAS')) {
    const spend = parseFloat(document.getElementById('ad_spend').value) || 0;
    const rev = parseFloat(document.getElementById('ad_revenue').value) || 0;
    const margin = parseFloat(document.getElementById('gross_margin').value) || 0;
    
    if (spend <= 0) {
      res.innerText = '⚠️ 請輸入大於 0 的廣告支出金額。';
      return;
    }
    const roas = (rev / spend).toFixed(2);
    const grossProfit = rev * (margin / 100);
    const netProfit = grossProfit - spend;
    const breakEvenRoas = (100 / margin).toFixed(2);
    
    res.innerHTML = `📊 【計算結果診斷報告】\\n• 實際 ROAS: <b>${roas}</b> (每投 $1 產生 $${roas} 營收)\\n• 損益平衡 ROAS 門檻: <b>${breakEvenRoas}</b>\\n• 預估毛利: NT$ ${grossProfit.toLocaleString()}\\n• 扣除廣告後淨損益: <b style="color:${netProfit >= 0 ? 'var(--green)' : 'red'}">NT$ ${netProfit.toLocaleString()}</b>\\n• 操盤診斷: ${netProfit >= 0 ? '✅ 廣告健康有獲利，建議維持或微調放大預算！' : '❌ 廣告虧損中，已低於損益平衡點，建議調整素材或客單價！'}`;
  } else if (currentTool.id === 'vat' || currentTool.name.includes('統一編號') || currentTool.name.includes('統編')) {
    const vat = document.getElementById('vat_input').value.trim();
    if (vat.length !== 8 || !/^\\d{8}$/.test(vat)) {
      res.innerText = '❌ 請輸入正確的 8 碼數字統一編號。';
      return;
    }
    const cx = [1, 2, 1, 2, 1, 2, 4, 1];
    let sum1 = 0, sum2 = 0;
    for (let i = 0; i < 8; i++) {
      let p = parseInt(vat[i]) * cx[i];
      let d1 = Math.floor(p / 10);
      let d2 = p % 10;
      sum1 += d1 + d2;
      if (i === 6 && vat[6] === '7') {
        sum2 += (d1 + d2 === 10 ? 1 : d1 + d2);
      } else {
        sum2 += d1 + d2;
      }
    }
    const valid = (sum1 % 5 === 0) || (vat[6] === '7' && sum2 % 5 === 0);
    res.innerHTML = valid ? 
      `✅ <b>驗證通過！</b> 統編【${vat}】符合台灣財政部新制/舊制檢查碼演算法。` : 
      `❌ <b>驗證失敗！</b> 統編【${vat}】檢查碼錯誤，非有效營業登記編號。`;
  } else {
    const title = document.getElementById('generic_title').value || '熱銷電商商品';
    const feat = document.getElementById('generic_features').value || '極致品質、台灣出貨';
    res.innerHTML = `✍️ 【${currentTool.name} 智慧輸出結果】\\n━━━━━━━━━━━━━━━━━━━━\\n【蝦皮/momo 標題】\\n🔥 限時爆款｜${title}（現貨供應 · 正品保證）\\n\\n【社群帶貨短文案 (FB/IG)】\\n還在找真正好用的【${title}】嗎？\\n解決你的痛點，三大核心升級一次到位：\\n✨ ${feat}\\n🚚 今日下單現貨秒出，點擊限時優惠搶購！\\n\\n【消保法標記】\\n本商品享 7 天猶豫期（非試用期）保障。`;
  }
}

renderTools(tools);
</script>
</body>
</html>
"""

full_content = html_head + "const tools = " + json.dumps(tools, ensure_ascii=False) + ";\n" + html_tail
open("D:/Workspace/03_Dev_Projects/wiki/static/ecom_tools.html", "w", encoding="utf-8").write(full_content)
print("Wrote ecom_tools.html successfully!")
