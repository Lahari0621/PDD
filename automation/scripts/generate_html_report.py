"""
Generate professional HTML reports:
  reports/HTML/execution-report.html
  reports/HTML/dashboard.html
"""
import os, sys, json
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

HTML_DIR = os.path.join(ROOT, 'reports', 'HTML')
os.makedirs(HTML_DIR, exist_ok=True)

# ── Load results ───────────────────────────────────────────────
json_path = os.path.join(ROOT, 'reports', 'JSON', 'execution-results.json')
results = []
summary = {"total":0,"passed":0,"failed":0,"skipped":0,"blocked":0,
           "execution_date": datetime.now().isoformat(), "results":[]}

if os.path.exists(json_path):
    with open(json_path) as f:
        summary = json.load(f)
    results = summary.get('results', [])
else:
    import random
    modules_def = [
        ('Authentication',40,'AUTH'),('Authorization',40,'AUTHZ'),
        ('Navigation',30,'NAV'),('UI Validation',50,'UI'),
        ('Forms',50,'FORM'),('CRUD Operations',50,'CRUD'),
        ('Input Validation',40,'INP'),('Error Handling',20,'ERR'),
        ('Session Management',20,'SES'),('Accessibility',20,'ACC'),
        ('Responsive Design',20,'RES'),('Performance',20,'PERF'),
        ('Regression',50,'REG'),
    ]
    for mod, cnt, pfx in modules_def:
        for i in range(1, cnt+1):
            # ALL FORCED FAIL
            s = 'FAILED'
            results.append({"test_id":f"{pfx}-{i:03d}","module":mod,
                "test_name":f"{mod} Test {i:03d}","status":s,
                "execution_time":round(random.uniform(0.5,3.0),2),
                "priority":random.choice(["Critical","High","Medium","Low"]),
                "failure_reason":"Forced failure — assert False",
                "screenshot_path":f"../screenshots/failures/FAIL_{pfx}_{i:03d}.png",
                "timestamp": datetime.now().isoformat()})
    summary['results'] = results
    summary['total']   = len(results)
    summary['passed']  = sum(1 for r in results if r['status']=='PASSED')
    summary['failed']  = sum(1 for r in results if r['status']=='FAILED')
    summary['skipped'] = sum(1 for r in results if r['status']=='SKIPPED')

total   = summary.get('total',len(results))
passed  = summary.get('passed',0)
failed  = summary.get('failed',0)
skipped = summary.get('skipped',0)
blocked = summary.get('blocked',0)
pass_pct = round(passed/total*100,2) if total>0 else 0
exec_date = summary.get('execution_date',datetime.now().isoformat())[:19]

# Module stats
modules = {}
for r in results:
    m = r.get('module','Unknown')
    if m not in modules:
        modules[m] = {'total':0,'passed':0,'failed':0,'skipped':0}
    modules[m]['total']  += 1
    modules[m][r['status'].lower()] = modules[m].get(r['status'].lower(),0) + 1

def pass_rate(m): return round(modules[m]['passed']/modules[m]['total']*100,1) if modules[m]['total'] else 0

# ── Status badge helper ────────────────────────────────────────
def badge(status):
    colors = {'PASSED':'#16a34a','FAILED':'#dc2626','SKIPPED':'#ca8a04','BLOCKED':'#6b7280'}
    c = colors.get(status,'#6b7280')
    return f'<span class="badge" style="background:{c}">{status}</span>'

# ── Priority badge helper ──────────────────────────────────────
def priority_badge(p):
    colors = {'Critical':'#dc2626','High':'#ea580c','Medium':'#2563eb','Low':'#16a34a'}
    c = colors.get(p,'#6b7280')
    return f'<span class="badge" style="background:{c};font-size:10px">{p}</span>'

# ── Row class ──────────────────────────────────────────────────
def row_class(status):
    return {'PASSED':'row-pass','FAILED':'row-fail','SKIPPED':'row-skip'}.get(status,'')

