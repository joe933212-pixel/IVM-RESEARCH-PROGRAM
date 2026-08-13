from dataclasses import dataclass
from typing import Dict, Any

@dataclass(frozen=True)
class CanonicalTransition:
    event_id: str = "E-001"
    applicant_id: str = "APPLICANT-001"
    licence_id: str = "LICENCE-001"
    authority_id: str = "AUTHORITY-001"
    rule_set: str = "LICENCE-RULES"
    rule_version: str = "1.0"
    pre_state_id: str = "S-001"
    pre_status: str = "PENDING"
    transition_id: str = "T-001"
    post_state_id: str = "S-002"
    post_status: str = "ACTIVE"
    history_id: str = "H-001"

    def as_context(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "applicant_id": self.applicant_id,
            "licence_id": self.licence_id,
            "authority_id": self.authority_id,
            "rule_set": self.rule_set,
            "rule_version": self.rule_version,
            "state": {"id": self.pre_state_id, "status": self.pre_status},
        }

    def expected_result(self) -> Dict[str, Any]:
        return {
            "event_id": self.event_id,
            "transition_id": self.transition_id,
            "pre_state": {"id": self.pre_state_id, "status": self.pre_status},
            "post_state": {"id": self.post_state_id, "status": self.post_status},
            "authority_id": self.authority_id,
            "rule_set": self.rule_set,
            "rule_version": self.rule_version,
            "commitment_status": "FINALIZED",
            "history_id": self.history_id,
            "replay": "EQUIVALENT",
            "recovery": "EQUIVALENT",
            "duplicate_event": "NO_SECOND_TRANSITION",
        }
