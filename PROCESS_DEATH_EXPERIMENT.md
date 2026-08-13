
# Experiment 004A — Actual Process Death and Recovery

## Question

Can the v0.4 commitment model survive actual process termination and allow a fresh runtime to recover the prepared institutional transaction without re-executing the transition?

## Method

The experiment uses a separate operating-system process as the execution worker.

The worker writes a durable JSON transaction journal and then terminates itself with a non-zero exit code at a defined transaction phase.

A separate test process then reads the journal as a fresh runtime would.

The experiment therefore distinguishes:

- ordinary exception handling inside one process;
- simulated interruption;
- actual process termination followed by restart/recovery.

## Cases

### Case A — Process death after STATE_COMMITTED

The worker persists:

PREPARED transaction data

plus the candidate State

and marks the transaction:

STATE_COMMITTED

The process then terminates.

The recovery process must find the journal intact and must recover the exact candidate State without executing the transition again.

### Case B — Process death after HISTORY_ATTACHED

The worker persists the History and Moment identifiers and then terminates.

A fresh process must recover the transaction with those identifiers intact.

## Result

The process-death tests pass.

The durable journal survives the worker process terminating with a non-zero exit code.

A fresh process can reconstruct the exact transaction record, including the candidate State and transaction phase.

No transition is re-executed during recovery.

## What This Establishes

The experiment establishes that the v0.4 transaction record can survive actual process death at the tested boundaries and can be consumed by a new process without inventing a new institutional transition.

## What This Does NOT Establish

This is not yet a production-grade durability or crash-consistency proof.

The journal is a small local file-based research mechanism.

The experiment does not establish:

- filesystem durability guarantees under sudden power loss;
- multi-process concurrent recovery;
- distributed transaction atomicity;
- replicated journal consensus;
- Byzantine fault tolerance;
- corruption detection or repair;
- recovery when the process dies during the physical persistence operation itself.

Those remain future experiments.

## Research Significance

v0.3 identified the State/History boundary as a failure surface.

v0.4 introduced a recoverable transaction record.

Experiment 004A now demonstrates that the record survives an actual process termination and can be recovered by a fresh process.

The next question is therefore no longer whether the transaction can survive an ordinary software exception.

It is whether the commitment protocol remains correct under increasingly realistic failure conditions.
