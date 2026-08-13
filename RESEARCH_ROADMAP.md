# IVM Research Roadmap

## Purpose

The roadmap defines the next research stages required to determine whether the Institutional Virtual Machine represents a materially distinct computational abstraction and whether the observed prototype properties survive stronger tests.

The roadmap is intentionally evidence-driven. A later stage should be undertaken because an earlier result creates a specific unanswered question, not because the repository needs additional features.

## Stage 1 — Complete the historical research record

Reconcile the experiment register against the original laboratory material and import the complete prior-art and literature analysis through Section 53, followed by the verified continuation beginning at Section 54.

**Output:** auditable research chronology and complete literature record.

## Stage 2 — Comparative execution

Extend Experiment 005 beyond the conventional deterministic state machine.

The next comparisons should be selected according to explicit research questions and should include process-death recovery where relevant.

**Output:** implementation-independent comparative evidence.

## Stage 3 — Concurrency and duplicate recovery

Test concurrent recovery attempts, duplicate recovery requests and competing transitions against the same durable transaction record.

**Research question:** Does the commitment model remain deterministic when more than one recovery actor can observe the same incomplete transaction?

## Stage 4 — Persistence-boundary testing

Move beyond process death and test failures during persistence itself, including interruption around file replacement, flush and journal update boundaries.

**Research question:** Which guarantees belong to the IVM protocol and which depend on the underlying storage substrate?

## Stage 5 — Formal semantic specification

Separate the semantic contract from the current Python implementation.

Define the transition, authority, rule-version, history and recovery invariants independently of implementation language.

**Output:** a formal or semi-formal conformance specification.

## Stage 6 — Independent replication

Provide sufficient instructions for an external researcher to reproduce the canonical experiments without access to the original development environment.

**Output:** reproducibility package and independent replication report.

## Stage 7 — Security analysis

Subject the transition and recovery model to adversarial analysis, including tampered journal material, replay attempts, authority substitution and malformed transitions.

**Output:** security threat model and test results.

## Stage 8 — Realistic systems evaluation

Evaluate the semantic model against increasingly realistic storage, identity, network and distributed-execution conditions.

**Output:** evidence about the boundary between prototype semantics and deployable infrastructure.

## Stage 9 — Independent technical review

Invite researchers and engineers with relevant expertise to attempt to reproduce, challenge or falsify the central proposition.

**Output:** public review record and response matrix.

## Stage 10 — Architectural conclusion

Only after the comparative, formal and independent-review stages should the programme make a strong conclusion about whether IVM constitutes a distinct abstraction, a useful synthesis of existing mechanisms or an unnecessary layer.

The desired result is not a predetermined verdict.

The desired result is a defensible one.
