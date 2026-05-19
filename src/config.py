import os

# ============================================================
# IMPORTANT: Variable names defined here are reserved.
# Do not redefine these names in notebooks or other modules.
# ============================================================

# ============================================================
# ROOT DIRECTORY — change this one line when moving machines
# ============================================================
PROJECT_ROOT = r"C:\Users\mjbou\governance-framework"

# ============================================================
# Derived paths — do not edit these
# ============================================================
RAW_DIR        = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR  = os.path.join(PROJECT_ROOT, "data", "processed")
OUTPUTS_DIR    = os.path.join(PROJECT_ROOT, "data", "outputs")
NOTEBOOKS_DIR  = os.path.join(PROJECT_ROOT, "notebooks")
REPORTS_DIR    = os.path.join(PROJECT_ROOT, "reports")
DOCS_DIR       = os.path.join(PROJECT_ROOT, "docs")
SRC_DIR        = os.path.join(PROJECT_ROOT, "src")

# ============================================================
# Downloads folder — change if browser saves elsewhere
# ============================================================
DOWNLOADS_DIR  = r"C:\Users\mjbou\Downloads"

# ============================================================
# Framework parameters — edit these as needed
# ============================================================
FRAMEWORK_START_YEAR = 1990