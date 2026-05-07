#!/usr/bin/env python3
"""Validate dashboard v4 before opening."""
import json, re

with open('context/drop-zone/Muir Campaign Performance - Standalone.html') as f:
    html = f.read()

print(f"File size: {len(html):,} bytes")

# HTML structure
sc_open = html.count('<script>')
sc_close = html.count('</script>')
body_open = html.count('<body>')
body_close = html.count('</body>')
print(f"<script>: {sc_open}, </script>: {sc_close}")
print(f"<body>: {body_open}, </body>: {body_close}")

# Extract and validate JSON (ends at ;\nvar maturityDays)
data_start = html.find('var RAW_DATA = ') + len('var RAW_DATA = ')
data_end = html.find(';\nvar maturityDays', data_start)
raw_json = html[data_start:data_end]
print(f"\nJSON: {len(raw_json):,} chars at {data_start}-{data_end}")

try:
    model = json.loads(raw_json)
    print(f"  VALID: {len(model['campaigns'])} campaigns, {model['total_activities']} activities")
    print(f"  copy_groups: {len(model.get('copy_groups', {}))} entries")
except json.JSONDecodeError as e:
    print(f"  ERROR: {e}")
    exit(1)

# JS block
js_start = html.find('<script>') + 8
js_end = html.find('</script>')
js = html[js_start:js_end]
print(f"JS: {len(js):,} chars")

# Required functions
funcs = [
    'parseDate', 'isMature', 'compactCell', 'emailCell', 'rateColor',
    'getFiltered', 'uniqueLeads', 'pipelineLeads', 'renderAll',
    'renderOverview', 'renderPerf', 'renderSteps', 'renderCopy',
    'renderAB', 'renderTrends', 'renderEmail', 'renderRaw',
    'renderFunnel', 'setFunnelChannel',
    'switchTab', 'setCopyFilter'
]
missing = []
for fn in funcs:
    if 'function ' + fn in js:
        print(f"  {fn}() ✓")
    else:
        missing.append(fn)
        print(f"  {fn}() MISSING!")

# Tab divs
tabs = ['perf', 'steps', 'funnel', 'copy', 'ab', 'trends', 'email', 'raw']
for tab in tabs:
    if f'id="tab-{tab}"' in html:
        print(f"  tab-{tab} div ✓")
    else:
        missing.append(f'tab-{tab} div')
        print(f"  tab-{tab} div MISSING!")

# Element IDs
ids = [
    'overviewStats', 'overviewInsights', 'perfBody', 'stepTable',
    'funnelVis', 'funnelMeta', 'funnelChannelToggle',
    'copySenderFilter', 'copyBody', 'abSummary', 'abTable',
    'weeklyVolume', 'weeklyRate', 'emailStats', 'emailInsights',
    'emailBody', 'rawList', 'maturitySlider', 'maturityVal',
    'dnsDate', 'dnsWindow'
]
for eid in ids:
    if f'id="{eid}"' not in html:
        missing.append(f'id={eid}')
        print(f"  id={eid} MISSING!")

# renderAll() call
if 'renderAll();' in js:
    print(f"  renderAll() call ✓")
else:
    missing.append('renderAll() call')

# Quote balance
single = js.count("'")
double = js.count('"')
print(f"  Quotes: '={single} \"={double}")
if single % 2 != 0:
    missing.append(f'unbalanced single quotes ({single})')
if double % 2 != 0:
    missing.append(f'unbalanced double quotes ({double})')

print(f"\n{'='*50}")
if missing:
    print(f"ISSUES ({len(missing)}):")
    for m in missing:
        print(f"  X {m}")
else:
    print("ALL CHECKS PASSED")
