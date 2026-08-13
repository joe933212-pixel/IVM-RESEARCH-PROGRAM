
import json
import subprocess
import sys
import tempfile
import unittest
import os
from pathlib import Path

from ivm_runtime.durable_journal import DurableJournal


class ProcessDeathRecoveryTests(unittest.TestCase):
    def run_worker(self, journal, txid, phase):
        return subprocess.run(
            [
                sys.executable,
                str(Path(__file__).with_name("process_death_worker.py")),
                str(journal),
                txid,
                phase,
            ],
            capture_output=True,
            text=True,
            env={**os.environ, "PYTHONPATH": str(Path(__file__).resolve().parents[1])},
        )

    def test_process_dies_after_state_commit_and_journal_survives(self):
        with tempfile.TemporaryDirectory() as td:
            journal_path = Path(td) / "transaction.json"

            result = self.run_worker(
                journal_path, "TX-PD-001", "STATE_COMMITTED"
            )

            self.assertEqual(result.returncode, 42)
            self.assertTrue(journal_path.exists())

            recovered = DurableJournal(journal_path).read()

            self.assertEqual(recovered["transaction_id"], "TX-PD-001")
            self.assertEqual(recovered["phase"], "STATE_COMMITTED")
            self.assertEqual(
                recovered["candidate_state"]["licence"]["status"],
                "ACTIVE",
            )
            self.assertIsNone(recovered["history_id"])

    def test_new_process_can_recover_exact_candidate_without_reexecution(self):
        with tempfile.TemporaryDirectory() as td:
            journal_path = Path(td) / "transaction.json"

            result = self.run_worker(
                journal_path, "TX-PD-002", "STATE_COMMITTED"
            )
            self.assertEqual(result.returncode, 42)

            # Simulate a fresh runtime by reading the durable journal from this
            # independent test process. No transition is re-executed.
            recovered = DurableJournal(journal_path).read()

            expected = {
                "transaction_id": "TX-PD-002",
                "event_id": "E-PROCESS-DEATH-001",
                "previous_state": {"licence": {"status": "PENDING"}},
                "candidate_state": {"licence": {"status": "ACTIVE"}},
                "phase": "STATE_COMMITTED",
                "history_id": None,
                "moment_id": None,
            }
            self.assertEqual(recovered, expected)

    def test_process_dies_after_history_attachment_and_record_remains_recoverable(self):
        with tempfile.TemporaryDirectory() as td:
            journal_path = Path(td) / "transaction.json"

            result = self.run_worker(
                journal_path, "TX-PD-003", "HISTORY_ATTACHED"
            )

            self.assertEqual(result.returncode, 43)

            recovered = DurableJournal(journal_path).read()

            self.assertEqual(recovered["phase"], "HISTORY_ATTACHED")
            self.assertEqual(recovered["history_id"], "H-PD-001")
            self.assertEqual(recovered["moment_id"], "M-PD-001")


if __name__ == "__main__":
    unittest.main()
