import json
from pathlib import Path
from .types import JsonDict

def load_personality(path) -> JsonDict:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8"))
