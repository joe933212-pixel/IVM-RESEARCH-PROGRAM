# IVM Reference Runtime v0.1

A minimal executable research prototype for the Institutional Virtual Machine (IVM) and Coordination Instruction Set Architecture (CISA).

Canonical execution sequence:

RECEIVE_EVENT -> LOAD_STATE -> VERIFY_AUTHORITY -> EVALUATE_RULES -> EXECUTE_TRANSITION -> COMMIT_STATE -> RECORD_HISTORY -> COMPLETE_EXECUTION

This prototype deliberately excludes networking, databases, external identity providers and distributed deployment. It exists to test the core execution semantics before those concerns are added.

## Run

Python 3.10+

```bash
python -m unittest discover -s tests -v
python examples/run_license_demo.py
```

## Research target

The central hypothesis being tested is that identical explicit institutional execution material can produce identical authoritative state and independently replayable history.
