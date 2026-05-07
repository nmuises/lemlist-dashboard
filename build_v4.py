#!/usr/bin/env python3
"""
Dashboard v4 — Complete. 7 tabs, compact cells, direct JSON embedding.
"""
import json

MODEL_PATH = '.tmp/lemlist-api/enhanced_model_v2.json'
OUT_PATH = 'context/drop-zone/Muir Campaign Performance - Standalone.html'

with open(MODEL_PATH) as f:
    model = json.load(f)
print(f"Loaded: {len(model['campaigns'])} campaigns, {model['total_activities']} activities")

# Preparse enriched data: campaign_id -> campaign_name, sender_name
camp_lookup = {c['id']: c['name'] for c in model['campaigns']}
camp_type_lookup = {c['id']: c['type'] for c in model['campaigns']}

# Build HTML parts
P = []

# ── CSS ──
P.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Muir AI — Lemlist Performance Dashboard</title>
<style>
:root {
  --bg: #0f172a; --card: #1e293b; --text: #e2e8f0; --muted: #94a3b8;
  --accent: #3b82f6; --accent2: #8b5cf6; --success: #22c55e; --warning: #f59e0b;
  --danger: #ef4444; --info: #06b6d4; --border: #334155;
}
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background:var(--bg); color:var(--text); line-height:1.6; }
.container { max-width:1500px; margin:0 auto; padding:20px; }
header { margin-bottom:24px; }
header h1 { font-size:1.8rem; font-weight:700; margin-bottom:4px; }
header p { color:var(--muted); font-size:0.9rem; }

.controls { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:24px; }
.controls h3 { font-size:0.85rem; text-transform:uppercase; letter-spacing:0.05em; color:var(--muted); margin-bottom:12px; }
.maturity-control { display:flex; align-items:center; gap:16px; flex-wrap:wrap; }
.maturity-control label { font-size:0.9rem; color:var(--muted); }
.maturity-control input[type=range] { width:300px; accent-color:var(--accent); }
.maturity-value { font-size:1.2rem; font-weight:700; color:var(--accent); min-width:60px; text-align:center; }
.maturity-desc { font-size:0.8rem; color:var(--muted); font-style:italic; }

.email-controls { display:flex; gap:16px; align-items:center; flex-wrap:wrap; margin-bottom:16px; }
.email-controls input[type=date] { background:var(--bg); border:1px solid var(--border); color:var(--text); padding:6px 10px; border-radius:6px; font-size:0.85rem; }
.email-controls label { font-size:0.85rem; color:var(--muted); }

.card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; margin-bottom:20px; }
.card h2 { font-size:1.1rem; font-weight:600; margin-bottom:16px; display:flex; align-items:center; gap:8px; }
.badge { font-size:0.7rem; padding:2px 8px; border-radius:20px; font-weight:500; text-transform:uppercase; }
.badge-info { background:rgba(6,182,212,0.15); color:var(--info); }
.badge-warning { background:rgba(245,158,11,0.15); color:var(--warning); }
.badge-success { background:rgba(34,197,94,0.15); color:var(--success); }

.stats-grid { display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:16px; margin-bottom:16px; }
.stat { background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:8px; padding:16px; }
.stat-value { font-size:1.6rem; font-weight:700; margin-bottom:4px; }
.stat-label { font-size:0.8rem; color:var(--muted); text-transform:uppercase; letter-spacing:0.03em; }
.stat-delta { font-size:0.75rem; margin-top:4px; color:var(--muted); }

table { width:100%; border-collapse:collapse; font-size:0.82rem; }
th { text-align:left; padding:8px 10px; color:var(--muted); font-weight:600; text-transform:uppercase; font-size:0.68rem; letter-spacing:0.03em; border-bottom:1px solid var(--border); white-space:nowrap; }
td { padding:8px 10px; border-bottom:1px solid rgba(255,255,255,0.04); vertical-align:middle; }
tr:hover td { background:rgba(255,255,255,0.02); }
.td-num { text-align:right; font-variant-numeric:tabular-nums; }
.td-campaign { font-weight:500; max-width:260px; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }
.td-type { font-size:0.7rem; white-space:nowrap; }
.scroll-h { overflow-x:auto; }

/* Compact cell: sent → positive (rate) */
.ch-cell { display:inline-flex; align-items:center; gap:4px; font-variant-numeric:tabular-nums; white-space:nowrap; padding:2px 6px; border-radius:4px; }
.ch-sent { color:var(--muted); font-size:0.82rem; }
.ch-arrow { color:var(--muted); font-size:0.7rem; margin:0 2px; }
.ch-pos { font-weight:600; font-size:0.85rem; }
.ch-rate { font-size:0.72rem; margin-left:2px; }
.ch-rate-good { color:var(--success); }
.ch-rate-avg { color:var(--warning); }
.ch-rate-bad { color:var(--danger); }
/* Channel indicators */
.ch-dm { border-left: 3px solid rgba(59,130,246,0.60); }
.ch-email { border-left: 3px solid rgba(6,182,212,0.60); }
.ch-invite { border-left: 3px solid rgba(139,92,246,0.60); }
.ch-combined { border-left: 3px solid rgba(148,163,184,0.45); }

.tabs { display:flex; gap:4px; margin-bottom:16px; border-bottom:1px solid var(--border); padding-bottom:0; overflow-x:auto; }
.tab { padding:8px 16px; font-size:0.85rem; cursor:pointer; border-radius:6px 6px 0 0; border-bottom:2px solid transparent; color:var(--muted); white-space:nowrap; user-select:none; }
.tab.active { color:var(--text); border-bottom-color:var(--accent); background:rgba(59,130,246,0.08); }
.tab-content { display:none; }
.tab-content.active { display:block; }

.insight { padding:12px 16px; border-radius:8px; margin-bottom:8px; font-size:0.85rem; }
.insight-good { background:rgba(34,197,94,0.08); border-left:3px solid var(--success); }
.insight-warn { background:rgba(245,158,11,0.08); border-left:3px solid var(--warning); }
.insight-bad { background:rgba(239,68,68,0.08); border-left:3px solid var(--danger); }
.insight-info { background:rgba(6,182,212,0.08); border-left:3px solid var(--info); }

