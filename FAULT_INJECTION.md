# IVM Reference Runtime v0.2 — Fault Injection Research Plan

v0.2 begins the transition from the happy path to failure analysis. The target is the canonical CISA sequence: RECEIVE_EVENT → LOAD_STATE → VERIFY_AUTHORITY → EVALUATE_RULES → EXECUTE_TRANSITION → COMMIT_STATE → RECORD_HISTORY → COMPLETE_EXECUTION.

The central boundary is COMMIT_STATE. Before commitment, a failed execution must not leave authoritative state changed. Around and after commitment, recovery must not create a second institutional outcome.

Current experiments test clean commitment, pre-commit authority failure, transportable execution material, and independent replay.

Next experiments will inject interruption at every canonical boundary and measure state mutation, history creation, institutional-moment creation, retry safety, duplicate outcomes, and replay determinism. Durable transactional storage and crash recovery are intentionally not claimed as solved by this prototype.
