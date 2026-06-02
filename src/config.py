import os
from datetime import datetime
from dotenv import load_dotenv

# Load machine-specific .env file — not tracked by git
# Each machine has its own .env with local paths
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ============================================================
# IMPORTANT: Variable names defined here are reserved.
# Do not redefine these names in notebooks or other modules.
# Reserved names: 
# PROJECT_ROOT, RAW_DIR, PROCESSED_DIR,
# OUTPUTS_DIR, NOTEBOOKS_DIR, REPORTS_DIR, DOCS_DIR, SRC_DIR,
# DOWNLOADS_DIR, FRAMEWORK_START_YEAR, CURRENT_YEAR, SSL_VERIFY
# ACLED_EMAIL, ACLED_PASSWORD
# ============================================================

# ============================================================
# ROOT DIRECTORY — set in .env file, not here
# .env file is machine-specific and not tracked by git
# ============================================================
PROJECT_ROOT = os.environ.get('PROJECT_ROOT', os.path.expanduser('~/Documents/governance-framework'))
DOWNLOADS_DIR = os.environ.get('DOWNLOADS_DIR', os.path.expanduser('~/Downloads'))

# ============================================================
# Derived paths — do not edit these
# ============================================================
RAW_DIR       = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUTS_DIR   = os.path.join(PROJECT_ROOT, "data", "outputs")
NOTEBOOKS_DIR = os.path.join(PROJECT_ROOT, "notebooks")
REPORTS_DIR   = os.path.join(PROJECT_ROOT, "reports")
DOCS_DIR      = os.path.join(PROJECT_ROOT, "docs")
SRC_DIR       = os.path.join(PROJECT_ROOT, "src")

# ============================================================
# Framework parameters — edit these as needed
# ============================================================
FRAMEWORK_START_YEAR = 1990
CURRENT_YEAR = datetime.today().year

# ============================================================
# Network settings — auto-detected, no manual configuration needed
# ============================================================
try:
    import requests as _req
    _req.get("https://api.worldbank.org/v2/country?format=json", timeout=5, verify=True)
    SSL_VERIFY = True
except Exception:
    SSL_VERIFY = False

# Standard browser User-Agent header — used for sources that block automated requests
BROWSER_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ============================================================
# API credentials — set in .env file, never hardcode
# ============================================================
ACLED_EMAIL = os.environ.get('ACLED_EMAIL', '')
ACLED_PASSWORD = os.environ.get('ACLED_PASSWORD', '')