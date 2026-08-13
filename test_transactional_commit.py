import tempfile
import unittest
from pathlib import Path

from ivm_runtime import Process, Event, TransactionalIVMRuntime


class TransactionalCommitTests(unittest.TestCase):
    def setUp(self):
        self.process = Process("business-license", "UG-KLA", "0.1")
        self.event = Event(
            "E-TX-001", "LICENSE_APPLICATION", "actor-001",
            {"application": {"complete": True}, "fee": 100},
        )
        self.initial = {"applications": {"E-TX-001": {"status": "PENDING"}}}
        self.transition = [
            {"op": "set", "path": "applications.E-TX-001.status", "value": "ACTIVE"}
        ]
        self.tmp = tempfile.TemporaryDirectory()
        self.journal = Path(self.tmp.name) / "commit-journal.json"

    def tearDown(self):
        self.tmp.cleanup()

    def test_prepare_persists_candidate_without_authoritative_commit(self):
        rt = TransactionalIVMRuntime(self.journal)
        tx = rt.prepare_commit(
            process=self.process, event=self.event,
            state=self.initial, transition=self.transition
        )
        self.assertEqual(tx.phase, "PREPARED")
        self.assertEqual(tx.previous_state, self.initial)
        self.assertEqual(tx.candidate_state["applications"]["E-TX-001"]["status"], "ACTIVE")
        self.assertTrue(self.journal.exists())

    def test_state_commit_without_history_cannot_finalize(self):
        rt = TransactionalIVMRuntime(self.journal)
        tx = rt.prepare_commit(process=self.process, event=self.event, state=self.initial, transition=self.transition)
        rt.store.mark_state_committed(tx.transaction_id)
        with self.assertRaises(ValueError):
            rt.store.finalize(tx.transaction_id)

    def test_crash_after_state_commit_is_recoverable_by_new_runtime(self):
        first = TransactionalIVMRuntime(self.journal)
        tx = first.prepare_commit(process=self.process, event=self.event, state=self.initial, transition=self.transition)
        first.store.mark_state_committed(tx.transaction_id)

        # Simulate process death: construct a new runtime against the same journal.
        recovered = TransactionalIVMRuntime(self.journal)
        record = recovered.recover_transaction(tx.transaction_id)

        self.assertEqual(record.phase, "STATE_COMMITTED")
        self.assertEqual(record.previous_state, self.initial)
        self.assertEqual(record.candidate_state["applications"]["E-TX-001"]["status"], "ACTIVE")
        self.assertIsNone(record.history_id)
        self.assertIsNone(record.moment_id)

    def test_recovery_after_history_attachment_finalizes(self):
        first = TransactionalIVMRuntime(self.journal)
        tx = first.prepare_commit(process=self.process, event=self.event, state=self.initial, transition=self.transition)
        first.store.mark_state_committed(tx.transaction_id)
        first.store.attach_history(tx.transaction_id, "H-1", "M-1")

        recovered = TransactionalIVMRuntime(self.journal)
        record = recovered.recover_transaction(tx.transaction_id)

        self.assertEqual(record.phase, "FINALIZED")
        self.assertEqual(record.history_id, "H-1")
        self.assertEqual(record.moment_id, "M-1")

    def test_recovery_does_not_recompute_a_different_candidate(self):
        first = TransactionalIVMRuntime(self.journal)
        tx = first.prepare_commit(process=self.process, event=self.event, state=self.initial, transition=self.transition)
        expected = tx.candidate_state
        first.store.mark_state_committed(tx.transaction_id)

        second = TransactionalIVMRuntime(self.journal)
        recovered = second.recover_transaction(tx.transaction_id)
        self.assertEqual(recovered.candidate_state, expected)


if __name__ == "__main__":
    unittest.main()
