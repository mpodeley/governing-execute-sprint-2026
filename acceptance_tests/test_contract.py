import unittest
from acceptance_contract.broker import reference, local_accounting, stale_ancestry
from acceptance_contract.probes import evaluate
from acceptance_contract.timing import episode


class AcceptanceTests(unittest.TestCase):
    def test_reference_and_isolated_failures(self):
        for factory, expected in ((reference, set()), (local_accounting, {"C2"}),
                                  (stale_ancestry, {"C3", "C4"})):
            with self.subTest(adapter=factory.__name__):
                rows = evaluate(factory, factory.__name__)
                self.assertEqual({r["probe"] for r in rows if not r["passed"]}, expected)

    def test_deny_all_does_not_pass(self):
        def broken():
            b = reference()
            b.act = lambda *args, **kwargs: False
            return b
        rows = evaluate(broken, "deny_all")
        self.assertEqual({r["probe"] for r in rows if not r["passed"]},
                         {"C2", "C3", "C4", "C5", "C6", "C7", "C8"})

    def test_erasing_spend_fails(self):
        def broken():
            b = reference()
            revoke = b.revoke
            def erase(tick, name):
                revoke(tick, name)
                for node in b.world.nodes.values():
                    node.subtree_spent = 0
            b.revoke = erase
            return b
        rows = evaluate(broken, "erase")
        self.assertFalse(next(r for r in rows if r["probe"] == "C5")["passed"])

    def test_timing_boundary(self):
        for arrival, delay, hold, hazards, unresolved in (
                (1, 6, True, 0, 0), (4, 6, True, 3, 0),
                (4, 6, False, 9, 0), (4, None, True, 3, 1),
                (4, None, False, 10, 1), (None, None, True, 10, 0)):
            with self.subTest(arrival=arrival, delay=delay, hold=hold):
                row = episode(arrival, delay, hold)
                self.assertEqual(row["hazardous_effects"], hazards)
                self.assertEqual(row["auxiliary_effects"], 10)
                self.assertEqual(row["committed_cost"], hazards + 10)
                self.assertEqual(row["unresolved"], unresolved)


if __name__ == "__main__":
    unittest.main()
