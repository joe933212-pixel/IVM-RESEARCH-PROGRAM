from copy import deepcopy
from typing import Dict, Any
from conformance.protocol import Comparator

class ConventionalStateMachine(Comparator):
    """Ordinary deterministic state-machine baseline for Experiment 005."""

    def __init__(self):
        self.state = {"id": "S-001", "status": "PENDING"}
        self.transitions = {}
        self.history = {}
        self.events = set()
        self.authority_revoked = set()
        self.rule_versions = {"LICENCE-RULES": {"1.0": {"eligible": True}}}

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        event_id = context["event_id"]

        if event_id in self.events:
            for tid, t in self.transitions.items():
                if t["event_id"] == event_id:
                    result = self._result_for_transition(tid)
                    result["duplicate_event"] = "NO_SECOND_TRANSITION"
                    return result

        authority = context["authority_id"]
        rules = context["rule_set"]
        version = context["rule_version"]

        if authority in self.authority_revoked:
            raise ValueError("authority revoked")
        if version not in self.rule_versions.get(rules, {}):
            raise ValueError("unknown rule version")
        if self.state["status"] != "PENDING":
            raise ValueError("invalid pre-state")

        tid = "T-001"
        post_state = {"id": "S-002", "status": "ACTIVE"}
        hid = "H-001"

        self.transitions[tid] = {
            "event_id": event_id,
            "authority_id": authority,
            "rule_set": rules,
            "rule_version": version,
            "pre_state": deepcopy(self.state),
            "post_state": deepcopy(post_state),
            "history_id": hid,
            "committed": True,
        }
        self.state = post_state
        self.history[hid] = deepcopy(self.transitions[tid])
        self.events.add(event_id)

        return self._result_for_transition(tid)

    def _result_for_transition(self, tid: str) -> Dict[str, Any]:
        t = self.transitions[tid]
        return {
            "event_id": t["event_id"],
            "transition_id": tid,
            "pre_state": t["pre_state"],
            "post_state": t["post_state"],
            "authority_id": t["authority_id"],
            "rule_set": t["rule_set"],
            "rule_version": t["rule_version"],
            "commitment_status": "FINALIZED" if t["committed"] else "INCOMPLETE",
            "history_id": t["history_id"] if t["committed"] else None,
            "replay": self.replay(tid),
            "recovery": self.recover(tid),
            "duplicate_event": self.duplicate_event(t["event_id"]),
        }

    def replay(self, tid: str) -> str:
        t = self.transitions[tid]
        if t["rule_version"] not in self.rule_versions.get(t["rule_set"], {}):
            return "NOT_REPLAYABLE"
        expected = {"id": "S-002", "status": "ACTIVE"}
        return "EQUIVALENT" if t["post_state"] == expected else "DIVERGENT"

    def duplicate_event(self, event_id: str) -> str:
        count = sum(t["event_id"] == event_id for t in self.transitions.values())
        return "NO_SECOND_TRANSITION" if count == 1 else "DUPLICATE_TRANSITION"

    def recover(self, tid: str) -> str:
        t = self.transitions[tid]
        return "EQUIVALENT" if t["committed"] and t["post_state"] == self.state else "DIVERGENT"

    def revoke_authority(self, authority_id: str):
        self.authority_revoked.add(authority_id)

    def add_rule_version(self, rule_set: str, version: str, eligible: bool = True):
        self.rule_versions.setdefault(rule_set, {})[version] = {"eligible": eligible}
