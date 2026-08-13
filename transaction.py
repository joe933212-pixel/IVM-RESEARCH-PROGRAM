"""Recoverable transactional commitment for IVM v0.4.

This module deliberately keeps persistence simple: a JSON journal is used as
an experimental durable store. The purpose is to test semantics, not provide
production storage or distributed consensus.
"""
from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any, Dict, Optional

from .canonical import deep_copy, digest
from .transition import apply_transition


@dataclass
class PendingCommit:
    transaction_id: str
    event_id: str
    previous_state: Dict[str, Any]
    candidate_state: Dict[str, Any]
    transition: Dict[str, Any]
    phase: str = "PREPARED"
    history_id: Optional[str] = None
    moment_id: Optional[str] = None

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data):
        return cls(**data)


class DurableCommitJournal:
    """Small JSON-backed journal used for crash/recovery experiments."""

    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.records = {}
        self._load()

    def _load(self):
        if self.path.exists():
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.records = {
                k: PendingCommit.from_dict(v) for k, v in data.items()
            }

    def _persist(self):
        payload = {k: v.to_dict() for k, v in self.records.items()}
        tmp = self.path.with_suffix(self.path.suffix + ".tmp")
        tmp.write_text(json.dumps(payload, sort_keys=True, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    def create(self, record):
        if record.transaction_id in self.records:
            raise ValueError("TRANSACTION_ALREADY_EXISTS")
        self.records[record.transaction_id] = record
        self._persist()
        return record

    def update(self, record):
        if record.transaction_id not in self.records:
            raise KeyError("TRANSACTION_NOT_FOUND")
        self.records[record.transaction_id] = record
        self._persist()
        return record

    def get(self, transaction_id):
        return self.records.get(transaction_id)

    def all(self):
        return list(self.records.values())


class TransactionalCommitStore:
    """Research implementation of recoverable institutional commitment."""

    def __init__(self, journal_path=None):
        self.journal = DurableCommitJournal(journal_path) if journal_path else None
        self.pending = {}
        self.committed = {}
        if self.journal:
            for record in self.journal.all():
                if record.phase == "FINALIZED":
                    self.committed[record.transaction_id] = record
                else:
                    self.pending[record.transaction_id] = record

    def _save(self, record):
        if self.journal:
            self.journal.update(record) if self.journal.get(record.transaction_id) else self.journal.create(record)

    def prepare(self, transaction_id, event_id, previous_state, transition):
        if transaction_id in self.pending or transaction_id in self.committed:
            raise ValueError("TRANSACTION_ALREADY_EXISTS")
        candidate = apply_transition(deep_copy(previous_state), transition)
        record = PendingCommit(
            transaction_id=transaction_id,
            event_id=event_id,
            previous_state=deep_copy(previous_state),
            candidate_state=deep_copy(candidate),
            transition=deep_copy(transition),
        )
        self.pending[transaction_id] = record
        self._save(record)
        return record

    def mark_state_committed(self, transaction_id):
        record = self.pending[transaction_id]
        record.phase = "STATE_COMMITTED"
        self._save(record)
        return record

    def attach_history(self, transaction_id, history_id, moment_id):
        record = self.pending[transaction_id]
        if record.phase != "STATE_COMMITTED":
            raise ValueError("HISTORY_REQUIRES_STATE_COMMIT")
        record.history_id = history_id
        record.moment_id = moment_id
        record.phase = "HISTORY_ATTACHED"
        self._save(record)
        return record

    def finalize(self, transaction_id):
        record = self.pending[transaction_id]
        if record.phase != "HISTORY_ATTACHED":
            raise ValueError("CANNOT_FINALIZE_WITHOUT_HISTORY")
        record.phase = "FINALIZED"
        self._save(record)
        self.pending.pop(transaction_id, None)
        self.committed[transaction_id] = record
        return record

    def recover(self, transaction_id):
        if transaction_id in self.committed:
            return self.committed[transaction_id]
        record = self.pending.get(transaction_id)
        if record is None:
            raise KeyError("TRANSACTION_NOT_FOUND")
        # Recovery never recalculates the candidate state. It resumes from the
        # durable transaction record and therefore cannot invent a new outcome.
        if record.phase == "PREPARED":
            return record
        if record.phase == "STATE_COMMITTED":
            return record
        if record.phase == "HISTORY_ATTACHED":
            return self.finalize(transaction_id)
        raise ValueError(f"UNKNOWN_TRANSACTION_PHASE:{record.phase}")

    @staticmethod
    def transaction_id(process_id, event_id, previous_state, transition):
        material = {
            "process_id": process_id,
            "event_id": event_id,
            "previous_state": previous_state,
            "transition": transition,
        }
        return "TX-" + digest(material)[:24]
