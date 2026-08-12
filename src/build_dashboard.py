"""
Inline the real dashboard_data.json + Plotly into the dashboard template,
producing the final self-contained dashboard/dashboard.html (works offline, file://).
Run after any data regeneration:  python src/build_dashboard.py
"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASH = os.path.join(ROOT, "dashboard")

html = open(os.path.join(DASH, "dashboard_template.html"), encoding="utf-8").read()
data = open(os.path.join(DASH, "dashboard_data.json"), encoding="utf-8").read()

# 1. swap the embedded sample for the real data
new, n = re.subn(r'const DATA = \{.*?\};', lambda m: 'const DATA = ' + data + ';',
                 html, count=1, flags=re.DOTALL)
assert n == 1, "DATA block not found in template"

# 2. inline Plotly, replacing the CDN script tag
import plotly
pjs = plotly.offline.get_plotlyjs()
cdn = re.search(r'<script src="https://cdn\.plot\.ly/[^"]+"[^>]*></script>', new)
assert cdn, "CDN plotly tag not found"
new = new.replace(cdn.group(0), "<script>" + pjs + "</script>", 1)

out = os.path.join(DASH, "dashboard.html")
open(out, "w", encoding="utf-8", newline="").write(new)
print("wrote %s  (%.1f MB)" % (out, os.path.getsize(out) / 1e6))
