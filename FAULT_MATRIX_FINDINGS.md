# IVM v0.3 — Fault Matrix Findings

## Purpose

v0.3 executes the IVM pipeline under deliberate interruption at every canonical instruction boundary, both immediately before and immediately after the instruction.

This is a research experiment designed to expose the architectural boundary conditions of commitment, history and recovery.

## Result

The matrix demonstrates a critical distinction.

Before COMMIT_STATE, an interrupted execution can preserve the original authoritative State.

After COMMIT_STATE but before RECORD_HISTORY, the prototype can expose a changed State with no corresponding History record.

This is **not treated as a successful property**. It is the central failure discovered by the experiment.

## Architectural implication

The prototype currently separates:

State commitment

from

History recording.

For a production-grade IVM, that separation creates a recoverability problem.

The next research question is therefore:

> Can State commitment and History creation be made one recoverable atomic institutional commitment?

Possible mechanisms are deliberately left open at this stage. The experiment must determine the required semantics before technology is selected.

## Important distinction

The current runtime uses in-memory structures. Therefore this experiment does not prove what a durable storage engine, database transaction, replicated state machine or distributed consensus protocol would do.

It proves something more useful at this stage:

**the architecture has identified a concrete failure boundary that must be resolved.**

That becomes a primary research objective for the next runtime iteration.
