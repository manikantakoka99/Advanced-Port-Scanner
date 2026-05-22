from jinja2 import Template
from datetime import datetime
import os

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<title>Port Scan Report - {{ host }}</title>
<style>
  body  { font-family: Arial; background:#0d1117; color:#c9d1d9; padding:30px; }
  h1    { color:#58a6ff; }
  h2    { color:#58a6ff; border-bottom:1px solid #30363d; padding-bottom:8px; }
  table { width:100%; border-collapse:collapse; margin-top:15px; }
  th    { background:#161b22; color:#58a6ff; padding:12px; text-align:left; }
  td    { padding:10px; border-bottom:1px solid #21262d; }
  tr:hover { background:#161b22; }
  .HIGH   { color:#ff7b72; font-weight:bold; }
  .MEDIUM { color:#e3b341; font-weight:bold; }
  .LOW    { color:#3fb950; }
  .stat   { background:#161b22; padding:15px; border-radius:8px;
            display:inline-block; margin:10px; text-align:center; }
  .num    { font-size:2em; color:#58a6ff; font-weight:bold; }
</style>
</head>
<body>

<h1>🔍 Port Scan Report</h1>

<div class="stat">
  <div class="num">{{ target }}</div>
  <div>Target</div>
</div>
<div class="stat">
  <div class="num">{{ ip }}</div>
  <div>IP Address</div>
</div>
<div class="stat">
  <div class="num">{{ ports|length }}</div>
  <div>Open Ports</div>
</div>
<div class="stat">
  <div class="num">{{ date }}</div>
  <div>Scan Date</div>
</div>

<h2>Open Ports</h2>
<table>
  <tr>
    <th>Port</th>
    <th>Service</th>
    <th>Risk Level</th>
    <th>Banner</th>
  </tr>
  {% for p in ports %}
  <tr>
    <td><strong>{{ p.port }}</strong></td>
    <td>{{ p.service }}</td>
    <td class="{{ p.risk }}">{{ p.risk }}</td>
    <td style="font-family:monospace;font-size:0.85em">{{ p.banner }}</td>
  </tr>
  {% endfor %}
</table>

{% set high = ports | selectattr('risk','eq','HIGH') | list %}
{% if high %}
<h2>⚠️ High Risk Ports Detected</h2>
<table>
  <tr><th>Port</th><th>Service</th><th>Why Risky</th></tr>
  {% for p in high %}
  <tr>
    <td class="HIGH">{{ p.port }}</td>
    <td>{{ p.service }}</td>
    <td>
      {% if p.port == 23  %}Telnet sends data in plaintext{% endif %}
      {% if p.port == 21  %}FTP often misconfigured, allows anon login{% endif %}
      {% if p.port == 445 %}SMB — EternalBlue, ransomware target{% endif %}
      {% if p.port == 3389%}RDP — brute force target{% endif %}
      {% if p.port == 135 %}RPC — lateral movement vector{% endif %}
      {% if p.port == 139 %}NetBIOS — legacy, often exploitable{% endif %}
      {% if p.port == 5900 %}VNC — often no auth required{% endif %}
    </td>
  </tr>
  {% endfor %}
</table>
{% endif %}

</body>
</html>
"""

def generate_report(host, ip, ports):
    os.makedirs("reports", exist_ok=True)

    template = Template(TEMPLATE)
    html = template.render(
        target=host,
        ip=ip,
        ports=ports,
        date=datetime.now().strftime("%Y-%m-%d %H:%M")
    )

    filename = f"reports/{host}_{datetime.now().strftime('%Y%m%d_%H%M')}.html"
    with open(filename, "w") as f:
        f.write(html)

    print(f"\n[+] Report saved: {filename}")
    return filename
