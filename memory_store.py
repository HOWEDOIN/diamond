import json
from pathlib import Path
from datetime import datetime

MEMORY_FILE = Path(__file__).with_name('hypotheses.json')


def load_memory() -> list:
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []


def save_hypothesis(entry: dict) -> None:
    data = load_memory()
    entry.setdefault('timestamp', datetime.utcnow().isoformat())
    data.append(entry)
    with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
