# Research Evidence Chain

The current executable research record forms a continuous chain:

**v0.1 — establish the executable baseline.**

The runtime tests successful execution, authority and rule rejection, duplicate handling and replay.

**v0.2 — introduce controlled failure.**

The research tests failure around the canonical execution pipeline and begins treating commitment as an explicit boundary.

**v0.3 — map the failure surface.**

The canonical fault matrix exposes a concrete gap between State commitment and History recording.

**v0.4 — introduce recoverable transactional commitment.**

A durable transaction record represents the transition as `PREPARED → STATE_COMMITTED → HISTORY_ATTACHED → FINALIZED`.

**004A — terminate the process.**

A separate worker is actually killed and a fresh process recovers the durable transaction record without re-executing the transition.

**005 — challenge the abstraction.**

A conventional deterministic state machine is tested against the same semantic contract.

This chain is the central empirical story of the current IVM research archive.

It does not prove that IVM is novel.

It demonstrates that the research has progressed through explicit hypotheses, executable tests, observed failure, architectural modification and comparative challenge.