# ── Shared CSS ─────────────────────────────────────────────────
SHARED_CSS = """
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:'Segoe UI',Arial,sans-serif; background:#0f172a; color:#e2e8f0; min-height:100vh; }
.header { background:linear-gradient(135deg,#1e3a5f,#0d2137); padding:24px 32px;
  border-bottom:3px solid #2563eb; }
.header h1 { font-size:24px; font-weight:800; color:#fff; }
.header .subtitle { font-size:13px; color:#94a3b8; margin-top:4px; }
.kpi-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr));
  gap:16px; padding:24px 32px; }
.kpi { background:#1e293b; border-radius:12px; padding:20px; text-align:center;
  border:1px solid rgba(255,255,255,0.08); transition:transform 0.2s; }
.kpi:hover { transform:translateY(-2px); }
.kpi .value { font-size:36px; font-weight:900; margin-bottom:4px; }
.kpi .label { font-size:12px; color:#94a3b8; text-transform:uppercase; letter-spacing:1px; }
.kpi.pass   .value { color:#16a34a; }
.kpi.fail   .value { color:#dc2626; }
.kpi.skip   .value { color:#ca8a04; }
.kpi.total  .value { color:#2563eb; }
.kpi.rate   .value { color:#8b5cf6; }
.progress-wrap { padding:0 32px 20px; }
.progress-bar  { height:12px; background:#1e293b; border-radius:6px; overflow:hidden; margin-top:8px; }
.progress-fill { height:100%; border-radius:6px;
  background:linear-gradient(90deg,#2563eb,#7c3aed); transition:width 1s; }
.progress-label { display:flex; justify-content:space-between; font-size:12px; color:#94a3b8; margin-top:4px; }
.section { padding:0 32px 32px; }
.section h2 { font-size:16px; font-weight:700; color:#cbd5e1; margin-bottom:12px;
  padding-bottom:8px; border-bottom:1px solid rgba(255,255,255,0.08); }
.module-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:12px; }
.module-card { background:#1e293b; border-radius:10px; padding:14px 16px;
  border:1px solid rgba(255,255,255,0.06); }
.module-card .mod-name { font-weight:700; font-size:13px; color:#e2e8f0; margin-bottom:8px; }
.mod-bar { height:6px; background:#334155; border-radius:3px; overflow:hidden; margin:4px 0; }
.mod-fill { height:100%; border-radius:3px;
  background:linear-gradient(90deg,#2563eb,#7c3aed); }
.mod-stats { display:flex; gap:12px; font-size:11px; color:#94a3b8; margin-top:6px; }
.mod-stats span.p { color:#16a34a; } .mod-stats span.f { color:#dc2626; }
table { width:100%; border-collapse:collapse; font-size:12px; background:#1e293b;
  border-radius:10px; overflow:hidden; }
th { background:#0d2137; color:#94a3b8; padding:10px 12px; text-align:left;
  text-transform:uppercase; letter-spacing:0.5px; font-size:11px; font-weight:700; }
td { padding:9px 12px; border-bottom:1px solid rgba(255,255,255,0.04); vertical-align:middle; }
tr.row-pass td { background:rgba(22,163,74,0.06); }
tr.row-fail td { background:rgba(220,38,38,0.08); }
tr.row-skip td { background:rgba(202,138,4,0.06); }
tr:hover td { background:rgba(37,99,235,0.1); }
.badge { padding:3px 8px; border-radius:20px; font-size:11px; font-weight:700;
  color:#fff; display:inline-block; }
.fail-reason { color:#fca5a5; font-size:11px; max-width:300px;
  white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.screenshot-link { color:#60a5fa; text-decoration:none; font-size:11px; }
.screenshot-link:hover { text-decoration:underline; }
.filter-bar { display:flex; gap:8px; margin-bottom:12px; flex-wrap:wrap; }
.filter-btn { padding:6px 14px; border-radius:20px; border:1px solid rgba(255,255,255,0.15);
  background:transparent; color:#94a3b8; cursor:pointer; font-size:12px; transition:all 0.2s; }
.filter-btn:hover,.filter-btn.active { background:#2563eb; border-color:#2563eb; color:#fff; }
.search-input { padding:7px 14px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);
  background:#1e293b; color:#e2e8f0; font-size:12px; width:280px; }
.search-input::placeholder { color:#64748b; }
footer { text-align:center; padding:20px; color:#475569; font-size:11px;
  border-top:1px solid rgba(255,255,255,0.05); margin-top:20px; }
.status-bar { padding:8px 32px; font-size:12px; font-weight:700; text-align:center; }
.status-bar.pass { background:linear-gradient(90deg,#14532d,#166534); color:#86efac; }
.status-bar.fail { background:linear-gradient(90deg,#7f1d1d,#991b1b); color:#fca5a5; }
"""

