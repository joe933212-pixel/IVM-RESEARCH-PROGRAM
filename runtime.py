from .canonical import deep_copy, digest
from .instructions import receive_event, load_state, verify_authority, evaluate_rules, execute_transition, commit_state, record_history, complete_execution
from .model import ExecutionContext, ExecutionResult, Process, Event, Authority, Rule

CANONICAL_SEQUENCE = ("RECEIVE_EVENT","LOAD_STATE","VERIFY_AUTHORITY","EVALUATE_RULES","EXECUTE_TRANSITION","COMMIT_STATE","RECORD_HISTORY","COMPLETE_EXECUTION")

class IVMRuntime:
    def __init__(self):
        self._committed_events = set()

    def execute(self, *, process, event, state, authority, rules, transition_operations):
        if event.event_id in self._committed_events:
            return ExecutionResult("REJECTED_DUPLICATE_EVENT", deep_copy(state), None, None, [], "EVENT_ALREADY_COMMITTED")
        ctx = ExecutionContext(process, event, deep_copy(state), None, list(rules)); ctx._initial_state = deep_copy(state)
        try:
            receive_event(ctx); load_state(ctx, state); verify_authority(ctx, authority); evaluate_rules(ctx)
            execute_transition(ctx, transition_operations); commit_state(ctx)
            record_history(ctx, self._history_id(ctx), self._moment_id(ctx)); complete_execution(ctx)
            self._committed_events.add(event.event_id)
            return ExecutionResult(ctx.status, deep_copy(ctx.state), ctx.history, ctx.moment, list(ctx.trace), None)
        except Exception as exc:
            return ExecutionResult("TERMINATED", deep_copy(state), None, None, list(ctx.trace), str(exc))

    def replay(self, *, execution_material):
        p = Process(**execution_material["process"]); e = Event(**execution_material["event"])
        a = Authority(**execution_material["authority"]) if execution_material.get("authority") else None
        r = [Rule(**x) for x in execution_material.get("rules", [])]
        return self.execute(process=p, event=e, state=execution_material["initial_state"], authority=a, rules=r, transition_operations=execution_material["transition_operations"])

    @staticmethod
    def execution_material(*, process, event, initial_state, authority, rules, transition_operations):
        return {
            "process": process.__dict__, "event": event.__dict__, "initial_state": deep_copy(initial_state),
            "authority": authority.__dict__ if authority else None,
            "rules": [r.__dict__ for r in rules], "transition_operations": deep_copy(transition_operations),
        }

    @staticmethod
    def _history_id(ctx):
        material = {"process_id":ctx.process.process_id,"event_id":ctx.event.event_id,"authority_id":ctx.authority.authority_id,
                    "rules":[r.rule_id for r in ctx.rules],"transition":{"operations":ctx.transition.operations},
                    "previous_state":digest(ctx._initial_state),"resulting_state":digest(ctx.state)}
        return "H-" + digest(material)[:24]

    @staticmethod
    def _moment_id(ctx):
        return "M-" + digest({"process_id":ctx.process.process_id,"event_id":ctx.event.event_id,"resulting_state":digest(ctx.state)})[:24]
