# IVM Reference Runtime Changelog

## Purpose

This changelog records the research-driven evolution of the reference runtime from v0.1 through v0.4.

The sequence is organised around the research problem each version was intended to investigate and the failure or observation that motivated the next version.

---

## v0.1 — Executable Baseline

### Research purpose

Establish a minimal executable IVM/CISA pipeline before introducing networking, databases, external identity providers or distributed deployment.

### Canonical pipeline

`RECEIVE_EVENT → LOAD_STATE → VERIFY_AUTHORITY → EVALUATE_RULES → EXECUTE_TRANSITION → COMMIT_STATE → RECORD_HISTORY → COMPLETE_EXECUTION`

### Core capabilities

The baseline runtime represents processes, events, authorities, rules and transitions and supports successful execution, authority/rule rejection, duplicate handling and replay.

### Evidence

Five runtime tests pass when executed from the correct package root.

### Research boundary

The runtime is deliberately in-memory and does not claim durable crash recovery or distributed execution.

---

## v0.2 — Fault Injection

### Motivation

The research moved beyond successful execution toward controlled failure analysis.

### Change

Fault-injection tests were added around the canonical execution sequence, with particular attention to the `COMMIT_STATE` boundary.

### Research question

What institutional state remains authoritative when execution fails before or around commitment, and can the same execution material be replayed independently?

### Evidence

Nine tests pass in the v0.2 test record.

### Research boundary

The v0.2 research plan explicitly leaves durable transactional storage and crash recovery unresolved.

---

## v0.3 — Canonical Fault Matrix

### Motivation

v0.2 established basic failure behaviour but did not systematically test every canonical instruction boundary.

### Change

A fault-injection matrix and dedicated fault model were introduced. Deliberate interruption was tested immediately before and after each canonical instruction boundary.

### Key finding

The experiment exposed an atomicity gap between `COMMIT_STATE` and `RECORD_HISTORY`.

A failure after State commitment but before History recording could leave authoritative State changed without corresponding History.

### Research significance

This was treated as a concrete architectural failure boundary.

The next question became whether State commitment and History creation could be represented as one recoverable institutional commitment rather than unrelated operations.

### Evidence

Fifteen tests pass in the v0.3 record, including explicit tests for the discovered History boundary.

---

## v0.4 — Transactional Commitment

### Motivation

Resolve the specific semantic gap exposed by v0.3 at the prototype level.

### Change

v0.4 introduces a durable JSON-backed transaction journal and a transactional execution path.

### Transaction model

`PREPARED → STATE_COMMITTED → HISTORY_ATTACHED → FINALIZED`

The journal stores the previous State, candidate State, Transition and Event identifier before commitment.

### Research proposition

An institutional transition should not be considered fully finalized until authoritative State and corresponding institutional History can be recovered as one deterministic transaction record.

### Evidence

Twenty runtime tests pass in the v0.4 suite.

The tests demonstrate recovery from the tested transaction boundaries without recalculating a different candidate State.

### Research boundary

The journal is a narrow local research mechanism. It does not establish distributed consensus, database-grade concurrency control, cryptographic notarization or general production durability.

---

## v0.4A — Actual Process-Death Validation

### Motivation

A simulated crash boundary is weaker evidence than actual termination of the process executing the transition.

### Change

A dedicated worker process was introduced. The worker persists the transaction journal and deliberately terminates with a non-zero exit code at defined transaction phases.

A fresh process then attempts recovery from the durable journal.

### Research question

Can recovery survive actual process death?

### Evidence

23 process-death tests pass.

The fresh process recovers the exact candidate State and transaction phase and does not re-execute the transition.

### Research boundary

The experiment does not establish filesystem power-loss durability, distributed atomicity, concurrent recovery, replication, Byzantine tolerance or corruption recovery.

### Next question

Can the same recovery semantics remain correct under concurrent recovery attempts, duplicate recovery, persistence faults and increasingly realistic storage conditions?

---

## Versioning Principle

A runtime version is a research instrument, not merely a software release.

Each version should therefore retain the question it was built to answer, the failure or observation that motivated the change and the evidence produced by the resulting implementation.

A later version does not erase the limitations or failures discovered by an earlier version.
