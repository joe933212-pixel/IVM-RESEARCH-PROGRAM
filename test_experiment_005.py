import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from conformance.canonical import CanonicalTransition
from conformance.harness import compare
from comparators.state_machine import ConventionalStateMachine

class Experiment005Tests(unittest.TestCase):
    def setUp(self):
        self.c = CanonicalTransition()
        self.sm = ConventionalStateMachine()

    def test_canonical_transition(self):
        actual = self.sm.execute(self.c.as_context())
        ok, diff = compare(actual, self.c.expected_result())
        self.assertTrue(ok, diff)

    def test_duplicate_event(self):
        self.sm.execute(self.c.as_context())
        before = len(self.sm.transitions)
        result = self.sm.execute(self.c.as_context())
        self.assertEqual(len(self.sm.transitions), before)
        self.assertEqual(result["duplicate_event"], "NO_SECOND_TRANSITION")

    def test_rule_version_change_does_not_rewrite_history(self):
        self.sm.execute(self.c.as_context())
        self.sm.add_rule_version("LICENCE-RULES", "2.0", eligible=False)
        self.assertEqual(self.sm.transitions["T-001"]["rule_version"], "1.0")
        self.assertEqual(self.sm.replay("T-001"), "EQUIVALENT")

    def test_revoked_authority_blocks_new_transition(self):
        self.sm.revoke_authority("AUTHORITY-001")
        with self.assertRaisesRegex(ValueError, "authority revoked"):
            self.sm.execute(self.c.as_context())

    def test_harness_detects_semantic_difference(self):
        expected = self.c.expected_result()
        actual = dict(expected)
        actual["commitment_status"] = "STATE_COMMITTED"
        ok, diff = compare(actual, expected)
        self.assertFalse(ok)
        self.assertIn("commitment_status", diff)

if __name__ == "__main__":
    unittest.main(verbosity=2)
