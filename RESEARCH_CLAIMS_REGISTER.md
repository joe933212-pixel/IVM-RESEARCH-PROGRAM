# Research Claims Register

## Purpose

This register distinguishes what the current IVM research record demonstrates from what it proposes, infers or has not yet tested.

The purpose is to prevent the repository from converting experimental observations into stronger claims than the evidence supports.

## Claim 001 — The IVM model can be expressed as executable transition semantics

**Classification:** Demonstrated at prototype level.

The reference runtime implements a canonical execution pipeline involving event receipt, state loading, authority verification, rule evaluation, transition execution, state commitment, history recording and completion.

The evidence establishes an executable prototype of the proposed semantics. It does not establish that the semantics are novel.

**Evidence:** `runtime/reference/versions/v0.1/`, `runtime/reference/versions/v0.4/`

## Claim 002 — Controlled failure can expose semantic failure boundaries

**Classification:** Demonstrated experimentally.

The v0.2 and v0.3 work introduced controlled interruption around the execution pipeline. The v0.3 fault matrix exposed a boundary in which State could be committed before corresponding History was attached.

This is an observed property of the prototype under the tested conditions.

**Evidence:** `results/v0.4/FAULT_MATRIX_FINDINGS.md`, `runtime/reference/versions/v0.3/`

## Claim 003 — v0.4 provides a recoverable transactional representation of the State/History boundary

**Classification:** Demonstrated at prototype level.

The v0.4 implementation represents the transaction through `PREPARED → STATE_COMMITTED → HISTORY_ATTACHED → FINALIZED` and stores sufficient local journal material to recover the tested transaction state.

The result does not establish general database-grade transactional guarantees.

**Evidence:** `results/v0.4/TRANSACTIONAL_COMMIT_v0.4.md`

## Claim 004 — The tested v0.4 transaction survives actual process termination

**Classification:** Demonstrated under defined experimental conditions.

Experiment 004A deliberately terminates a separate worker process and subsequently starts a fresh process. The fresh process recovers the durable transaction record without re-executing the transition.

The historical record reports 23 tests run and 23 passed.

This does not establish power-loss durability, distributed atomicity, concurrency safety, replication or corruption recovery.

**Evidence:** `results/v0.4/PROCESS_DEATH_EXPERIMENT.md`, `results/v0.4/TEST_RESULTS_PROCESS_DEATH.txt`

## Claim 005 — A conventional deterministic state machine can satisfy the current Experiment 005 semantic contract

**Classification:** Demonstrated for the current conformance harness.

The available comparator passes five conformance tests covering the current canonical semantic contract.

This result is important because it is a direct challenge to the IVM proposition. It does not by itself establish equivalence, non-equivalence or novelty.

**Evidence:** `experiments/005/`, `results/experiment-005/`

## Claim 006 — The IVM abstraction is novel

**Classification:** Not established.

The repository explicitly does not make this claim.

The prior-art and literature analysis is incomplete in the public package and continues from Section 54. Comparative research is also still active.

## Claim 007 — Conventional systems cannot represent institutional semantics

**Classification:** Not established and currently too strong.

Experiment 005 exists specifically to test this proposition rather than assume it.

## Claim 008 — IVM is commercially superior to existing architectures

**Classification:** Not tested.

No commercial superiority claim should be made on the basis of the current evidence.

## Claim 009 — IVM is production-ready

**Classification:** Not established.

The current runtime is a research prototype. Its v0.4 journal is a local JSON mechanism and its limitations are explicitly recorded.

## Claim 010 — The research programme is fundable as an independent validation programme

**Classification:** Research proposition.

The evidence now supports a concrete next-stage programme involving comparative implementations, formalisation, storage and concurrency testing, independent review, security analysis and reproducibility work.

The funding case should be based on the existence of a testable hypothesis and an accumulated experimental record, not on an assertion that the final answer is already known.

## Claim Discipline

Every new research claim should be assigned one of the following statuses before being promoted into a public conclusion:

**Demonstrated experimentally.**

**Supported by implementation evidence.**

**Derived interpretation.**

**Hypothesis.**

**Prior-art dependent.**

**Not yet tested.**

**Explicitly not claimed.**

The register should be updated whenever a new experiment materially changes the status of a claim.
