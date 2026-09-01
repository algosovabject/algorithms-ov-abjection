import json
from datetime import datetime

LOG_PATH = "data/epitaphs.jsonl"

def log_query(inputs, start_states, path):

    entry = {
        "timestamp": datetime.now().isoformat(),
        "input": inputs,
        "start_state": start_states,
        "path": path
    }

    with open(LOG_PATH, "a") as f:
        f.write(
            json.dumps(entry) + "\n"
        )