from .canonical import deep_copy, digest
from .model import HistoryRecord, InstitutionalMoment, Transition
from .rules import evaluate_rule
from .transition import apply_transition

def receive_event(ctx):
    ctx.trace.append("RECEIVE_EVENT"); ctx.status = "EVENT_ACCEPTED"

def load_state(ctx, state):
    ctx.trace.append("LOAD_STATE"); ctx.state = deep_copy(state); ctx.status = "STATE_LOADED"

def verify_authority(ctx, authority):
    ctx.trace.append("VERIFY_AUTHORITY")
    if authority is None or not authority.active: raise RuntimeError("AUTHORITY_NOT_ESTABLISHED")
    if authority.actor_id != ctx.event.actor_id: raise RuntimeError("AUTHORITY_ACTOR_MISMATCH")
    if authority.jurisdiction != ctx.process.jurisdiction: raise RuntimeError("AUTHORITY_JURISDICTION_MISMATCH")
    ctx.authority = authority; ctx.status = "AUTHORITY_VERIFIED"

def evaluate_rules(ctx):
    ctx.trace.append("EVALUATE_RULES")
    for rule in ctx.rules:
        if not evaluate_rule(ctx.event.payload, rule): raise RuntimeError(f"RULE_FAILED:{rule.rule_id}")
    ctx.status = "RULES_SATISFIED"

def execute_transition(ctx, operations):
    ctx.trace.append("EXECUTE_TRANSITION"); ctx.transition = Transition(deep_copy(operations)); ctx.status = "TRANSITION_PROVISIONAL"

def commit_state(ctx):
    ctx.trace.append("COMMIT_STATE")
    if ctx.transition is None: raise RuntimeError("NO_PROVISIONAL_TRANSITION")
    ctx.state = apply_transition(ctx.state, ctx.transition.operations); ctx.status = "STATE_COMMITTED"

def record_history(ctx, history_id, moment_id):
    ctx.trace.append("RECORD_HISTORY")
    if ctx.authority is None or ctx.transition is None: raise RuntimeError("INCOMPLETE_COMMIT_CONTEXT")
    ctx.history = HistoryRecord(history_id, ctx.process.process_id, ctx.event.event_id, ctx.authority.authority_id,
        [r.rule_id for r in ctx.rules], {"operations": deep_copy(ctx.transition.operations)},
        digest(ctx._initial_state), digest(ctx.state), moment_id)
    ctx.moment = InstitutionalMoment(moment_id, ctx.process.process_id, ctx.event.event_id,
        deep_copy(ctx.state), {"operations": deep_copy(ctx.transition.operations)}, history_id)
    ctx.status = "HISTORY_RECORDED"

def complete_execution(ctx):
    ctx.trace.append("COMPLETE_EXECUTION"); ctx.status = "COMPLETED"
