from dataclasses import dataclass
from typing import Optional

from .canonical import deep_copy
from .instructions import (
    receive_event,
    load_state,
    verify_authority,
    evaluate_rules,
    execute_transition,
    commit_state,
    record_history,
    complete_execution,
)
from .model import ExecutionContext


@dataclass(frozen=True)
class FaultPoint:
    instruction: str
    timing: str  # "before" or "after"


@dataclass(frozen=True)
class FaultOutcome:
    fault_point: FaultPoint
    interrupted: bool
    state: dict
    history_exists: bool
    moment_exists: bool
    trace: list[str]
    status: str
    error: Optional[str]


CANONICAL_STEPS = (
    "RECEIVE_EVENT",
    "LOAD_STATE",
    "VERIFY_AUTHORITY",
    "EVALUATE_RULES",
    "EXECUTE_TRANSITION",
    "COMMIT_STATE",
    "RECORD_HISTORY",
    "COMPLETE_EXECUTION",
)


def run_with_fault(
    *,
    runtime,
    process,
    event,
    state,
    authority,
    rules,
    transition_operations,
    fault_point: FaultPoint,
) -> FaultOutcome:
    ctx = ExecutionContext(
        process=process,
        event=event,
        state=deep_copy(state),
        authority=None,
        rules=list(rules),
    )
    ctx._initial_state = deep_copy(state)

    def maybe_fault(step, timing):
        if fault_point == FaultPoint(step, timing):
            raise RuntimeError(f"INJECTED_FAULT:{timing}:{step}")

    try:
        maybe_fault("RECEIVE_EVENT", "before")
        receive_event(ctx)
        maybe_fault("RECEIVE_EVENT", "after")

        maybe_fault("LOAD_STATE", "before")
        load_state(ctx, state)
        maybe_fault("LOAD_STATE", "after")

        maybe_fault("VERIFY_AUTHORITY", "before")
        verify_authority(ctx, authority)
        maybe_fault("VERIFY_AUTHORITY", "after")

        maybe_fault("EVALUATE_RULES", "before")
        evaluate_rules(ctx)
        maybe_fault("EVALUATE_RULES", "after")

        maybe_fault("EXECUTE_TRANSITION", "before")
        execute_transition(ctx, transition_operations)
        maybe_fault("EXECUTE_TRANSITION", "after")

        maybe_fault("COMMIT_STATE", "before")
        commit_state(ctx)
        maybe_fault("COMMIT_STATE", "after")

        maybe_fault("RECORD_HISTORY", "before")
        history_id = runtime._history_id(ctx)
        moment_id = runtime._moment_id(ctx)
        record_history(ctx, history_id, moment_id)
        maybe_fault("RECORD_HISTORY", "after")

        maybe_fault("COMPLETE_EXECUTION", "before")
        complete_execution(ctx)
        maybe_fault("COMPLETE_EXECUTION", "after")

        return FaultOutcome(
            fault_point=fault_point,
            interrupted=False,
            state=deep_copy(ctx.state),
            history_exists=ctx.history is not None,
            moment_exists=ctx.moment is not None,
            trace=list(ctx.trace),
            status=ctx.status,
            error=None,
        )

    except Exception as exc:
        return FaultOutcome(
            fault_point=fault_point,
            interrupted=True,
            state=deep_copy(ctx.state),
            history_exists=ctx.history is not None,
            moment_exists=ctx.moment is not None,
            trace=list(ctx.trace),
            status="INTERRUPTED",
            error=str(exc),
        )
