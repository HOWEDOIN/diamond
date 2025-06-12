import json
from pathlib import Path

DEFAULT_BIBLE_PATH = Path(__file__).with_name('genesis_sample.json')


def load_bible(path: str | None = None) -> dict:
    """Load Bible data from a JSON file."""
    file_path = Path(path) if path else DEFAULT_BIBLE_PATH
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_verse(bible: dict, book: str, chapter: str, verse: int) -> str | None:
    try:
        return bible[book][chapter][verse - 1]
    except (KeyError, IndexError):
        return None
