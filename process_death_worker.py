
import json
import os
import sys
from pathlib import Path

from ivm_runtime.durable_journal import DurableJournal


def main():
    journal = DurableJournal(sys.argv[1])
    txid = sys.argv[2]
    phase = sys.argv[3]

    record = {
        "transaction_id": txid,
        "event_id": "E-PROCESS-DEATH-001",
        "previous_state": {"licence": {"status": "PENDING"}},
        "candidate_state": {"licence": {"status": "ACTIVE"}},
        "phase": phase,
        "history_id": None,
        "moment_id": None,
    }

    if phase == "STATE_COMMITTED":
        journal.write(record)
        os._exit(42)

    if phase == "HISTORY_ATTACHED":
        record["history_id"] = "H-PD-001"
        record["moment_id"] = "M-PD-001"
        journal.write(record)
        os._exit(43)

    raise ValueError("unknown phase")


if __name__ == "__main__":
    main()
