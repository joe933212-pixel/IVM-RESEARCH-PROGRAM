import unittest
from ivm_runtime import IVMRuntime, Process, Event, Authority, Rule

class RuntimeTests(unittest.TestCase):
    def setUp(self):
        self.runtime=IVMRuntime(); self.process=Process("business-license","UG-KLA","0.1")
        self.event=Event("E-001","LICENSE_APPLICATION","actor-001",{"application":{"complete":True},"fee":100})
        self.authority=Authority("AUTH-001","actor-001","LICENSING_OFFICER","UG-KLA")
        self.rules=[Rule("R-001","application.complete","equals",True),Rule("R-002","fee","gte",100)]
        self.initial={"applications":{"E-001":{"status":"PENDING"}}}
        self.transition=[{"op":"set","path":"applications.E-001.status","value":"ACTIVE"}]
    def execute(self, **kw): return self.runtime.execute(process=self.process,event=self.event,state=self.initial,authority=self.authority,rules=self.rules,transition_operations=self.transition,**kw)
    def test_success(self):
        r=self.execute(); self.assertEqual(r.status,"COMPLETED"); self.assertEqual(r.state["applications"]["E-001"]["status"],"ACTIVE")
        self.assertEqual(r.trace,list(__import__('ivm_runtime.runtime',fromlist=['CANONICAL_SEQUENCE']).CANONICAL_SEQUENCE)); self.assertIsNotNone(r.history)
    def test_authority_failure_preserves_state(self):
        bad=Authority("AUTH-002","other","LICENSING_OFFICER","UG-KLA")
        r=self.runtime.execute(process=self.process,event=self.event,state=self.initial,authority=bad,rules=self.rules,transition_operations=self.transition)
        self.assertEqual(r.status,"TERMINATED"); self.assertEqual(r.state,self.initial); self.assertIsNone(r.history)
    def test_rule_failure_preserves_state(self):
        r=self.runtime.execute(process=self.process,event=self.event,state=self.initial,authority=self.authority,rules=[Rule("R-X","application.complete","equals",False)],transition_operations=self.transition)
        self.assertEqual(r.status,"TERMINATED"); self.assertEqual(r.state,self.initial)
    def test_duplicate(self):
        a=self.execute(); b=self.runtime.execute(process=self.process,event=self.event,state=a.state,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        self.assertEqual(a.status,"COMPLETED"); self.assertEqual(b.status,"REJECTED_DUPLICATE_EVENT")
    def test_replay(self):
        material=self.runtime.execution_material(process=self.process,event=self.event,initial_state=self.initial,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        a=self.execute(); b=IVMRuntime().replay(execution_material=material)
        self.assertEqual(a.state,b.state); self.assertEqual(a.history.history_id,b.history.history_id); self.assertEqual(a.moment.moment_id,b.moment.moment_id)

if __name__=="__main__": unittest.main()
