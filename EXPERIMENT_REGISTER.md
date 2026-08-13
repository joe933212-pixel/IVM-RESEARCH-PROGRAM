# IVM Experiment Register

## Purpose

This register provides a single index of the executable research experiments represented in the current archive.

The register distinguishes verified experiment evidence from historical sequence labels that still require reconciliation against the original research notes.

The project does not infer an experiment number merely because a runtime version exists.

---

## Experiment 001 — Initial Reference Runtime Behaviour

**Status:** Historical experiment grouping; original standalone protocol not yet located.

**Implementation basis:** Reference Runtime v0.1.

**Research target:** Test the core execution semantics of the IVM prototype before networking, databases, external identity providers or distributed deployment are introduced.

**Canonical execution sequence:**

`RECEIVE_EVENT → LOAD_STATE → VERIFY_AUTHORITY → EVALUATE_RULES → EXECUTE_TRANSITION → COMMIT_STATE → RECORD_HISTORY → COMPLETE_EXECUTION`

**Verified test evidence:** The v0.1 test suite contains five tests covering successful execution, authority failure, rule failure, duplicate handling and replay. The packaged historical result file records an import-path failure when executed from the archive without the package path configured. The same source suite was subsequently rerun from the correct package root and all five tests passed.

**Interpretation:** The runtime provided an executable baseline for state transition, authority/rule rejection, duplicate handling and replay.

**Evidence:** `runtime/reference/versions/v0.1/`

---

## Experiment 002 — Failure-Oriented Execution

**Status:** Verified through the v0.2 fault-injection research record.

**Implementation basis:** Reference Runtime v0.2.

**Research target:** Move from the happy path toward controlled failure analysis and examine the semantic boundary around `COMMIT_STATE`.

**Verified result:** Nine tests passed. The tests cover clean commitment, transportable execution material, pre-commit authority failure, independent replay, authority failure, duplicate handling, replay, rule failure and success.

**Important limitation:** The v0.2 research plan explicitly states that durable transactional storage and crash recovery were not yet claimed as solved.

**Evidence:** `runtime/reference/versions/v0.2/FAULT_INJECTION.md` and `TEST_RESULTS_v0.2.txt`.

---

## Experiment 003 — Canonical Fault Matrix

**Status:** Verified through the v0.3 fault-matrix record.

**Implementation basis:** Reference Runtime v0.3.

**Research target:** Inject deliberate interruption immediately before and after every canonical instruction boundary.

**Verified result:** Fifteen tests passed. The matrix exposed a specific failure boundary: after `COMMIT_STATE` but before `RECORD_HISTORY`, the prototype could expose changed authoritative State without corresponding History.

**Research finding:** State commitment and History recording were separate operations in the prototype. The resulting gap was treated as a failure requiring architectural resolution, not as a successful property.

**Evidence:** `runtime/reference/versions/v0.3/FAULT_MATRIX_FINDINGS.md`, `fault_matrix.json` and `TEST_RESULTS_v0.3.txt`.

---

## Experiment 004 — Transactional Commitment

**Status:** Verified through Reference Runtime v0.4.

**Implementation basis:** Reference Runtime v0.4.

**Research question:** Can the State/History boundary exposed by v0.3 be represented as one recoverable institutional transaction?

**Transaction phases:**

`PREPARED → STATE_COMMITTED → HISTORY_ATTACHED → FINALIZED`

**Verified result:** Twenty tests passed in the v0.4 runtime suite. The tests establish that a transaction can persist its candidate State and phase, recover after a simulated crash boundary and avoid recomputing a different candidate. A transaction cannot be finalized while History is absent.

**Research limitation:** The v0.4 transactional journal is a small local JSON research mechanism. It does not establish distributed consensus, database-grade concurrency control, cryptographic notarization or general crash-consistency guarantees.

**Evidence:** `runtime/reference/versions/v0.4/TRANSACTIONAL_COMMIT_v0.4.md` and `TEST_RESULTS_v0.4.txt`.

---

## Experiment 004A — Actual Process Death and Recovery

**Status:** Verified.

**Implementation basis:** Reference Runtime v0.4 process-death validation package.

**Question:** Can the v0.4 commitment model survive actual process termination and allow a fresh runtime to recover the prepared institutional transaction without re-executing the transition?

**Method:** A separate operating-system process executes the worker. The worker persists the transaction journal, terminates with a non-zero exit code at defined transaction phases, and a fresh process subsequently reads and recovers the durable record.

**Verified result:** 23 tests passed. The fresh process recovered the exact candidate State and transaction phase and did not re-execute the transition.

**What this establishes:** At the tested boundaries, the local durable transaction record survives actual process termination and can be consumed by a fresh process without inventing a second institutional transition.

**What this does not establish:** Filesystem power-loss durability, distributed atomicity, concurrent recovery, replication, Byzantine fault tolerance, corruption recovery or failure during the physical persistence operation remain untested.

**Evidence:** `runtime/reference/versions/v0.4/PROCESS_DEATH_EXPERIMENT.md` and `TEST_RESULTS_PROCESS_DEATH.txt`.

---

## Experiment 005 — Comparative Institutional Execution

**Status:** Active research programme.

**Implementation basis:** Conventional deterministic state-machine comparator and conformance harness.

**Canonical transition:**

`PENDING → ACTIVE`

**Research question:** Can a conventional execution model satisfy the same institutional semantic contract represented by the IVM test vector?

**Current semantic vector:** Event identity, authority, rule-set identity and version, pre-state, post-state, transition identity, commitment, history, replay and duplicate-event behaviour.

**Current comparator:** Conventional deterministic state machine.

**Verified result:** Five conformance tests passed in the available v0.2 harness.

**Interpretation:** The current result demonstrates that the comparator can satisfy the tested semantic contract. It does not establish equivalence or non-equivalence with IVM, nor does it establish architectural novelty.

**Next boundary:** Process-death testing and additional comparative execution models.

**Evidence:** `experiments/005/` and `comparators/conventional-state-machine/`.

---

## Register Status

The historical sequence represented by Experiments 001–004 should be reconciled against the original laboratory notes before the repository is presented as a complete archival chronology.

The runtime evidence itself is preserved independently of that numbering question.

That distinction is deliberate: the repository records what the artefacts demonstrate without manufacturing historical certainty where the original source record is incomplete.
