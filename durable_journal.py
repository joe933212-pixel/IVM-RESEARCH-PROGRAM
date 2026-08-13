
import json
from pathlib import Path


class DurableJournal:
    """Small append/replace JSON journal used for process-death experiments."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, record):
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(record, sort_keys=True, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def read(self):
        if not self.path.exists():
            return None
        return json.loads(self.path.read_text(encoding="utf-8"))
