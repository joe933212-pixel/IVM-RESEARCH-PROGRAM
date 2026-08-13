# IVM Reference Runtime v0.1 — Architecture Note

This is a research instrument translating the current CISA execution semantics into an executable machine.

The prototype preserves the canonical observable order: RECEIVE_EVENT, LOAD_STATE, VERIFY_AUTHORITY, EVALUATE_RULES, EXECUTE_TRANSITION, COMMIT_STATE, RECORD_HISTORY, COMPLETE_EXECUTION.

Before COMMIT_STATE, the transition is provisional. After COMMIT_STATE, the resulting state becomes authoritative for the execution result. History is recorded only after successful commitment.

Deterministic JSON serialization and SHA-256 are implementation choices for stable identifiers in this prototype, not claims that the specification mandates SHA-256.

Replay reconstructs execution from explicit process, event, initial state, authority, rules and transition material.

Known limitation: duplicate-event protection is local in-memory state. A production runtime needs durable uniqueness, crash recovery and concurrency semantics. This is intentionally left as a research problem rather than hidden behind infrastructure.
