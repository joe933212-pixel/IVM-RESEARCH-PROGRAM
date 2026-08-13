# IVM Reference Runtime v0.4 — Transactional Commitment

## Purpose

Version 0.3 exposed a specific execution-boundary problem: `COMMIT_STATE` could complete before `RECORD_HISTORY` completed. The resulting condition was potentially **authoritative State without corresponding History**.

Version 0.4 tests a recovery-oriented commitment model for that boundary.

## Research proposition

An institutional transition should not be considered fully finalized until its authoritative State and corresponding institutional History can be recovered as one deterministic transaction record.

The prototype therefore introduces a durable JSON-backed commit journal with four phases:

`PREPARED → STATE_COMMITTED → HISTORY_ATTACHED → FINALIZED`

The journal stores the previous State, candidate State, Transition and Event identifier before commitment. Recovery resumes from this durable record rather than recalculating the transition.

## What v0.4 demonstrates

The tests demonstrate that a process can be restarted after the `STATE_COMMITTED` boundary and recover the exact candidate State and transaction phase without inventing a new transition.

They also demonstrate that a transaction cannot be finalized while History is absent.

## What v0.4 does not demonstrate

This is not a production transaction manager. It does not provide distributed consensus, multi-node durability, database-grade concurrency control, cryptographic notarization, or crash-consistency guarantees beyond the small JSON journal used by the experiment.

The implementation is deliberately narrow: it tests the **semantic recovery model** before introducing distributed infrastructure.

## Research finding

The v0.4 model closes the specific semantic gap observed in v0.3 at the prototype level: an interrupted transaction can be represented as a recoverable institutional commitment record rather than as an ambiguous pair of independent State and History operations.

The next validation question is whether this model remains correct under real process termination, concurrent recovery, duplicate recovery attempts and durable-storage faults.
