import pandas as pd
import os
from datetime import datetime

LOG_PATH = r"C:\Users\mjbou\governance-framework\data\raw\download_log.csv"

COLUMNS = [
    "source_id",
    "last_attempted_date",
    "last_successful_download_date",
    "data_as_of_date",
    "local_filename",
    "latest_available_version",
    "no_update_reason",
    "notes"
]


def load_log():
    """Load the download log, creating it if it doesn't exist."""
    if os.path.exists(LOG_PATH):
        return pd.read_csv(LOG_PATH, dtype=str)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(LOG_PATH, index=False)
        return df


def get_entry(source_id):
    """Return the log entry for a source, or None if not present."""
    log = load_log()
    matches = log[log["source_id"] == source_id]
    if len(matches) == 0:
        return None
    return matches.iloc[0].to_dict()


def update_entry(source_id, **kwargs):
    """
    Create or update a log entry for a source.
    Pass any COLUMNS fields as keyword arguments.
    Always sets last_attempted_date to today.
    """
    log = load_log()
    today = datetime.today().strftime("%Y-%m-%d")

    # Build the updated row
    entry = {col: "" for col in COLUMNS}
    entry["source_id"] = source_id
    entry["last_attempted_date"] = today

    # If entry already exists, start from existing values
    existing = log[log["source_id"] == source_id]
    if len(existing) > 0:
        for col in COLUMNS:
            entry[col] = str(existing.iloc[0][col]) if pd.notna(existing.iloc[0][col]) else ""

    # Apply updates
    for key, value in kwargs.items():
        if key in COLUMNS:
            entry[key] = str(value) if value is not None else ""

    # Remove old entry and append updated one
    log = log[log["source_id"] != source_id]
    new_row = pd.DataFrame([entry])
    log = pd.concat([log, new_row], ignore_index=True)
    log.to_csv(LOG_PATH, index=False)
    print(f"[download_log] Updated entry for {source_id}")


def print_entry(source_id):
    """Print the log entry for a source in readable format."""
    entry = get_entry(source_id)
    if entry is None:
        print(f"No entry found for {source_id}")
        return
    for key, value in entry.items():
        print(f"  {key}: {value}")


def print_stale_sources(max_days=90):
    """Print sources not successfully downloaded within max_days."""
    log = load_log()
    if log.empty:
        print("Log is empty.")
        return
    today = datetime.today()
    stale = []
    for _, row in log.iterrows():
        if pd.isna(row["last_successful_download_date"]) or row["last_successful_download_date"] == "":
            stale.append((row["source_id"], "never downloaded"))
            continue
        try:
            last = datetime.strptime(row["last_successful_download_date"], "%Y-%m-%d")
            days = (today - last).days
            if days > max_days:
                stale.append((row["source_id"], f"{days} days ago"))
        except ValueError:
            stale.append((row["source_id"], "invalid date"))
    if not stale:
        print(f"All sources downloaded within {max_days} days.")
    else:
        print(f"Stale sources (>{max_days} days):")
        for source_id, reason in stale:
            print(f"  {source_id}: {reason}")