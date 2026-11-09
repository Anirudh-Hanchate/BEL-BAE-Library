# BAE – BEL Library Management System & Intranet Dashboard
### Bharat Electronics Limited (BEL) – BAE Academics & Excellence

This repository contains the standalone, production-ready Library Management System and Intranet Web Dashboard designed specifically for the 3 BAE Wings (**Leadership**, **Technology**, **Quality**) with universal serial numbering (**J1 to Jx**) and 100% offline support.

---

## 📦 What's Inside the Deployment Package

| File | Purpose |
| :--- | :--- |
| **`BAE_BEL_Library_HighTech_Dashboard.html`** | Standalone web dashboard with live search, pop-up book lists, wing metrics, and interactive charts. |
| **`BAE_BEL_Library_Management_System_Final.xlsx`** | Master Excel file (Book Register J1..Jx, formulas, auto-filters, transaction logs). |
| **`bel_logo.jpg`** | Official Bharat Electronics Limited corporate logo. |
| **`chart.min.js` & `all.min.css`** | Offline libraries (ensures charts and icons render with **zero internet**). |
| **`sync_library_data.py`** | Automation script that syncs the Master Excel changes directly into the web dashboard. |
| **`SYNC_TO_INTRANET.bat`** | 1-Click desktop sync button for the Library Administrator. |
| **`books_data.json`** | Structured data payload. |

---

## 🚀 How to Deploy on the BEL Server / Intranet

1. **Upload or Copy to the Shared Server Folder**:
   - Extract this folder into the shared departmental folder on your BEL intranet server (e.g., `\\BEL-SERVER\BAE\Library\`).

2. **Configure Access Permissions (One-Time Setup with IT)**:
   - **Library Administrator PC**: Grant **Read & Write (Modify)** permission.
   - **All Other BEL PCs (Viewers)**: Grant **Read-Only** permission.

3. **Daily Workflow**:
   - The Library Administrator edits `BAE_BEL_Library_Management_System_Final.xlsx` to add books or record loans/returns.
   - After saving, double-click `SYNC_TO_INTRANET.bat`.
   - All employees on any intranet computer opening `BAE_BEL_Library_HighTech_Dashboard.html` will immediately see the updated records and charts.

