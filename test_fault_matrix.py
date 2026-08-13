import unittest

from ivm_runtime import IVMRuntime, Process, Event, Authority, Rule
from ivm_runtime.faults import FaultPoint, CANONICAL_STEPS, run_with_fault


class CanonicalFaultMatrixTests(unittest.TestCase):
    def setUp(self):
        self.runtime = IVMRuntime()
        self.process = Process("business-license", "UG-KLA", "0.1")
        self.event = Event(
            "E-MATRIX-001",
            "LICENSE_APPLICATION",
            "actor-001",
            {"application": {"complete": True}, "fee": 100},
        )
        self.authority = Authority(
            "AUTH-001", "actor-001", "LICENSING_OFFICER", "UG-KLA"
        )
        self.rules = [
            Rule("R-001", "application.complete", "equals", True),
            Rule("R-002", "fee", "gte", 100),
        ]
        self.initial_state = {
            "applications": {"E-MATRIX-001": {"status": "PENDING"}}
        }
        self.transition = [
            {"op": "set", "path": "applications.E-MATRIX-001.status", "value": "ACTIVE"}
        ]

    def run_fault(self, step, timing):
        return run_with_fault(
            runtime=self.runtime,
            process=self.process,
            event=self.event,
            state=self.initial_state,
            authority=self.authority,
            rules=self.rules,
            transition_operations=self.transition,
            fault_point=FaultPoint(step, timing),
        )

    def test_fault_is_observed_at_every_boundary(self):
        for step in CANONICAL_STEPS:
            for timing in ("before", "after"):
                with self.subTest(step=step, timing=timing):
                    outcome = self.run_fault(step, timing)
                    self.assertTrue(outcome.interrupted)
                    self.assertIn(f"INJECTED_FAULT:{timing}:{step}", outcome.error)

    def test_pre_commit_faults_cannot_create_authoritative_state(self):
        pre_commit = {
            "RECEIVE_EVENT", "LOAD_STATE", "VERIFY_AUTHORITY",
            "EVALUATE_RULES", "EXECUTE_TRANSITION"
        }

        for step in pre_commit:
            for timing in ("before", "after"):
                with self.subTest(step=step, timing=timing):
                    outcome = self.run_fault(step, timing)
                    self.assertEqual(outcome.state, self.initial_state)
                    self.assertFalse(outcome.history_exists)
                    self.assertFalse(outcome.moment_exists)

    def test_commit_before_fault_has_a_visible_state_transition(self):
        outcome = self.run_fault("COMMIT_STATE", "after")
        self.assertEqual(
            outcome.state["applications"]["E-MATRIX-001"]["status"], "ACTIVE"
        )
        self.assertFalse(outcome.history_exists)
        self.assertFalse(outcome.moment_exists)

    def test_history_boundary_exposes_current_atomicity_gap(self):
        # This is intentionally a research assertion, not a "success" assertion.
        # A crash after COMMIT_STATE but before RECORD_HISTORY leaves committed
        # state without a history record in this in-memory prototype.
        outcome = self.run_fault("RECORD_HISTORY", "before")
        self.assertEqual(
            outcome.state["applications"]["E-MATRIX-001"]["status"], "ACTIVE"
        )
        self.assertFalse(outcome.history_exists)

    def test_post_history_fault_preserves_history(self):
        outcome = self.run_fault("RECORD_HISTORY", "after")
        self.assertTrue(outcome.history_exists)
        self.assertTrue(outcome.moment_exists)

    def test_completion_fault_preserves_history(self):
        outcome = self.run_fault("COMPLETE_EXECUTION", "after")
        self.assertTrue(outcome.history_exists)
        self.assertTrue(outcome.moment_exists)


if __name__ == "__main__":
    unittest.main()