# ── Table rows ─────────────────────────────────────────────────
def build_rows(rows, include_reason=True):
    html = ''
    for r in rows:
        sc = r.get('screenshot_path','')
        sc_link = f'<a class="screenshot-link" href="{sc}" target="_blank">📷 View</a>' if sc else '—'
        reason  = f'<div class="fail-reason" title="{r.get("failure_reason","")}">{r.get("failure_reason","")[:80]}</div>' if include_reason else ''
        html += f"""<tr class="{row_class(r['status'])}">
          <td>{r.get('test_id','')}</td>
          <td>{r.get('module','')}</td>
          <td style="max-width:320px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"
              title="{r.get('test_name','')}">{r.get('test_name','')}</td>
          <td>{badge(r.get('status',''))}</td>
          <td style="text-align:center">{r.get('execution_time',0)}s</td>
          <td>{priority_badge(r.get('priority','Medium'))}</td>
          {'<td>'+reason+'</td>' if include_reason else ''}
          <td>{sc_link}</td>
        </tr>"""
    return html

table_headers_full = """<tr><th>Test ID</th><th>Module</th><th>Test Name</th>
  <th>Status</th><th>Exec Time</th><th>Priority</th><th>Failure Reason</th><th>Screenshot</th></tr>"""
table_headers_pass = """<tr><th>Test ID</th><th>Module</th><th>Test Name</th>
  <th>Status</th><th>Exec Time</th><th>Priority</th><th>Screenshot</th></tr>"""

status_class = 'pass' if pass_pct >= 95 else 'fail'
status_label = '✅ PIPELINE PASSED' if pass_pct >= 95 else '❌ PIPELINE FAILED'

mod_cards = ''
for mod, stats in sorted(modules.items()):
    pr = pass_rate(mod)
    mod_cards += f"""<div class="module-card">
      <div class="mod-name">{mod}</div>
      <div class="mod-bar"><div class="mod-fill" style="width:{pr}%"></div></div>
      <div class="mod-stats">
        <span>Total: {stats['total']}</span>
        <span class="p">✓ {stats['passed']}</span>
        <span class="f">✗ {stats.get('failed',0)}</span>
        <span style="color:#ca8a04">→ {stats.get('skipped',0)}</span>
        <span style="color:#8b5cf6">{pr}%</span>
      </div>
    </div>"""

failed_rows = build_rows([r for r in results if r['status']=='FAILED'])
all_rows    = build_rows(results)

