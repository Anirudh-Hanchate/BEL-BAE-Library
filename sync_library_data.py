# ==============================================================================
# BHARAT ELECTRONICS LIMITED (BEL) - BAE ACADEMICS & EXCELLENCE
# CENTRAL LIBRARY AUTO-SYNC SCRIPT (Run by Library Administrator on Admin PC)
# ==============================================================================
# This script reads the Master Excel file edited by the Library Manager
# and instantly generates/updates the web dashboard (HTML) and JSON data.
# When saved in the shared network folder, ALL computers across the BEL intranet
# see the updated dashboard immediately upon opening or refreshing!
# ==============================================================================

import openpyxl
import json
import os
import sys
from datetime import datetime

EXCEL_FILE = 'BAE_BEL_Library_Management_System_Final.xlsx'
JSON_FILE = 'books_data.json'
HTML_TEMPLATE = 'BAE_BEL_Library_HighTech_Dashboard.html'

def sync_library():
    print("=" * 70)
    print(" BAE - BEL LIBRARY MANAGEMENT INTRANET SYNC ENGINE")
    print("=" * 70)
    
    if not os.path.exists(EXCEL_FILE):
        print(f"[ERROR] Excel file '{EXCEL_FILE}' not found in current folder!")
        return

    print(f"[*] Reading master catalog from: {EXCEL_FILE}...")
    try:
        wb = openpyxl.load_workbook(EXCEL_FILE, data_only=True)
    except PermissionError:
        print(f"[WARNING] '{EXCEL_FILE}' is currently open in Excel. Please save and close it, or try again.")
        return

    ws = wb['Book Register']
    books = []

    for r in range(5, 2000):
        serial = ws.cell(row=r, column=1).value
        title = ws.cell(row=r, column=2).value
        
        # Stop when rows are empty
        if not serial or not title:
            # Check if there are more rows or if this is the end
            next_serial = ws.cell(row=r+1, column=1).value
            if not next_serial:
                break
            continue

        wing = ws.cell(row=r, column=3).value or 'General'
        status = ws.cell(row=r, column=4).value or 'Available'
        borrower = ws.cell(row=r, column=5).value or '-'
        staff_id = ws.cell(row=r, column=6).value or '-'
        issue_type = ws.cell(row=r, column=7).value or '-'
        due_date = ws.cell(row=r, column=10).value or '-'
        shelf = ws.cell(row=r, column=13).value or 'Shelf Location'

        # Format date cleanly if datetime object
        if isinstance(due_date, datetime):
            due_str = due_date.strftime('%Y-%m-%d')
        else:
            due_str = str(due_date).strip()

        # Check overdue
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

    # 1. Save books_data.json
    with open(JSON_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"[+] Data exported to '{JSON_FILE}'.")

    # 2. Embed directly into the standalone HTML file so it works 100% offline without local server
    if os.path.exists(HTML_TEMPLATE):
        with open(HTML_TEMPLATE, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # Find defaultBooks array in JS and update it
        marker_start = "const defaultBooks = ["
        marker_end = "];"
        idx_start = html_content.find(marker_start)
        if idx_start != -1:
            idx_end = html_content.find(marker_end, idx_start)
            if idx_end != -1:
                json_books_js = json.dumps(books, indent=2, ensure_ascii=False)
                new_js_block = f"const defaultBooks = {json_books_js};"
                updated_html = html_content[:idx_start] + new_js_block + html_content[idx_end + len(marker_end):]
                with open(HTML_TEMPLATE, 'w', encoding='utf-8') as f:
                    f.write(updated_html)
                print(f"[+] Embedded latest data into '{HTML_TEMPLATE}'.")

    print("\n[SUCCESS] SYNC COMPLETE!")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("All intranet computers opening the HTML file will now see the latest updated data!")
    print("=" * 70)

if __name__ == '__main__':
    sync_library()

