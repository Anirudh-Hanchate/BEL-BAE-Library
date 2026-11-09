import base64
import os

with open('bel_logo.jpg', 'rb') as f:
    logo_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

with open('chart.min.js', 'r', encoding='utf-8') as f:
    chart_js_code = f.read()

with open('all.min.css', 'r', encoding='utf-8') as f:
    fa_css_code = f.read()

with open('BAE_BEL_Library_HighTech_Dashboard.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Inline FontAwesome CSS
html = html.replace('<link rel="stylesheet" href="all.min.css">', f'<style>\n{fa_css_code}\n</style>')

# Inline Chart.js JavaScript
html = html.replace('<script src="chart.min.js"></script>', f'<script>\n{chart_js_code}\n</script>')

# Inline BEL Logo image
html = html.replace('src="bel_logo.jpg"', f'src="{logo_b64}"')

out_file = 'BAE_BEL_Library_Dashboard_Standalone.html'
with open(out_file, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"Standalone HTML generated: {out_file} ({round(os.path.getsize(out_file)/1024, 1)} KB)")

