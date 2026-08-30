# src/memory.py

import json
from datetime import datetime

LOG_PATH = "data/oracle_log.jsonl"

def log_query(question, path, matched_tags):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "question": question,
        "path": path,
        "tags": list(matched_tags)
    }

    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")
