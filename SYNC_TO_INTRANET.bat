@echo off
title BAE - BEL Library Management Auto-Sync Engine
color 1F
cls
echo ======================================================================
echo    BHARAT ELECTRONICS LIMITED (BEL) - BAE ACADEMICS & EXCELLENCE
echo        CENTRAL LIBRARY INTRANET SYNCHRONIZATION ENGINE
echo ======================================================================
echo.
echo [*] Syncing Master Excel data to Intranet HTML Dashboard...
echo.
python sync_library_data.py
echo.
pause

