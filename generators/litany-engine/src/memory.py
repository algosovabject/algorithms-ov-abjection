# src/memory.py

import json
from datetime import datetime

LOG_PATH = "data/oracle_log.jsonl"

def log_query(question, path, matched_tags):
    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": "I wanted forgiveness but fed the machine instead.",
        "start_state": "forgiveness",
        "path": [
            "forgiveness",
            "hunger",
            "machine",
            "blood"
        ]
    }

    with open(LOG_PATH, 'a') as f:
        f.write(json.dumps(entry) + "\n")