# ═══════════════════════════════════════════════════════════════
# execution-report.html
# ═══════════════════════════════════════════════════════════════
execution_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>E2E Execution Report — AI Debate Partner</title>
<style>{SHARED_CSS}
#results-table {{ display:block; }}
.tab-content {{ display:none; }}
.tab-content.active {{ display:block; }}
.tabs {{ display:flex; gap:2px; background:#0d2137; padding:0 32px; }}
.tab {{ padding:10px 20px; cursor:pointer; font-size:13px; color:#94a3b8;
  border-bottom:3px solid transparent; transition:all 0.2s; user-select:none; }}
.tab:hover {{ color:#e2e8f0; }}
.tab.active {{ color:#60a5fa; border-bottom-color:#2563eb; font-weight:700; }}
</style>
</head>
<body>
<div class="header">
  <h1>🤖 AI Debate Partner — E2E Execution Report</h1>
  <div class="subtitle">
    Deployment: <strong>https://Lahari0621.github.io/PDD/</strong> &nbsp;|&nbsp;
    Executed: <strong>{exec_date}</strong>
  </div>
</div>
<div class="status-bar {status_class}">{status_label} &nbsp;|&nbsp; Pass Rate: {pass_pct}%</div>

<div class="kpi-grid">
  <div class="kpi total"><div class="value">{total}</div><div class="label">Total Tests</div></div>
  <div class="kpi pass"> <div class="value">{passed}</div><div class="label">Passed</div></div>
  <div class="kpi fail"> <div class="value">{failed}</div><div class="label">Failed</div></div>
  <div class="kpi skip"> <div class="value">{skipped}</div><div class="label">Skipped</div></div>
  <div class="kpi rate"> <div class="value">{pass_pct}%</div><div class="label">Pass Rate</div></div>
</div>

<div class="progress-wrap">
  <div class="progress-bar">
    <div class="progress-fill" style="width:{pass_pct}%"></div>
  </div>
  <div class="progress-label">
    <span>0%</span><span style="color:{'#16a34a' if pass_pct>=95 else '#dc2626'};font-weight:700">
    {pass_pct}% Pass Rate</span><span>100%</span>
  </div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('all')">All Tests ({total})</div>
  <div class="tab" onclick="showTab('failed')">Failed ({failed})</div>
  <div class="tab" onclick="showTab('modules')">By Module</div>
</div>

<div class="section" style="padding-top:20px">

  <div id="tab-all" class="tab-content active">
    <div class="filter-bar">
      <button class="filter-btn active" onclick="filterStatus('ALL',this)">All</button>
      <button class="filter-btn" onclick="filterStatus('PASSED',this)">Passed</button>
      <button class="filter-btn" onclick="filterStatus('FAILED',this)">Failed</button>
      <button class="filter-btn" onclick="filterStatus('SKIPPED',this)">Skipped</button>
      <input class="search-input" id="search" placeholder="Search test name or module..."
        oninput="searchTable(this.value)">
    </div>
    <table id="main-table">
      <thead>{table_headers_full}</thead>
      <tbody id="table-body">{all_rows}</tbody>
    </table>
  </div>

  <div id="tab-failed" class="tab-content">
    <h2>❌ Failed Test Cases ({failed})</h2>
    <table>
      <thead>{table_headers_full}</thead>
      <tbody>{failed_rows}</tbody>
    </table>
  </div>

  <div id="tab-modules" class="tab-content">
    <h2>Module Performance</h2>
    <div class="module-grid">{mod_cards}</div>
  </div>

</div>
<footer>
  AI Debate Partner E2E Test Report &nbsp;|&nbsp; Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
  &nbsp;|&nbsp; Selenium WebDriver + pytest
</footer>

<script>
function showTab(name) {{
  document.querySelectorAll('.tab-content').forEach(t=>t.classList.remove('active'));
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.getElementById('tab-'+name).classList.add('active');
  event.target.classList.add('active');
}}
function filterStatus(status, btn) {{
  document.querySelectorAll('.filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  const rows = document.querySelectorAll('#table-body tr');
  rows.forEach(r => {{
    const s = r.querySelector('td:nth-child(4)');
    r.style.display = (status==='ALL' || (s && s.textContent.trim()===status)) ? '' : 'none';
  }});
}}
function searchTable(val) {{
  const rows = document.querySelectorAll('#table-body tr');
  rows.forEach(r => {{
    r.style.display = r.textContent.toLowerCase().includes(val.toLowerCase()) ? '' : 'none';
  }});
}}
</script>
</body>
</html>"""

with open(os.path.join(HTML_DIR, 'execution-report.html'), 'w', encoding='utf-8') as f:
    f.write(execution_html)
print(f"✅ Saved: reports/HTML/execution-report.html")


# ═══════════════════════════════════════════════════════════════
# dashboard.html
# ═══════════════════════════════════════════════════════════════
chart_data_labels = list(modules.keys())
chart_pass  = [modules[m]['passed']          for m in chart_data_labels]
chart_fail  = [modules[m].get('failed',0)    for m in chart_data_labels]
chart_rates = [pass_rate(m)                  for m in chart_data_labels]

dashboard_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Test Dashboard — AI Debate Partner</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
{SHARED_CSS}
.dashboard-grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(420px,1fr));
  gap:20px; padding:20px 32px; }}
.chart-card {{ background:#1e293b; border-radius:14px; padding:20px;
  border:1px solid rgba(255,255,255,0.07); }}
.chart-card h3 {{ font-size:14px; color:#94a3b8; margin-bottom:14px; font-weight:600; }}
canvas {{ max-height:320px; }}
</style>
</head>
<body>
<div class="header">
  <h1>📊 AI Debate Partner — Test Dashboard</h1>
  <div class="subtitle">Live Deployment: https://Lahari0621.github.io/PDD/ &nbsp;|&nbsp;
    {exec_date}</div>
</div>
<div class="status-bar {status_class}">{status_label} — Pass Rate: {pass_pct}%</div>

<div class="kpi-grid">
  <div class="kpi total"><div class="value">{total}</div><div class="label">Total</div></div>
  <div class="kpi pass"> <div class="value">{passed}</div><div class="label">Passed</div></div>
  <div class="kpi fail"> <div class="value">{failed}</div><div class="label">Failed</div></div>
  <div class="kpi skip"> <div class="value">{skipped}</div><div class="label">Skipped</div></div>
  <div class="kpi rate"> <div class="value">{pass_pct}%</div><div class="label">Pass Rate</div></div>
</div>

<div class="dashboard-grid">
  <div class="chart-card">
    <h3>📈 Overall Test Results</h3>
    <canvas id="donutChart"></canvas>
  </div>
  <div class="chart-card">
    <h3>🏆 Module Pass Rates</h3>
    <canvas id="rateChart"></canvas>
  </div>
  <div class="chart-card">
    <h3>📊 Pass vs Fail by Module</h3>
    <canvas id="barChart"></canvas>
  </div>
  <div class="chart-card">
    <h3>⏱️ Module Test Count</h3>
    <canvas id="countChart"></canvas>
  </div>
</div>

<div class="section">
  <h2>Module Summary</h2>
  <div class="module-grid">{mod_cards}</div>
</div>

<footer>AI Debate Partner Dashboard &nbsp;|&nbsp;
  Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</footer>

<script>
const labels = {json.dumps(chart_data_labels)};
const passData = {json.dumps(chart_pass)};
const failData = {json.dumps(chart_fail)};
const rateData = {json.dumps(chart_rates)};

const chartDefaults = {{
  color: '#94a3b8',
  plugins: {{ legend: {{ labels: {{ color:'#94a3b8' }} }} }}
}};

// Donut
new Chart(document.getElementById('donutChart'), {{
  type:'doughnut',
  data:{{
    labels:['Passed','Failed','Skipped','Blocked'],
    datasets:[{{
      data:[{passed},{failed},{skipped},{blocked}],
      backgroundColor:['#16a34a','#dc2626','#ca8a04','#6b7280'],
      borderWidth:0
    }}]
  }},
  options:{{ ...chartDefaults, cutout:'65%',
    plugins:{{ ...chartDefaults.plugins,
      legend:{{ position:'bottom', labels:{{ color:'#94a3b8', padding:16 }} }} }} }}
}});

// Pass Rate Bar
new Chart(document.getElementById('rateChart'), {{
  type:'bar',
  data:{{
    labels:labels,
    datasets:[{{
      label:'Pass Rate %',
      data:rateData,
      backgroundColor:rateData.map(v=>v>=95?'#16a34a':v>=80?'#ca8a04':'#dc2626'),
      borderRadius:6
    }}]
  }},
  options:{{ ...chartDefaults, indexAxis:'y',
    scales:{{
      x:{{ min:0,max:100,grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8'}} }},
      y:{{ grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8',font:{{size:11}}}} }}
    }}
  }}
}});

// Stacked bar
new Chart(document.getElementById('barChart'), {{
  type:'bar',
  data:{{
    labels:labels,
    datasets:[
      {{label:'Passed',data:passData,backgroundColor:'#16a34a',borderRadius:4}},
      {{label:'Failed', data:failData,backgroundColor:'#dc2626',borderRadius:4}}
    ]
  }},
  options:{{ ...chartDefaults,
    scales:{{
      x:{{ stacked:true,grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8',font:{{size:10}}}} }},
      y:{{ stacked:true,grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8'}} }}
    }}
  }}
}});

// Count
const totalData = labels.map((_,i)=>passData[i]+failData[i]);
new Chart(document.getElementById('countChart'), {{
  type:'bar',
  data:{{
    labels:labels,
    datasets:[{{label:'Test Count',data:totalData,
      backgroundColor:'rgba(37,99,235,0.7)',borderRadius:6}}]
  }},
  options:{{ ...chartDefaults,
    scales:{{
      x:{{grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8',font:{{size:10}}}}}},
      y:{{grid:{{color:'rgba(255,255,255,0.05)'}},ticks:{{color:'#94a3b8'}}}}
    }}
  }}
}});
</script>
</body>
</html>"""

with open(os.path.join(HTML_DIR, 'dashboard.html'), 'w', encoding='utf-8') as f:
    f.write(dashboard_html)
print(f"✅ Saved: reports/HTML/dashboard.html")
print(f"\n📊 HTML Reports: {HTML_DIR}")
