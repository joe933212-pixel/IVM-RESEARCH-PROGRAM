import json, sys
sys.path.insert(0, ".")
from ivm_runtime import IVMRuntime, Process, Event, Authority, Rule
runtime=IVMRuntime()
process=Process("business-license","UG-KLA","0.1")
event=Event("E-001","LICENSE_APPLICATION","actor-001",{"application":{"complete":True},"fee":100})
authority=Authority("AUTH-001","actor-001","LICENSING_OFFICER","UG-KLA")
rules=[Rule("R-001","application.complete","equals",True),Rule("R-002","fee","gte",100)]
initial={"applications":{"E-001":{"status":"PENDING"}}}
transition=[{"op":"set","path":"applications.E-001.status","value":"ACTIVE"}]
r=runtime.execute(process=process,event=event,state=initial,authority=authority,rules=rules,transition_operations=transition)
print("STATUS:",r.status); print("TRACE:"," -> ".join(r.trace)); print("STATE:",json.dumps(r.state,indent=2)); print("HISTORY:",json.dumps(r.history.__dict__,indent=2))
material=runtime.execution_material(process=process,event=event,initial_state=initial,authority=authority,rules=rules,transition_operations=transition)
r2=IVMRuntime().replay(execution_material=material)
print("REPLAY STATUS:",r2.status); print("REPLAY STATE IDENTICAL:",r2.state==r.state); print("REPLAY HISTORY IDENTICAL:",r2.history.history_id==r.history.history_id)
