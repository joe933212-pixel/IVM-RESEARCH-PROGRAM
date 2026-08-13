from dataclasses import dataclass, field
from typing import Any, Optional

@dataclass(frozen=True)
class Process:
    process_id: str
    jurisdiction: str
    version: str

@dataclass(frozen=True)
class Event:
    event_id: str
    event_type: str
    actor_id: str
    payload: dict[str, Any]

@dataclass(frozen=True)
class Authority:
    authority_id: str
    actor_id: str
    role: str
    jurisdiction: str
    active: bool = True

@dataclass(frozen=True)
class Rule:
    rule_id: str
    field: str
    operator: str
    value: Any

@dataclass(frozen=True)
class Transition:
    operations: list[dict[str, Any]]

@dataclass(frozen=True)
class HistoryRecord:
    history_id: str
    process_id: str
    event_id: str
    authority_id: str
    rule_ids: list[str]
    transition: dict[str, Any]
    previous_state_digest: str
    resulting_state_digest: str
    moment_id: str

@dataclass(frozen=True)
class InstitutionalMoment:
    moment_id: str
    process_id: str
    event_id: str
    state: dict[str, Any]
    transition: dict[str, Any]
    history_id: str

@dataclass
class ExecutionContext:
    process: Process
    event: Event
    state: dict[str, Any]
    authority: Optional[Authority] = None
    rules: list[Rule] = field(default_factory=list)
    transition: Optional[Transition] = None
    history: Optional[HistoryRecord] = None
    moment: Optional[InstitutionalMoment] = None
    status: str = "CREATED"
    trace: list[str] = field(default_factory=list)
    error: Optional[str] = None

@dataclass(frozen=True)
class ExecutionResult:
    status: str
    state: dict[str, Any]
    history: Optional[HistoryRecord]
    moment: Optional[InstitutionalMoment]
    trace: list[str]
    error: Optional[str]
