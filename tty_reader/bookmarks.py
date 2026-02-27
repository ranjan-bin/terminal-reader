"""Save and restore reading positions."""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

BOOKMARK_DIR = Path.home() / ".tty-reader"
BOOKMARK_FILE = BOOKMARK_DIR / "bookmarks.json"


def _load_all() -> dict:
    BOOKMARK_DIR.mkdir(parents=True, exist_ok=True)
    if not BOOKMARK_FILE.exists():
        return {}
    try:
        return json.loads(BOOKMARK_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}


def _save_all(bookmarks: dict) -> None:
    BOOKMARK_DIR.mkdir(parents=True, exist_ok=True)
    BOOKMARK_FILE.write_text(json.dumps(bookmarks, indent=2))


def save_bookmark(file_key: str, position: dict) -> None:
    bookmarks = _load_all()
    bookmarks[file_key] = {
        **position,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    _save_all(bookmarks)


def get_bookmark(file_key: str) -> dict | None:
    return _load_all().get(file_key)


def list_bookmarks() -> list[dict]:
    bookmarks = _load_all()
    return [{"file_key": k, **v} for k, v in bookmarks.items()]
