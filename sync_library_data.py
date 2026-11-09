# ==============================================================================
# BHARAT ELECTRONICS LIMITED (BEL) - BAE ACADEMICS & EXCELLENCE
# COMPLETE INTRANET SYNC & STANDALONE HTML BUNDLER ENGINE
# ==============================================================================

import openpyxl
import json
import base64
import os
import sys
from datetime import datetime

EXCEL_FILE = 'BAE_BEL_Library_Management_System_Final.xlsx'
STANDALONE_HTML = 'BAE_BEL_Library_Dashboard_Standalone.html'
BASE_HTML = 'BAE_BEL_Library_HighTech_Dashboard.html'
LOGO_FILE = 'bel_logo.jpg'
CHART_FILE = 'chart.min.js'
FA_FILE = 'all.min.css'

def sync_and_bundle():
    print("=" * 70)
    print(" BAE - BEL LIBRARY INTRANET 1-CLICK SYNC & BUNDLE ENGINE")
    print("=" * 70)

    if not os.path.exists(EXCEL_FILE):
        print(f"[ERROR] Excel file '{EXCEL_FILE}' not found!")
        return

    print(f"[*] Step 1: Reading records from '{EXCEL_FILE}'...")
    try:
        wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    except PermissionError:
        print(f"[WARNING] '{EXCEL_FILE}' is currently open in Excel. Please save and close it, then re-run.")
        return

    ws = wb['Book Register']
    books = []

    for r in range(5, 2000):
        serial = ws.cell(row=r, column=1).value
        title = ws.cell(row=r, column=2).value
        if not serial or not title:
            # Check if there is an empty line or end of data
            if not ws.cell(row=r+1, column=1).value:
                break
            continue

        wing = ws.cell(row=r, column=3).value or 'General'
        status = ws.cell(row=r, column=4).value or 'Available'
        borrower = ws.cell(row=r, column=5).value or '-'
        staff_id = ws.cell(row=r, column=6).value or '-'
        issue_type = ws.cell(row=r, column=7).value or '-'
        due_date = ws.cell(row=r, column=10).value or '-'
        shelf = ws.cell(row=r, column=13).value or 'Shelf Location'

        if isinstance(due_date, datetime):
            due_str = due_date.strftime('%Y-%m-%d')
        else:
            due_str = str(due_date).strip()

        overdue = False
        if status == 'Issued' and due_str not in ['-', 'N/A', 'Permanent', '']:
            try:
                parsed_due = datetime.strptime(due_str[:10], '%Y-%m-%d')
                if datetime.now() > parsed_due:
                    overdue = True
            except:
                pass

        books.append({
            'serial': str(serial).strip(),
            'title': str(title).strip(),
            'author': 'BAE Publication',
            'wing': str(wing).strip(),
            'status': str(status).strip(),
            'borrower': str(borrower).strip(),
            'staffId': str(staff_id).strip(),
            'type': str(issue_type).strip(),
            'due': due_str,
            'shelf': str(shelf).strip(),
            'overdue': overdue
        })

    print(f"[+] Loaded {len(books)} books across Leadership, Technology & Quality wings.")

    # Save books_data.json
    with open('books_data.json', 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)

    print("[*] Step 2: Bundling data and offline assets into Standalone HTML...")
    with open(BASE_HTML, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject latest book array
    marker_start = "const defaultBooks = ["
    marker_end = "];"
    idx_s = html.find(marker_start)
    if idx_s != -1:
        idx_e = html.find(marker_end, idx_s)
        if idx_e != -1:
            json_books_js = json.dumps(books, indent=2, ensure_ascii=False)
            html = html[:idx_s] + f"const defaultBooks = {json_books_js};" + html[idx_e + len(marker_end):]

    # Inline FontAwesome CSS
    if os.path.exists(FA_FILE):
        with open(FA_FILE, 'r', encoding='utf-8') as f:
            fa_css = f.read()
        html = html.replace('<link rel="stylesheet" href="all.min.css">', f'<style>\n{fa_css}\n</style>')

    # Inline Chart.js
    if os.path.exists(CHART_FILE):
        with open(CHART_FILE, 'r', encoding='utf-8') as f:
            chart_js = f.read()
        html = html.replace('<script src="chart.min.js"></script>', f'<script>\n{chart_js}\n</script>')

    # Inline BEL Logo
    if os.path.exists(LOGO_FILE):
        with open(LOGO_FILE, 'rb') as f:
            logo_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')
        html = html.replace('src="bel_logo.jpg"', f'src="{logo_b64}"')

    # Save the standalone HTML file
    with open(STANDALONE_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    file_size_kb = round(os.path.getsize(STANDALONE_HTML) / 1024, 1)
    print(f"[+] Created 100% Standalone HTML: '{STANDALONE_HTML}' ({file_size_kb} KB)")
    print("\n[SUCCESS] All-in-One Standalone Dashboard is Ready!")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

if __name__ == '__main__':
    sync_and_bundle()
