import copy
import unittest
from ivm_runtime import IVMRuntime, Process, Event, Authority, Rule

class FaultInjectionTests(unittest.TestCase):
    def setUp(self):
        self.process=Process("business-license","UG-KLA","0.1")
        self.event=Event("E-FAULT-001","LICENSE_APPLICATION","actor-001",{"application":{"complete":True},"fee":100})
        self.authority=Authority("AUTH-001","actor-001","LICENSING_OFFICER","UG-KLA")
        self.rules=[Rule("R-001","application.complete","equals",True),Rule("R-002","fee","gte",100)]
        self.initial_state={"applications":{"E-FAULT-001":{"status":"PENDING"}}}
        self.transition=[{"op":"set","path":"applications.E-FAULT-001.status","value":"ACTIVE"}]
    def test_clean_execution_commits(self):
        r=IVMRuntime().execute(process=self.process,event=self.event,state=self.initial_state,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        self.assertEqual(r.status,"COMPLETED"); self.assertEqual(r.state["applications"]["E-FAULT-001"]["status"],"ACTIVE"); self.assertIsNotNone(r.history)
    def test_precommit_authority_failure_preserves_state(self):
        bad=Authority("AUTH-BAD","different-actor","LICENSING_OFFICER","UG-KLA")
        r=IVMRuntime().execute(process=self.process,event=self.event,state=self.initial_state,authority=bad,rules=self.rules,transition_operations=self.transition)
        self.assertEqual(r.status,"TERMINATED"); self.assertEqual(r.state,self.initial_state); self.assertIsNone(r.history)
    def test_execution_material_is_transportable(self):
        rt=IVMRuntime(); m=rt.execution_material(process=self.process,event=self.event,initial_state=self.initial_state,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        r=IVMRuntime().replay(execution_material=copy.deepcopy(m))
        self.assertEqual(r.status,"COMPLETED"); self.assertEqual(r.state["applications"]["E-FAULT-001"]["status"],"ACTIVE")
    def test_replay_is_independent_of_first_runtime(self):
        rt=IVMRuntime(); first=rt.execute(process=self.process,event=self.event,state=self.initial_state,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        m=rt.execution_material(process=self.process,event=self.event,initial_state=self.initial_state,authority=self.authority,rules=self.rules,transition_operations=self.transition)
        replay=IVMRuntime().replay(execution_material=m)
        self.assertEqual(first.state,replay.state); self.assertEqual(first.history.history_id,replay.history.history_id); self.assertEqual(first.moment.moment_id,replay.moment.moment_id)

if __name__=="__main__": unittest.main()