.filter-bar { display:flex; gap:6px; margin-bottom:12px; flex-wrap:wrap; }
.filter-btn { padding:4px 12px; border-radius:16px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer; font-size:0.78rem; }
.filter-btn.active { background:var(--accent); color:#fff; border-color:var(--accent); }

.chart-container { margin:16px 0; }
.bar-row { display:flex; align-items:center; gap:8px; margin:4px 0; }
.bar-label-w { width:105px; text-align:right; font-size:0.75rem; color:var(--muted); flex-shrink:0; }
.bar-track { flex:1; height:22px; background:rgba(255,255,255,0.04); border-radius:4px; overflow:hidden; position:relative; }
.bar-fill { height:100%; border-radius:4px; display:flex; align-items:center; padding:0 8px; font-size:0.7rem; font-weight:600; transition:width 0.3s; }
.bar-val { width:50px; text-align:right; font-size:0.78rem; font-weight:600; flex-shrink:0; }

footer { text-align:center; padding:40px 0; color:var(--muted); font-size:0.8rem; }

/* ── Filter Dropdowns ── */
.filter-row { display:flex; gap:10px; margin-bottom:14px; flex-wrap:wrap; align-items:flex-start; }
.filter-dropdown { position:relative; }
.dd-btn { background:var(--bg); border:1px solid var(--border); color:var(--text); padding:6px 12px; border-radius:6px; cursor:pointer; font-size:0.78rem; display:flex; align-items:center; gap:4px; white-space:nowrap; }
.dd-btn:hover { border-color:var(--accent); }
.dd-arrow { font-size:0.6rem; margin-left:2px; }
.dd-panel { display:none; position:absolute; top:100%; left:0; margin-top:4px; background:var(--card); border:1px solid var(--border); border-radius:8px; padding:8px 0; min-width:220px; max-height:340px; overflow-y:auto; z-index:100; box-shadow:0 8px 24px rgba(0,0,0,0.4); }
.dd-panel.open { display:block; }
.dd-option { display:flex; align-items:center; gap:8px; padding:5px 12px; cursor:pointer; font-size:0.78rem; color:var(--text); white-space:nowrap; }
.dd-option:hover { background:rgba(255,255,255,0.04); }
.dd-option input[type=checkbox] { accent-color:var(--accent); cursor:pointer; }
.dd-option-all { border-bottom:1px solid var(--border); padding-bottom:7px; margin-bottom:4px; font-weight:600; }

/* ── Sortable Headers ── */
.th-sort { cursor:pointer; user-select:none; }
.th-sort:hover { color:var(--text); }
.sort-arrow { font-size:0.65rem; margin-left:2px; }

/* ── Totals Row ── */
.total-row td { font-weight:600; background:rgba(255,255,255,0.04); }
.total-sep td { border-bottom:2px solid var(--border); padding:0; height:0; }

/* ── Channel Toggle ── */
.channel-toggle { display:flex; gap:2px; }
.ch-toggle-btn { padding:6px 14px; border:1px solid var(--border); background:transparent; color:var(--muted); cursor:pointer; font-size:0.78rem; }
.ch-toggle-btn:first-child { border-radius:6px 0 0 6px; }
.ch-toggle-btn:last-child { border-radius:0 6px 6px 0; }
.ch-toggle-btn.active { background:var(--accent); color:#fff; border-color:var(--accent); }
</style>
</head>
<body>
<div class="container">
<header>
  <h1>Muir AI — Lemlist Performance Dashboard</h1>
  <p>28 campaigns · 6,024 activities · 1,280 leads · Built 2026-05-06</p>
</header>

<div class="controls">
  <h3>Maturity Filter</h3>
  <div class="maturity-control">
    <label>Exclude activity newer than:</label>
    <input type="range" id="maturitySlider" min="0" max="30" value="7" step="1">
    <div class="maturity-value"><span id="maturityVal">7</span>d</div>
    <div class="maturity-desc" id="maturityDesc">Standard — DMs need ~7 days for replies</div>
  </div>
</div>

<div class="controls">
  <h3>Rate Benchmarks <span style="font-weight:400;font-size:0.75rem;color:var(--muted);">(targets for color coding)</span></h3>
  <div class="maturity-control">
    <label>Invite accept:</label>
    <input type="range" id="inviteTarget" min="5" max="60" value="30" step="1">
    <div class="maturity-value" style="color:var(--accent2);"><span id="inviteTargetVal">30</span>%</div>
  </div>
  <div class="maturity-control">
    <label>DM reply:</label>
    <input type="range" id="dmTarget" min="2" max="50" value="10" step="1">
    <div class="maturity-value"><span id="dmTargetVal">10</span>%</div>
  </div>
  <div class="maturity-control">
    <label>Email reply:</label>
    <input type="range" id="emailTarget" min="1" max="30" value="5" step="1">
    <div class="maturity-value" style="color:var(--info);"><span id="emailTargetVal">5</span>%</div>
  </div>
  <div class="maturity-desc" style="margin-top:8px;"><span style="color:var(--success);">Green</span> = at or above target · <span style="color:var(--warning);">Yellow</span> = 50-99% of target · <span style="color:var(--danger);">Red</span> = below 50%</div>
</div>

<div class="card">
  <h2>Overview <span class="badge badge-info">Live</span></h2>
  <div class="stats-grid" id="overviewStats"></div>
  <div id="overviewInsights"></div>
</div>

<div class="tabs">
  <div class="tab active" onclick="switchTab('perf')">Performance</div>
  <div class="tab" onclick="switchTab('steps')">By Step</div>
  <div class="tab" onclick="switchTab('copy')">Copy Analysis</div>
  <div class="tab" onclick="switchTab('ab')">A/B Tests</div>
  <div class="tab" onclick="switchTab('trends')">Trends</div>
  <div class="tab" onclick="switchTab('email')">Email</div>
  <div class="tab" onclick="switchTab('raw')">Raw Data</div>
</div>

<div class="tab-content active" id="tab-perf">
  <div class="card">
    <h2>Campaign Performance by Channel <span class="badge badge-info">Filtered</span></h2>
    <div class="filter-row">
      <div class="filter-dropdown" id="perf-type">
        <button class="dd-btn" onclick="ddToggle('perf-type')">Type: <span id="perf-type-label">All</span> <span class="dd-arrow">▾</span></button>
        <div class="dd-panel" id="perf-type-panel"></div>
      </div>
      <div class="filter-dropdown" id="perf-sender">
        <button class="dd-btn" onclick="ddToggle('perf-sender')">Sender: <span id="perf-sender-label">All</span> <span class="dd-arrow">▾</span></button>
        <div class="dd-panel" id="perf-sender-panel"></div>
      </div>
      <div class="filter-dropdown" id="perf-campaign">
        <button class="dd-btn" onclick="ddToggle('perf-campaign')">Campaign: <span id="perf-campaign-label">All</span> <span class="dd-arrow">▾</span></button>
        <div class="dd-panel" id="perf-campaign-panel"></div>
      </div>
    </div>
    <div class="scroll-h">
      <table><thead><tr>
        <th class="th-sort" onclick="perfSort('name')">Campaign <span class="sort-arrow" id="sa-perf-name"></span></th>
        <th class="th-sort" onclick="perfSort('type')">Type <span class="sort-arrow" id="sa-perf-type"></span></th>
        <th class="th-sort" onclick="perfSort('sender')">Sender <span class="sort-arrow" id="sa-perf-sender"></span></th>
        <th class="th-sort td-num" onclick="perfSort('leads')">Current Leads <span class="sort-arrow" id="sa-perf-leads"></span></th>
        <th class="th-sort td-num" onclick="perfSort('pipeline')">Pipeline <span class="sort-arrow" id="sa-perf-pipeline"></span></th>
        <th class="th-sort" onclick="perfSort('invites')">Invites <span class="sort-arrow" id="sa-perf-invites"></span></th>
        <th class="th-sort" onclick="perfSort('dms')">DMs <span class="sort-arrow" id="sa-perf-dms"></span></th>
        <th class="th-sort" onclick="perfSort('emails')">Emails <span class="sort-arrow" id="sa-perf-emails"></span></th>
        <th class="th-sort td-num" onclick="perfSort('interested')">Interested <span class="sort-arrow" id="sa-perf-interested"></span></th>
        <th class="th-sort" onclick="perfSort('last')">Last <span class="sort-arrow" id="sa-perf-last"></span></th>
      </tr></thead><tbody id="perfBody"></tbody></table>
    </div>
  </div>
</div>

<div class="tab-content" id="tab-steps">
  <div class="card">
    <h2>Performance by Step <span class="badge badge-info">Filtered</span></h2>
    <div style="font-size:0.72rem;color:var(--muted);margin-bottom:10px;display:flex;gap:16px;align-items:center;">
      <span>Channel:</span>
      <span style="border-left:3px solid rgba(59,130,246,0.60);padding-left:6px;">LinkedIn DM</span>
      <span style="border-left:3px solid rgba(6,182,212,0.60);padding-left:6px;">Email</span>
      <span style="border-left:3px solid rgba(139,92,246,0.60);padding-left:6px;">Invite</span>
      <span style="border-left:3px solid rgba(148,163,184,0.45);padding-left:6px;">Combined</span>
    </div>
    <div class="filter-row">
      <div class="channel-toggle" id="stepChannelToggle">
        <button class="ch-toggle-btn active" onclick="setStepChannel('both')">LinkedIn + Email</button>
        <button class="ch-toggle-btn" onclick="setStepChannel('linkedin')">LinkedIn Only</button>
        <button class="ch-toggle-btn" onclick="setStepChannel('email')">Email Only</button>
      </div>
      <div class="filter-dropdown" id="step-campaign">
        <button class="dd-btn" onclick="ddToggle('step-campaign')">Campaign: <span id="step-campaign-label">All</span> <span class="dd-arrow">▾</span></button>
        <div class="dd-panel" id="step-campaign-panel"></div>
      </div>
    </div>
    <div class="scroll-h"><div id="stepTable"></div></div>
  </div>
</div>

<div class="tab-content" id="tab-copy">
  <div class="card">
    <h2>Copy Performance <span class="badge badge-info">All Time</span></h2>
    <div class="filter-bar" id="copySenderFilter"></div>
    <div class="filter-bar" style="margin-bottom:16px;">
      <span style="font-size:0.78rem;color:var(--muted);margin-right:8px;">View:</span>
      <button class="filter-btn active" id="copyViewIndiv" onclick="setCopyView('individual')">Individual</button>
      <button class="filter-btn" id="copyViewGroup" onclick="setCopyView('grouped')">Grouped by Template</button>
    </div>
    <div class="scroll-h">
      <table><thead><tr id="copyHeader"></tr></thead><tbody id="copyBody"></tbody></table>
    </div>
  </div>
</div>

<div class="tab-content" id="tab-ab">
  <div class="card">
    <h2>A/B Test Results <span class="badge badge-info">Copy-Level</span></h2>
    <div id="abSummary"></div>
    <div class="scroll-h"><div id="abTable"></div></div>
  </div>
</div>

<div class="tab-content" id="tab-trends">
  <div class="card">
    <h2>Weekly Activity Volume</h2>
    <div class="chart-container" id="weeklyVolume"></div>
  </div>
  <div class="card">
    <h2>Weekly DM Reply Rate</h2>
    <div class="chart-container" id="weeklyRate"></div>
  </div>
</div>

<div class="tab-content" id="tab-email">
  <div class="card">
    <h2>Email Deliverability</h2>
    <div class="email-controls">
      <label>DNS fix date:</label>
      <input type="date" id="dnsDate" value="2026-04-28">
      <span style="margin-left:auto;font-size:0.8rem;color:var(--muted);">Post-DNS since: <strong id="dnsWindow">—</strong></span>
    </div>
    <div class="stats-grid" id="emailStats"></div>
    <div id="emailInsights"></div>
  </div>
  <div class="card">
    <h2>Email by Campaign</h2>
    <div class="scroll-h">
      <table><thead><tr><th>Campaign</th><th>Pre Sends</th><th>Pre Replies</th><th>Post Sends</th><th>Post Replies</th><th>Rate</th></tr></thead>
      <tbody id="emailBody"></tbody></table>
    </div>
  </div>
</div>

<div class="tab-content" id="tab-raw">
  <div class="card">
    <h2>All Campaigns</h2>
    <div class="scroll-h"><div id="rawList"></div></div>
  </div>
</div>

<footer>Muir AI · Lemlist Performance Dashboard · Built 2026-05-06</footer>
</div>
''')

# ── JavaScript ──
P.append('<script>')
model_json = json.dumps(model, ensure_ascii=False)
P.append('var RAW_DATA = ' + model_json + ';')

# JS code
P.append(r'''
var maturityDays = 7;
var dnsFixDate = new Date('2026-04-28');
var copyFilterSender = 'All';
var copyViewMode = 'individual';
var inviteTarget = 30;
var dmTarget = 10;
var emailTarget = 5;

// ── Filter & Sort State ──
var ddState = {};       // dropdown id → {options, excluded, onChange}
var perfExcluded = {};  // {type: {value:true}, sender: {value:true}, campaign: {value:true}} — empty = all
var perfSortCol = '';
var perfSortDir = 0;    // 0=none, 1=asc, -1=desc
var stepChannel = 'both'; // 'both', 'linkedin', 'email'
var stepExcluded = {};  // {campaign: {value:true}} — empty = all
var stepSortCol = '';
var stepSortDir = 0;
perfExcluded.type = {}; perfExcluded.sender = {}; perfExcluded.campaign = {};
stepExcluded.campaign = {};

function parseDate(s) {
  if (!s) return null;
  var d = new Date(s);
  return isNaN(d.getTime()) ? null : d;
}
function daysDiff(d1, d2) {
  return Math.floor((d2 - d1) / (1000 * 60 * 60 * 24));
}
function isMature(dateStr, matDays, now) {
  var d = parseDate(dateStr);
  if (!d) return false;
  return daysDiff(d, now) >= matDays;
}
function fmtNum(n) {
  if (n === undefined || n === null) return '0';
  return n.toLocaleString();
}
function fmtPct(n, d) {
  if (!d || d === 0) return '—';
  return (n / d * 100).toFixed(1) + '%';
}
function rateColor(rate, channel) {
  var target;
  if (channel === 'email') target = emailTarget;
  else if (channel === 'invite') target = inviteTarget;
  else if (channel === 'combined') target = dmTarget;
  else target = dmTarget;
  if (target === 0) return 'ch-rate-avg';
  var pct = rate / target;
  if (pct >= 1.0) return 'ch-rate-good';
  if (pct >= 0.5) return 'ch-rate-avg';
  return 'ch-rate-bad';
}
function compactCell(sent, positive, channel) {
  if (!channel) channel = 'dm';
  if (!sent || sent === 0) return '<span class="ch-cell ch-' + channel + '"><span class="ch-sent">0</span></span>';
  var rate = positive / sent * 100;
  var cls = rateColor(rate, channel);
  return '<span class="ch-cell ch-' + channel + '"><span class="ch-sent">' + fmtNum(sent) + '</span><span class="ch-arrow">→</span><span class="ch-pos">' + fmtNum(positive) + '</span><span class="ch-rate ' + cls + '">' + rate.toFixed(1) + '%</span></span>';
}
function emailCell(sent, positive) {
  if (!sent || sent === 0) return '<span class="ch-cell ch-email"><span class="ch-sent">0</span></span>';
  var rate = positive / sent * 100;
  var cls = rateColor(rate, 'email');
  return '<span class="ch-cell ch-email"><span class="ch-sent">' + fmtNum(sent) + '</span><span class="ch-arrow">→</span><span class="ch-pos">' + fmtNum(positive) + '</span><span class="ch-rate ' + cls + '">' + rate.toFixed(1) + '%</span></span>';
}

function getFiltered() {
  var now = new Date();
  return RAW_DATA.campaigns.map(function(c) {
    // Separate sends (maturity-gated) from responses (always count if lead has mature send)
    var matureSends = [];
    var responses = [];
    var other = [];
    var matureLeadIds = {};
    c.activities.forEach(function(a) {
      var isSend = (a.step === 'message_sent' || a.step === 'invite_sent' || a.step === 'email_sent');
      var isResponse = (a.step === 'message_replied' || a.step === 'invite_accepted' || a.step === 'email_replied');
      if (isSend) {
        if (isMature(a.date, maturityDays, now)) {
          matureSends.push(a);
          if (a.lead_id) matureLeadIds[a.lead_id] = true;
        }
      } else if (isResponse) {
        responses.push(a);
      } else {
        other.push(a);
      }
    });
    // Only include responses/other from leads who have at least one mature send
    var validResponses = responses.filter(function(a) {
      return a.lead_id && matureLeadIds[a.lead_id];
    });
    var validOther = other.filter(function(a) {
      return a.lead_id && matureLeadIds[a.lead_id];
    });
    var allFiltered = matureSends.concat(validResponses).concat(validOther);
    return {campaign: c, activities: allFiltered};
  });
}

function uniqueLeads(activities, step) {
  var seen = {};
  activities.forEach(function(a) {
    if (a.step === step && a.lead_id) seen[a.lead_id] = true;
  });
  return Object.keys(seen).length;
}

function pipelineLeads(campaign, activities) {
  var seen = {};
  activities.forEach(function(a) {
    if (a.lead_id) seen[a.lead_id] = true;
  });
  return Object.keys(seen).length;
}

// ── DROPDOWN SYSTEM ──
function ddInit(id, options, onChange) {
  ddState[id] = {options: options, excluded: {}, onChange: onChange};
  var panel = document.getElementById(id + '-panel');
  var html = '<label class="dd-option dd-option-all"><input type="checkbox" checked onchange="ddToggleAll(\'' + id + '\', this.checked)"> All</label>';
  options.forEach(function(o) {
    html += '<label class="dd-option"><input type="checkbox" value="' + o.id.replace(/"/g, '&quot;').replace(/'/g, "&#39;") + '" checked onchange="ddCheck(\'' + id + '\', this.value, this.checked)"> ' + o.label + '</label>';
  });
  panel.innerHTML = html;
  ddUpdateLabel(id);
}

function ddToggle(id) {
  var panel = document.getElementById(id + '-panel');
  var isOpen = panel.classList.contains('open');
  // Close all dropdowns
  Object.keys(ddState).forEach(function(k) {
    document.getElementById(k + '-panel').classList.remove('open');
  });
  if (!isOpen) panel.classList.add('open');
}

function ddToggleAll(id, checked) {
  var st = ddState[id];
  if (checked) {
    st.excluded = {};
  } else {
    st.options.forEach(function(o) { st.excluded[o.id] = true; });
  }
  ddSyncCheckboxes(id);
  ddUpdateLabel(id);
  st.onChange();
}

function ddCheck(id, value, checked) {
  var st = ddState[id];
  if (checked) {
    delete st.excluded[value];
  } else {
    st.excluded[value] = true;
  }
  // Sync All checkbox
  var allChecked = Object.keys(st.excluded).length === 0;
  var panel = document.getElementById(id + '-panel');
  var allCb = panel.querySelector('.dd-option-all input');
  if (allCb) allCb.checked = allChecked;
  ddUpdateLabel(id);
  st.onChange();
}

function ddSyncCheckboxes(id) {
  var st = ddState[id];
  var panel = document.getElementById(id + '-panel');
  var cbs = panel.querySelectorAll('input[type=checkbox]');
  cbs.forEach(function(cb) {
    if (cb.parentElement.classList.contains('dd-option-all')) return;
    cb.checked = !st.excluded.hasOwnProperty(cb.value);
  });
}

function ddUpdateLabel(id) {
  var st = ddState[id];
  var count = Object.keys(st.excluded).length;
  var total = st.options.length;
  var label = count === 0 ? 'All' : (count >= total ? 'None' : (total - count) + ' selected');
  document.getElementById(id + '-label').textContent = label;
}

function ddIsFiltered(id) {
  var st = ddState[id];
  return Object.keys(st.excluded).length > 0;
}

function ddMatch(id, value) {
  var st = ddState[id];
  return !st.excluded.hasOwnProperty(value);
}

// ── SORT HELPERS ──
function sortNum(a, b) { return a - b; }
function sortStr(a, b) { return a.localeCompare(b); }
function sortDate(a, b) { return (a||'').localeCompare(b||''); }

function applySort(arr, col, dir, extract) {
  if (!dir || !col) return arr;
  var sorted = arr.slice().sort(function(a, b) {
    var va = extract(a, col), vb = extract(b, col);
    var cmp = typeof va === 'number' ? sortNum(va, vb) : sortStr(String(va||''), String(vb||''));
    return dir * cmp;
  });
  return sorted;
}

function updateSortArrows(prefix, col, dir) {
  for (var i = 0; i < 20; i++) {
    var el = document.getElementById('sa-' + prefix + '-placeholder'); // not used — clear all arrows
  }
  // Clear all arrows with this prefix
  var all = document.querySelectorAll('[id^="sa-' + prefix + '-"]');
  for (var j = 0; j < all.length; j++) { all[j].textContent = ''; }
  if (dir !== 0) {
    var arrow = document.getElementById('sa-' + prefix + '-' + col);
    if (arrow) arrow.textContent = dir === 1 ? '▲' : '▼';
  }
}

// ── PERFORMANCE TAB SORT ──
function perfSort(col) {
  if (perfSortCol === col) {
    perfSortDir = perfSortDir === 1 ? -1 : (perfSortDir === -1 ? 0 : 1);
  } else {
    perfSortCol = col;
    perfSortDir = 1;
  }
  if (perfSortDir === 0) perfSortCol = '';
  updateSortArrows('perf', col, perfSortDir);
  renderPerf();
}

function perfExtract(d, col) {
  switch (col) {
    case 'name': return d.campaign.name;
    case 'type': return d.campaign.type;
    case 'sender': return d.campaign.sender || '';
    case 'leads': return d.campaign.lead_count;
    case 'pipeline': return d.pl;
    case 'invites': return d.invites;
    case 'dms': return d.sent;
    case 'emails': return d.emails;
    case 'interested': return d.interested;
    case 'last': return d.campaign.last_activity || '';
    default: return 0;
  }
}

// ── PERFORMANCE TAB FILTER ──
function perfAccepts(d) {
  if (ddIsFiltered('perf-type') && !ddMatch('perf-type', d.campaign.type)) return false;
  if (ddIsFiltered('perf-sender') && !ddMatch('perf-sender', d.campaign.sender || '(none)')) return false;
  if (ddIsFiltered('perf-campaign') && !ddMatch('perf-campaign', d.campaign.id)) return false;
  return true;
}

// ── STEP TAB ──
function setStepChannel(ch) {
  stepChannel = ch;
  var btns = document.querySelectorAll('#stepChannelToggle .ch-toggle-btn');
  btns.forEach(function(b, i) {
    var vals = ['both', 'linkedin', 'email'];
    b.classList.toggle('active', vals[i] === ch);
  });
  renderSteps();
}

function stepAccepts(d) {
  if (ddIsFiltered('step-campaign') && !ddMatch('step-campaign', d.campaign.id)) return false;
  return true;
}

// ── INIT DROPDOWNS ──
function initAllDropdowns() {
  // Performance tab: types
  var types = {};
  RAW_DATA.campaigns.forEach(function(c) {
    if (c.type && c.type !== 'undefined') types[c.type] = true;
  });
  var typeOpts = Object.keys(types).sort().map(function(t) { return {id: t, label: t}; });
  ddInit('perf-type', typeOpts, renderPerf);

  // Performance tab: senders
  var senders = {};
  RAW_DATA.campaigns.forEach(function(c) {
    var s = c.sender || '(none)';
    senders[s] = true;
  });
  var senderOpts = Object.keys(senders).sort().map(function(s) { return {id: s, label: s}; });
  ddInit('perf-sender', senderOpts, renderPerf);

  // Performance tab: campaigns
  var campOpts = RAW_DATA.campaigns.map(function(c) {
    return {id: c.id, label: c.name};
  });
  ddInit('perf-campaign', campOpts, renderPerf);

  // Step tab: campaigns
  ddInit('step-campaign', campOpts, renderSteps);
}

// Click outside closes dropdowns
document.addEventListener('click', function(e) {
  var inside = false;
  var el = e.target;
  while (el) {
    if (el.classList && (el.classList.contains('filter-dropdown') || el.classList.contains('dd-btn'))) {
      inside = true;
      break;
    }
    el = el.parentElement;
  }
  if (!inside) {
    Object.keys(ddState).forEach(function(k) {
      document.getElementById(k + '-panel').classList.remove('open');
    });
  }
});

// ── RENDER ALL ──
function renderAll() {
  renderOverview();
  renderPerf();
  renderSteps();
  renderCopy();
  renderAB();
  renderTrends();
  renderEmail();
  renderRaw();
}

// ── OVERVIEW ──
function renderOverview() {
  var data = getFiltered();
  var totalSent = 0, totalReplies = 0, totalEmails = 0, totalEReplies = 0, totalInterested = 0;
  var allLeads = {};
  data.forEach(function(d) {
    totalSent += uniqueLeads(d.activities, 'message_sent');
    totalReplies += uniqueLeads(d.activities, 'message_replied');
    totalEmails += uniqueLeads(d.activities, 'email_sent');
    totalEReplies += uniqueLeads(d.activities, 'email_replied');
    totalInterested += uniqueLeads(d.activities, 'interested');
    d.activities.forEach(function(a) { if (a.lead_id) allLeads[a.lead_id] = true; });
  });
  var pipelineCount = Object.keys(allLeads).length;

  document.getElementById('overviewStats').innerHTML =
    '<div class="stat"><div class="stat-value">' + fmtNum(pipelineCount) + '</div><div class="stat-label">Pipeline Leads</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(totalSent) + '</div><div class="stat-label">LinkedIn DMs Sent</div></div>' +
    '<div class="stat"><div class="stat-value" style="color:var(--success)">' + fmtNum(totalReplies) + '</div><div class="stat-label">DM Replies</div><div class="stat-delta">' + fmtPct(totalReplies, totalSent) + ' reply rate</div></div>' +
    '<div class="stat"><div class="stat-value" style="color:var(--accent2)">' + fmtNum(totalInterested) + '</div><div class="stat-label">Marked Interested</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(totalEmails) + '</div><div class="stat-label">Emails Sent</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(totalEReplies) + '</div><div class="stat-label">Email Replies</div><div class="stat-delta">' + fmtPct(totalEReplies, totalEmails) + '</div></div>';

  var insights = [];
  var replyRate = totalSent > 0 ? totalReplies / totalSent * 100 : 0;
  insights.push('<div class="insight insight-info">Maturity: excluding activity newer than <strong>' + maturityDays + 'd</strong>. ' + pipelineCount + ' leads in pipeline with mature activity.</div>');
  if (replyRate >= 10) insights.push('<div class="insight insight-good">LinkedIn DM reply rate: ' + replyRate.toFixed(1) + '% — above 10% benchmark.</div>');
  else if (replyRate >= 5) insights.push('<div class="insight insight-warn">LinkedIn DM reply rate: ' + replyRate.toFixed(1) + '% — at benchmark (5-10%).</div>');
  else insights.push('<div class="insight insight-bad">LinkedIn DM reply rate: ' + replyRate.toFixed(1) + '% — below 5% benchmark.</div>');
  document.getElementById('overviewInsights').innerHTML = insights.join('');
}

// ── PERFORMANCE BY CHANNEL ──
function renderPerf() {
  var data = getFiltered();
  // Enrich with computed values
  var enriched = [];
  data.forEach(function(d) {
    var c = d.campaign;
    var acts = d.activities;
    var invites = uniqueLeads(acts, 'invite_sent');
    var accepts = uniqueLeads(acts, 'invite_accepted');
    var sent = uniqueLeads(acts, 'message_sent');
    var replies = uniqueLeads(acts, 'message_replied');
    var emails = uniqueLeads(acts, 'email_sent');
    var eReplies = uniqueLeads(acts, 'email_replied');
    var interested = uniqueLeads(acts, 'interested');
    var pl = pipelineLeads(c, acts);
    if (c.lead_count === 0 && pl === 0 && c.status !== 'running') return;
    enriched.push({campaign: c, invites: invites, accepts: accepts, sent: sent, replies: replies, emails: emails, eReplies: eReplies, interested: interested, pl: pl});
  });

  // Filter
  var filtered = enriched.filter(function(d) { return perfAccepts(d); });

  // Sort
  filtered = applySort(filtered, perfSortCol, perfSortDir, perfExtract);

  // Compute totals (from filtered data)
  var t = {invites: 0, accepts: 0, sent: 0, replies: 0, emails: 0, eReplies: 0, interested: 0, pl: 0, leads: 0};
  filtered.forEach(function(d) {
    t.invites += d.invites;
    t.accepts += d.accepts;
    t.sent += d.sent;
    t.replies += d.replies;
    t.emails += d.emails;
    t.eReplies += d.eReplies;
    t.interested += d.interested;
    t.pl += d.pl;
    t.leads += d.campaign.lead_count;
  });

  // Build rows
  var rows = '';

  // Totals row
  rows += '<tr class="total-row">' +
    '<td class="td-campaign" style="font-weight:700;">TOTAL (' + filtered.length + ' campaigns)</td>' +
    '<td class="td-type">—</td>' +
    '<td>—</td>' +
    '<td class="td-num">' + fmtNum(t.leads) + '</td>' +
    '<td class="td-num">' + fmtNum(t.pl) + '</td>' +
    '<td>' + compactCell(t.invites, t.accepts, 'invite') + '</td>' +
    '<td>' + compactCell(t.sent, t.replies, 'dm') + '</td>' +
    '<td>' + emailCell(t.emails, t.eReplies) + '</td>' +
    '<td class="td-num">' + fmtNum(t.interested) + '</td>' +
    '<td style="font-size:0.72rem;color:var(--muted);">—</td>' +
    '</tr>';

  // Separator
  rows += '<tr class="total-sep"><td colspan="10"></td></tr>';

  // Data rows
  filtered.forEach(function(d) {
    var c = d.campaign;
    var lastAct = c.last_activity ? c.last_activity.split('T')[0] : 'Never';
    rows += '<tr>' +
      '<td class="td-campaign" title="' + c.name.replace(/"/g, '&quot;') + '">' + c.name + '</td>' +
      '<td class="td-type">' + c.type + '</td>' +
      '<td>' + (c.sender || '') + '</td>' +
      '<td class="td-num">' + fmtNum(c.lead_count) + '</td>' +
      '<td class="td-num">' + fmtNum(d.pl) + '</td>' +
      '<td>' + compactCell(d.invites, d.accepts, 'invite') + '</td>' +
      '<td>' + compactCell(d.sent, d.replies, 'dm') + '</td>' +
      '<td>' + emailCell(d.emails, d.eReplies) + '</td>' +
      '<td class="td-num">' + fmtNum(d.interested) + '</td>' +
      '<td style="font-size:0.72rem;color:var(--muted);">' + lastAct + '</td>' +
      '</tr>';
  });
  document.getElementById('perfBody').innerHTML = rows;
}

// ── PERFORMANCE BY STEP ──
function renderSteps() {
  var data = getFiltered();
  // Build per-campaign: invite + ordered message steps
  var stepData = {};
  var globalMaxMsg = 0;
  data.forEach(function(d) {
    var cid = d.campaign.id;
    if (!stepData[cid]) {
      stepData[cid] = {
        name: d.campaign.name, id: cid,
        inviteSent: {}, inviteAccepted: {},
        msgSteps: {}
      };
    }
    var sd = stepData[cid];
    d.activities.forEach(function(a) {
      var sn = a.sequence_step;
      if (sn === undefined || sn === null) return;
      if (a.step === 'visit') return;
      var lid = a.lead_id;
      if (a.step === 'invite_sent' && lid) sd.inviteSent[lid] = true;
      if (a.step === 'invite_accepted' && lid) sd.inviteAccepted[lid] = true;
      if (a.step === 'message_sent' || a.step === 'message_replied' ||
          a.step === 'email_sent' || a.step === 'email_replied') {
        if (!sd.msgSteps[sn]) sd.msgSteps[sn] = {dmSent:{}, dmReplied:{}, emailSent:{}, emailReplied:{}};
        var ms = sd.msgSteps[sn];
        if (a.step === 'message_sent' && lid) ms.dmSent[lid] = true;
        if (a.step === 'message_replied' && lid) ms.dmReplied[lid] = true;
        if (a.step === 'email_sent' && lid) ms.emailSent[lid] = true;
        if (a.step === 'email_replied' && lid) ms.emailReplied[lid] = true;
        if (sn > globalMaxMsg) globalMaxMsg = sn;
      }
    });
  });

  // Convert to array and filter by campaign
  var stepArr = [];
  Object.keys(stepData).forEach(function(cid) {
    var sd = stepData[cid];
    stepArr.push(sd);
  });
  stepArr = stepArr.filter(function(sd) {
    return stepAccepts({campaign: {id: sd.id}}); // wrap for stepAccepts
  });

  // Compute totals across filtered campaigns
  var totals = {invSent: 0, invAcc: 0, msgSteps: {}};
  stepArr.forEach(function(sd) {
    totals.invSent += Object.keys(sd.inviteSent).length;
    totals.invAcc += Object.keys(sd.inviteAccepted).length;
    Object.keys(sd.msgSteps).forEach(function(sn) {
      if (!totals.msgSteps[sn]) totals.msgSteps[sn] = {dmS:0, dmR:0, emS:0, emR:0};
      var ms = sd.msgSteps[sn];
      totals.msgSteps[sn].dmS += Object.keys(ms.dmSent).length;
      totals.msgSteps[sn].dmR += Object.keys(ms.dmReplied).length;
      totals.msgSteps[sn].emS += Object.keys(ms.emailSent).length;
      totals.msgSteps[sn].emR += Object.keys(ms.emailReplied).length;
    });
  });

  // Build table: column 0 = Connect, columns 1..N = Msg N
  var html = '<table><thead><tr><th>Campaign</th><th>Connect</th>';
  for (var m = 1; m <= globalMaxMsg + 1; m++) {
    html += '<th>Msg ' + m + '</th>';
  }
  html += '</tr></thead><tbody>';

  // Totals row
  html += '<tr class="total-row"><td class="td-campaign" style="font-weight:700;">TOTAL (' + stepArr.length + ' campaigns)</td>';
  html += '<td>' + compactCell(totals.invSent, totals.invAcc, 'invite') + '</td>';
  for (var mi = 0; mi <= globalMaxMsg; mi++) {
    var tms = totals.msgSteps[mi] || {dmS:0, dmR:0, emS:0, emR:0};
    var tcell = '';
    if (stepChannel !== 'email' && tms.dmS > 0) tcell += compactCell(tms.dmS, tms.dmR, 'dm');
    if (stepChannel !== 'linkedin' && tms.emS > 0) tcell += (tcell ? '<br>' : '') + emailCell(tms.emS, tms.emR);
    if (stepChannel === 'both' && tms.dmS > 0 && tms.emS > 0) {
      tcell += '<br>' + compactCell(tms.dmS + tms.emS, tms.dmR + tms.emR, 'combined');
    }
    html += '<td>' + (tcell || '<span style="color:var(--muted);font-size:0.78rem;">—</span>') + '</td>';
  }
  html += '</tr>';

  // Separator
  html += '<tr class="total-sep"><td colspan="' + (2 + globalMaxMsg + 1) + '"></td></tr>';

  // Data rows
  stepArr.forEach(function(sd) {
    html += '<tr><td class="td-campaign">' + sd.name + '</td>';

    var invSent = Object.keys(sd.inviteSent).length;
    var invAcc = Object.keys(sd.inviteAccepted).length;
    html += '<td>' + compactCell(invSent, invAcc, 'invite') + '</td>';

    var msgNums = Object.keys(sd.msgSteps).sort(function(a, b) { return a - b; });
    for (var mi = 0; mi <= globalMaxMsg; mi++) {
      var sn = msgNums[mi];
      if (sn !== undefined && sd.msgSteps[sn]) {
        var ms = sd.msgSteps[sn];
        var dmS = Object.keys(ms.dmSent).length;
        var dmR = Object.keys(ms.dmReplied).length;
        var emS = Object.keys(ms.emailSent).length;
        var emR = Object.keys(ms.emailReplied).length;
        var cell = '';
        if (stepChannel !== 'email' && dmS > 0) cell += compactCell(dmS, dmR, 'dm');
        if (stepChannel !== 'linkedin' && emS > 0) cell += (cell ? '<br>' : '') + emailCell(emS, emR);
        if (stepChannel === 'both' && dmS > 0 && emS > 0) {
          cell += '<br>' + compactCell(dmS + emS, dmR + emR, 'combined');
        }
        html += '<td>' + (cell || '<span style="color:var(--muted);font-size:0.78rem;">—</span>') + '</td>';
      } else {
        html += '<td style="color:var(--muted);font-size:0.78rem;">—</td>';
      }
    }
    html += '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('stepTable').innerHTML = html;
}

// ── COPY ANALYSIS ──
function normalizeMsg(msg) {
  if (!msg) return '';
  msg = msg.replace(/^\([^)]*\)\s*/, '');
  msg = msg.replace(/^(Hey|Hi|Hello|Hola)\s+[A-Z][a-zA-Z'\-]+(?:\s+[A-Z][a-zA-Z'\-]+)?\s*[,.]?\s*/, '');
  return msg.trim();
}

function renderCopy() {
  var groups = RAW_DATA.copy_groups || {};
  var copies = Object.values(groups);

  // Build sender filter buttons (from all copies)
  var allSenders = {};
  copies.forEach(function(g) {
    (g.senders || []).forEach(function(s) { allSenders[s] = true; });
  });
  var senderList = Object.keys(allSenders).sort();
  var filterHtml = '<button class="filter-btn' + (copyFilterSender === 'All' ? ' active' : '') + '" onclick="setCopyFilter(\'All\')">All</button>';
  senderList.forEach(function(s) {
    filterHtml += '<button class="filter-btn' + (copyFilterSender === s ? ' active' : '') + '" onclick="setCopyFilter(\'' + s.replace(/'/g, "\\'") + '\')">' + s + '</button>';
  });
  document.getElementById('copySenderFilter').innerHTML = filterHtml;

  // Update view toggle buttons
  var btnI = document.getElementById('copyViewIndiv');
  var btnG = document.getElementById('copyViewGroup');
  if (btnI) { btnI.className = 'filter-btn' + (copyViewMode === 'individual' ? ' active' : ''); }
  if (btnG) { btnG.className = 'filter-btn' + (copyViewMode === 'grouped' ? ' active' : ''); }

  if (copyViewMode === 'individual') {
    renderCopyIndividual(copies);
  } else {
    renderCopyGrouped(copies);
  }
}

function renderCopyIndividual(copies) {
  // Dynamic header
  document.getElementById('copyHeader').innerHTML = '<th>Copy (first 80 chars)</th><th>Senders</th><th>Sends</th><th>Replies</th><th>Rate</th>';

  // Filter by sender
  var filtered = copies;
  if (copyFilterSender !== 'All') {
    filtered = copies.filter(function(g) {
      return (g.senders || []).indexOf(copyFilterSender) >= 0;
    });
  }
  filtered.sort(function(a, b) { return (b.leads_sent || 0) - (a.leads_sent || 0); });

  var rows = '';
  filtered.forEach(function(g) {
    var sent = g.leads_sent || 0;
    if (sent === 0) return;
    var replied = g.leads_replied || 0;
    var rate = replied / sent * 100;
    var cls = rateColor(rate, 'linkedin');
    var label = (g.normalized_msg || '').substring(0, 80);

    rows += '<tr>' +
      '<td class="td-campaign" title="' + (g.normalized_msg || '').replace(/"/g, '&quot;') + '">' + label + '</td>' +
      '<td style="font-size:0.72rem;color:var(--muted);">' + (g.senders || []).join(', ') + '</td>' +
      '<td class="td-num">' + fmtNum(sent) + '</td>' +
      '<td class="td-num">' + fmtNum(replied) + '</td>' +
      '<td><span class="ch-rate ' + cls + '">' + rate.toFixed(1) + '%</span></td>' +
      '</tr>';
  });
  document.getElementById('copyBody').innerHTML = rows || '<tr><td colspan="5" style="color:var(--muted);">No copy data available</td></tr>';
}

function renderCopyGrouped(copies) {
  // Dynamic header
  document.getElementById('copyHeader').innerHTML = '<th>Copy Template (name-stripped)</th><th>Variants</th><th>Camps</th><th>Senders</th><th>Sends</th><th>Replies</th><th>Rate</th>';

  // Re-group by normalized message with fuzzy key
  var templateMap = {};
  copies.forEach(function(g) {
    var msg = g.normalized_msg || '';
    var template = normalizeMsg(msg);
    if (!template) template = msg;

    // Build fuzzy key: lowercase, normalize variants, strip punctuation, first 50 chars
    var key = template.toLowerCase();
    key = key.replace(/going on in /g, 'going in ');
    key = key.replace(/thanks for connecting/gi, 'appreciate you connecting');
    key = key.replace(/[^a-z0-9 ]/g, ' ');
    key = key.replace(/\s+/g, ' ').trim();
    key = key.substring(0, 50);
    if (!key) return;

    if (!templateMap[key]) {
      templateMap[key] = {
        template: template.substring(0, 100),
        total_sent: 0, total_replies: 0,
        senders: {}, campaigns: {}, variants: 0
      };
    }
    var t = templateMap[key];
    t.total_sent += (g.leads_sent || 0);
    t.total_replies += (g.leads_replied || 0);
    (g.senders || []).forEach(function(s) { t.senders[s] = true; });
    (g.campaigns || []).forEach(function(c) { t.campaigns[c] = true; });
    t.variants++;
  });

  var templates = Object.values(templateMap);

  // Filter by sender
  var filtered = templates;
  if (copyFilterSender !== 'All') {
    filtered = templates.filter(function(t) {
      return t.senders.hasOwnProperty(copyFilterSender);
    });
  }
  filtered.sort(function(a, b) { return b.total_sent - a.total_sent; });

  var rows = '';
  filtered.forEach(function(t) {
    if (!t.total_sent || t.total_sent === 0) return;
    var rate = t.total_replies / t.total_sent * 100;
    var cls = rateColor(rate, 'linkedin');
    var label = t.template.substring(0, 90);
    var senderNames = Object.keys(t.senders).sort().join(', ');
    var campCount = Object.keys(t.campaigns).length;

    rows += '<tr>' +
      '<td class="td-campaign" title="' + t.template.replace(/"/g, '&quot;') + '">' + label + '</td>' +
      '<td class="td-num">' + t.variants + '</td>' +
      '<td class="td-num">' + campCount + '</td>' +
      '<td style="font-size:0.72rem;color:var(--muted);">' + senderNames + '</td>' +
      '<td class="td-num">' + fmtNum(t.total_sent) + '</td>' +
      '<td class="td-num">' + fmtNum(t.total_replies) + '</td>' +
      '<td><span class="ch-rate ' + cls + '">' + rate.toFixed(1) + '%</span></td>' +
      '</tr>';
  });
  document.getElementById('copyBody').innerHTML = rows || '<tr><td colspan="7" style="color:var(--muted);">No copy data available</td></tr>';
}

function setCopyView(mode) {
  copyViewMode = mode;
  renderCopy();
}

function setCopyFilter(sender) {
  copyFilterSender = sender;
  renderCopy();
}

// ── A/B TESTS (detected from activity template_ids) ──
function renderAB() {
  // First pass: collect all activities by campaign+step+template
  // Store raw activities so we can extract message_text from the best source
  var abRaw = {};
  RAW_DATA.campaigns.forEach(function(c) {
    c.activities.forEach(function(a) {
      var tid = a.template_id || '';
      if (!tid) return;
      var step = a.sequence_step || 0;
      var key = c.id + '|' + step;
      if (!abRaw[key]) abRaw[key] = {campaign: c.name, step: step, templates: {}};
      if (!abRaw[key].templates[tid]) abRaw[key].templates[tid] = [];
      abRaw[key].templates[tid].push(a);
    });
  });

  // Second pass: build counts and find best message for each template
  var groups = [];
  Object.keys(abRaw).forEach(function(key) {
    var g = abRaw[key];
    var tids = Object.keys(g.templates);
    if (tids.length < 2) return;
    var variants = [];
    tids.forEach(function(tid) {
      var acts = g.templates[tid];
      var sent = {}, replied = {};
      var bestMsg = '';
      var channelTags = {};
      acts.forEach(function(a) {
        if (a.step === 'message_sent' || a.step === 'invite_sent' || a.step === 'email_sent') {
          sent[a.lead_id] = true;
        }
        if (a.step === 'message_replied' || a.step === 'invite_accepted' || a.step === 'email_replied') {
          replied[a.lead_id] = true;
        }
        // Track channel
        if (a.step === 'message_sent' || a.step === 'message_replied') channelTags['DM'] = true;
        if (a.step === 'invite_sent' || a.step === 'invite_accepted') channelTags['Invite'] = true;
        if (a.step === 'email_sent' || a.step === 'email_replied') channelTags['Email'] = true;
        // Best message: prefer message_sent with text
        if (a.message_text && (!bestMsg || a.step === 'message_sent')) {
          bestMsg = a.message_text;
        }
      });
      var sentCount = Object.keys(sent).length;
      if (sentCount === 0) return;
      var repliedCount = Object.keys(replied).length;
      // Build label: message text first, otherwise "Variant A/B/C"
      var chKeys = Object.keys(channelTags);
      var chBadge = '';
      if (chKeys.length > 0) {
        var chNames = {DM: 'LinkedIn', Invite: 'Connect', Email: 'Email'};
        chBadge = ' <span style="font-size:0.62rem;color:var(--muted);">' + chKeys.map(function(k) { return chNames[k] || k; }).join('+') + '</span>';
      }
      var label;
      if (bestMsg) {
        label = bestMsg.substring(0, 75);
      } else {
        label = 'Variant ' + String.fromCharCode(65 + variants.length);
      }
      variants.push({tid: tid, msg: label, chBadge: chBadge, sent: sentCount, replied: repliedCount});
    });
    if (variants.length >= 2) {
      variants.sort(function(a, b) { return b.sent - a.sent; });
      groups.push({campaign: g.campaign, step: g.step, variants: variants});
    }
  });
  groups.sort(function(a, b) { return a.campaign.localeCompare(b.campaign) || a.step - b.step; });

  // Summary
  var totalVariants = 0, notableTests = 0;
  groups.forEach(function(g) {
    totalVariants += g.variants.length;
    if (g.variants.length >= 2) {
      var rates = g.variants.map(function(v) { return v.sent > 0 ? v.replied/v.sent : 0; });
      var spread = Math.max.apply(null, rates) - Math.min.apply(null, rates);
      var totalSends = g.variants.reduce(function(s, v) { return s + v.sent; }, 0);
      if (spread > 0.10 && totalSends >= 15) notableTests++;
    }
  });

  document.getElementById('abSummary').innerHTML =
    '<div class="stats-grid">' +
    '<div class="stat"><div class="stat-value">' + groups.length + '</div><div class="stat-label">A/B Test Groups</div></div>' +
    '<div class="stat"><div class="stat-value">' + totalVariants + '</div><div class="stat-label">Copy Variants</div></div>' +
    '<div class="stat"><div class="stat-value">' + notableTests + '</div><div class="stat-label">Notable Spreads (>10pp)</div></div>' +
    '</div>';

  // Table: one row per variant, grouped by campaign-step
  var html = '<table><thead><tr><th>Campaign</th><th>Step</th><th>Variant</th><th>Sends</th><th>Replies</th><th>Rate</th></tr></thead><tbody>';
  groups.forEach(function(g) {
    var bestRate = 0;
    g.variants.forEach(function(v) {
      var r = v.sent > 0 ? v.replied/v.sent : 0;
      if (r > bestRate) bestRate = r;
    });
    var stepLabel = g.step === 0 ? 'Connect' : 'Msg ' + g.step;
    g.variants.forEach(function(v, vi) {
      var rate = v.sent > 0 ? v.replied/v.sent*100 : 0;
      var isBest = rate > 0 && Math.abs(rate/100 - bestRate) < 0.001;
      var rateCls = isBest ? 'ch-rate-good' : 'ch-rate-avg';
      var campaignCell = vi === 0 ? '<td class="td-campaign" rowspan="' + g.variants.length + '">' + g.campaign + '</td>' : '';
      var stepCell = vi === 0 ? '<td rowspan="' + g.variants.length + '">' + stepLabel + '</td>' : '';
      html += '<tr>' + campaignCell + stepCell +
        '<td style="font-size:0.75rem;max-width:340px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;" title="' + v.msg.replace(/"/g, '&quot;') + '">' + v.msg + v.chBadge + '</td>' +
        '<td class="td-num">' + v.sent + '</td>' +
        '<td class="td-num">' + v.replied + '</td>' +
        '<td><span class="ch-rate ' + rateCls + '">' + rate.toFixed(1) + '%</span>' + (isBest ? ' <span style="font-size:0.65rem;color:var(--success);">best</span>' : '') + '</td>' +
        '</tr>';
    });
  });
  html += '</tbody></table>';
  document.getElementById('abTable').innerHTML = html || '<p style="color:var(--muted);">No multi-variant copy tests detected.</p>';
}

// ── TRENDS ──
function renderTrends() {
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var weekData = {};

  RAW_DATA.campaigns.forEach(function(c) {
    c.activities.forEach(function(a) {
      var d = parseDate(a.date);
      if (!d) return;
      // Monday of this week
      var day = d.getDay() || 7;
      var mon = new Date(d);
      mon.setDate(d.getDate() - day + 1);
      mon.setHours(0,0,0,0);
      var key = mon.getTime();
      if (!weekData[key]) weekData[key] = {min: d, max: d, sent: 0, replies: 0};
      if (d < weekData[key].min) weekData[key].min = d;
      if (d > weekData[key].max) weekData[key].max = d;
      if (a.step === 'message_sent') weekData[key].sent++;
      if (a.step === 'message_replied') weekData[key].replies++;
    });
  });

  var sorted = Object.keys(weekData).sort(function(a, b) { return a - b; }).slice(-12).map(function(k) {
    var w = weekData[k];
    var f = w.min, l = w.max;
    var label = months[f.getMonth()] + ' ' + f.getDate();
    if (f.getTime() !== l.getTime()) {
      label += (f.getMonth() !== l.getMonth() ? '–' + months[l.getMonth()] + ' ' : '–') + l.getDate();
    }
    return {label: label, sent: w.sent, replies: w.replies};
  });

  var maxSent = Math.max.apply(null, sorted.map(function(w) { return w.sent; }).concat([1]));

  var volHtml = '';
  sorted.forEach(function(w) {
    var pct = w.sent / maxSent * 100;
    volHtml += '<div class="bar-row"><div class="bar-label-w">' + w.label + '</div><div class="bar-track"><div class="bar-fill" style="width:' + Math.max(pct, 2) + '%;background:var(--accent);">' + (pct > 15 ? w.sent : '') + '</div></div><div class="bar-val">' + w.sent + '</div></div>';
  });
  document.getElementById('weeklyVolume').innerHTML = volHtml;

  var maxRate = Math.max.apply(null, sorted.map(function(w) { return w.sent > 0 ? w.replies/w.sent*100 : 0; }).concat([1]));
  var rateHtml = '';
  sorted.forEach(function(w) {
    var rate = w.sent > 0 ? w.replies / w.sent * 100 : 0;
    var pct = rate / maxRate * 100;
    rateHtml += '<div class="bar-row"><div class="bar-label-w">' + w.label + '</div><div class="bar-track"><div class="bar-fill" style="width:' + Math.max(pct, 2) + '%;background:var(--success);">' + (pct > 15 ? rate.toFixed(1) + '%' : '') + '</div></div><div class="bar-val">' + rate.toFixed(1) + '%</div></div>';
  });
  document.getElementById('weeklyRate').innerHTML = rateHtml;
}

// ── EMAIL ──
function renderEmail() {
  var dnsStart = new Date(dnsFixDate);
  document.getElementById('dnsWindow').textContent = dnsStart.toISOString().split('T')[0];

  var data = getFiltered();
  var preSends = 0, preReplies = 0, postSends = 0, postReplies = 0;
  var campEmail = {};

  data.forEach(function(d) {
    var c = d.campaign;
    var cp = {name: c.name, preS: {}, preR: {}, postS: {}, postR: {}};
    d.activities.forEach(function(a) {
      var ad = parseDate(a.date);
      if (!ad) return;
      var isPost = ad >= dnsStart;
      var lid = a.lead_id;
      if (a.step === 'email_sent' && lid) {
        if (isPost) cp.postS[lid] = true; else cp.preS[lid] = true;
      }
      if (a.step === 'email_replied' && lid) {
        if (isPost) cp.postR[lid] = true; else cp.preR[lid] = true;
      }
    });
    var preS = Object.keys(cp.preS).length;
    var preR = Object.keys(cp.preR).length;
    var postS = Object.keys(cp.postS).length;
    var postR = Object.keys(cp.postR).length;
    preSends += preS; preReplies += preR; postSends += postS; postReplies += postR;
    if (preS + postS > 0) campEmail[c.name] = {preS: preS, preR: preR, postS: postS, postR: postR};
  });

  var preRate = preSends > 0 ? preReplies / preSends * 100 : 0;
  var postRate = postSends > 0 ? postReplies / postSends * 100 : 0;
  var preCls = preSends > 0 ? rateColor(preRate, 'email') : 'ch-rate-avg';
  var postCls = postSends > 0 ? rateColor(postRate, 'email') : 'ch-rate-avg';

  document.getElementById('emailStats').innerHTML =
    '<div class="stat"><div class="stat-value">' + fmtNum(preSends) + '</div><div class="stat-label">Pre-DNS Sends</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(preReplies) + '</div><div class="stat-label">Pre-DNS Replies</div><div class="stat-delta"><span class="ch-rate ' + preCls + '">' + (preSends > 0 ? preRate.toFixed(1) + '%' : '—') + '</span> vs ' + emailTarget + '% target</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(postSends) + '</div><div class="stat-label">Post-DNS Sends</div></div>' +
    '<div class="stat"><div class="stat-value">' + fmtNum(postReplies) + '</div><div class="stat-label">Post-DNS Replies</div><div class="stat-delta"><span class="ch-rate ' + postCls + '">' + (postSends > 0 ? postRate.toFixed(1) + '%' : '—') + '</span> vs ' + emailTarget + '% target</div></div>';

  var ins = [];
  if (postSends > 0 && preSends > 0 && postRate > preRate * 1.5) {
    ins.push('<div class="insight insight-good">Post-DNS reply rate (' + postRate.toFixed(1) + '%) is meaningfully higher than pre-DNS (' + preRate.toFixed(1) + '%).</div>');
  } else if (postSends > 20 && postRate <= preRate) {
    ins.push('<div class="insight insight-warn">Post-DNS reply rate has not improved over pre-DNS. Verify the DNS fix date.</div>');
  }
  ins.push('<div class="insight insight-info">Maturity filter: ' + maturityDays + 'd · DNS fix: ' + dnsStart.toISOString().split('T')[0] + ' · Rates vs ' + emailTarget + '% email target.</div>');
  document.getElementById('emailInsights').innerHTML = ins.join('');

  // Campaign breakdown — sorted by total sends
  var campList = Object.keys(campEmail).map(function(name) {
    var cp = campEmail[name];
    return {name: name, preS: cp.preS, preR: cp.preR, postS: cp.postS, postR: cp.postR, total: cp.preS + cp.postS};
  }).sort(function(a, b) { return b.total - a.total; });

  var erows = '';
  campList.forEach(function(cp) {
    var rate = cp.total > 0 ? (cp.preR + cp.postR) / cp.total * 100 : 0;
    var cls = rateColor(rate, 'email');
    erows += '<tr><td class="td-campaign">' + cp.name + '</td><td class="td-num">' + fmtNum(cp.preS) + '</td><td class="td-num">' + fmtNum(cp.preR) + '</td><td class="td-num">' + fmtNum(cp.postS) + '</td><td class="td-num">' + fmtNum(cp.postR) + '</td><td><span class="ch-rate ' + cls + '">' + (cp.total > 0 ? rate.toFixed(1) + '%' : '—') + '</span></td></tr>';
  });
  document.getElementById('emailBody').innerHTML = erows || '<tr><td colspan="6" style="color:var(--muted);">No email activity in filtered data.</td></tr>';
}

// ── RAW DATA ──
function renderRaw() {
  var html = '<table><thead><tr><th>Campaign</th><th>Status</th><th>Type</th><th>Sender</th><th>Leads</th><th>Activities</th><th>Manual</th><th>First</th><th>Last</th></tr></thead><tbody>';
  RAW_DATA.campaigns.forEach(function(c) {
    html += '<tr>' +
      '<td class="td-campaign">' + c.name + '</td>' +
      '<td>' + c.status + '</td>' +
      '<td class="td-type">' + c.type + '</td>' +
      '<td>' + (c.sender || '') + '</td>' +
      '<td class="td-num">' + fmtNum(c.lead_count) + '</td>' +
      '<td class="td-num">' + fmtNum(c.activities.length) + '</td>' +
      '<td>' + (c.has_manual ? 'Yes' : 'No') + '</td>' +
      '<td style="font-size:0.72rem;color:var(--muted);">' + (c.first_activity || '?').split('T')[0] + '</td>' +
      '<td style="font-size:0.72rem;color:var(--muted);">' + (c.last_activity || '?').split('T')[0] + '</td>' +
      '</tr>';
  });
  html += '</tbody></table>';
  document.getElementById('rawList').innerHTML = html;
}

// ── TAB SWITCHING ──
function switchTab(tab) {
  document.querySelectorAll('.tab').forEach(function(t) { t.classList.remove('active'); });
  document.querySelectorAll('.tab-content').forEach(function(t) { t.classList.remove('active'); });
  if (event && event.target) event.target.classList.add('active');
  var content = document.getElementById('tab-' + tab);
  if (content) content.classList.add('active');
}

// ── EVENT LISTENERS ──
document.getElementById('maturitySlider').addEventListener('input', function(e) {
  maturityDays = parseInt(e.target.value);
  document.getElementById('maturityVal').textContent = maturityDays;
  renderAll();
});

document.getElementById('dnsDate').addEventListener('change', function(e) {
  dnsFixDate = new Date(e.target.value);
  renderAll();
});

// Benchmark sliders
document.getElementById('inviteTarget').addEventListener('input', function(e) {
  inviteTarget = parseInt(e.target.value);
  document.getElementById('inviteTargetVal').textContent = inviteTarget;
  renderAll();
});
document.getElementById('dmTarget').addEventListener('input', function(e) {
  dmTarget = parseInt(e.target.value);
  document.getElementById('dmTargetVal').textContent = dmTarget;
  renderAll();
});
document.getElementById('emailTarget').addEventListener('input', function(e) {
  emailTarget = parseInt(e.target.value);
  document.getElementById('emailTargetVal').textContent = emailTarget;
  renderAll();
});

initAllDropdowns();
renderAll();
</script>
</body>
</html>
''')

# ── Write ──
html = ''.join(P)
with open(OUT_PATH, 'w') as f:
    f.write(html)

# Validate
print(f"Written: {len(html):,} bytes")
checks = [
    ('DOCTYPE', html.startswith('<!DOCTYPE html>')),
    ('</html>', html.rstrip().endswith('</html>')),
    ('<script>', html.count('<script>') == 1),
    ('</script>', html.count('</script>') == 1),
]
all_ok = True
for name, ok in checks:
    s = "OK" if ok else "FAIL"
    if not ok: all_ok = False
    print(f"  {name}: {s}")
print("VALID" if all_ok else "INVALID")
