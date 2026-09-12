import itertools
import json
import unittest
from governing_execute.model import World
from governing_execute.study import ROOT, episode, setup, summarize

CFG = json.loads((ROOT/"configs/study.json").read_text())


class Controls(unittest.TestCase):
    def test_budget_conserved_for_every_order(self):
        for regime in ("hierarchy", "review"):
            for costs in itertools.permutations((20, 40, 60)):
                w = setup(regime, 3)
                for t, cost in enumerate(costs, 1):
                    w.act(t, "a" if t % 2 else "b", cost=cost)
                self.assertLessEqual(w.nodes["root"].subtree_spent, 100)
                self.assertEqual(w.nodes["root"].subtree_spent,
                                 sum(n.own_spent for n in w.nodes.values()))

    def test_local_budget_does_not_conserve_root(self):
        w = setup("local", 3)
        w.act(1, "a", cost=80)
        w.act(1, "b", cost=80)
        self.assertEqual(w.nodes["root"].subtree_spent, 160)

    def test_intermediate_budget(self):
        w = World("hierarchy", 3)
        w.delegate(0, "root", "limited", 50, 12, {"work"})
        for name in ("a", "b"):
            w.delegate(0, "limited", name, 50, 12, {"work"})
        self.assertTrue(w.act(1, "a", cost=30)["accepted"])
        self.assertFalse(w.act(2, "b", cost=30)["accepted"])
        self.assertEqual(w.nodes["root"].subtree_spent, 30)

    def test_grant_attenuation(self):
        for field, value in (("budget", 101), ("expires", 13),
                             ("permissions", {"outside"})):
            w = setup("hierarchy", 3)
            args = dict(budget=100, expires=12, permissions={"work"})
            args[field] = value
            self.assertFalse(w.delegate(1, "root", "new", **args)["accepted"])
        w = setup("review", 1)
        self.assertFalse(w.delegate(1, "a", "too_deep", 10, 12, {"work"})["accepted"])

    def test_pending_revalidated_and_past_effect_retained(self):
        w = setup("hierarchy", 3)
        w.act(0, "a", cost=10)
        w.queue(1, "q", name="b", cost=20)
        w.revoke(2, "branch1")
        self.assertFalse(w.execute_pending(3, "q")["accepted"])
        self.assertEqual(w.nodes["root"].subtree_spent, 10)
        self.assertFalse(w.delegate(3, "branch2", "c", 10, 12, {"work"})["accepted"])

    def test_expiry_exact_boundary(self):
        w = setup("hierarchy", 3)
        w.nodes["root"].expires = 4
        self.assertTrue(w.act(3, "a")["accepted"])
        self.assertFalse(w.act(4, "a")["accepted"])

    def test_false_report_scope_and_expansion(self):
        w = setup("review", 3)
        w.report(1, "r", "false_alarm", 2)
        self.assertFalse(w.act(1, "a")["accepted"])
        self.assertTrue(w.act(1, "b", action="aux")["accepted"])
        self.assertFalse(w.delegate(1, "root", "c", 10, 12, {"work"})["accepted"])
        w.resolve_due(3)
        self.assertTrue(w.act(3, "a")["accepted"])

    def test_second_report_keeps_hold(self):
        w = setup("review", 1)
        w.report(1, "r1", "false_alarm", 0)
        w.report(1, "r2", "false_alarm", 6)
        w.resolve_due(1)
        self.assertFalse(w.act(2, "a")["accepted"])
        w.resolve_due(7)
        self.assertTrue(w.act(7, "a")["accepted"])

    def test_silence_never_grants_input(self):
        w = setup("review", 1)
        w.input_available = False
        w.report(1, "r", "missing_input", 20)
        for t in range(2, 12):
            w.resolve_due(t)
            self.assertFalse(w.act(t, "a")["accepted"])

    def test_negative_cost_and_duplicate_queue(self):
        w = setup("review", 1)
        with self.assertRaises(ValueError):
            w.act(1, "a", cost=-10)
        w.queue(1, "q", name="a")
        with self.assertRaises(ValueError):
            w.queue(1, "q", name="b")

    def test_full_grid_control_contract(self):
        count = 0
        for sc, regime, delay, depth in itertools.product(
                CFG["scenarios"], CFG["regimes"], CFG["delays"], CFG["depths"]):
            w = episode(sc, regime, delay, depth)
            m = summarize(w, sc, delay, depth)
            count += 1
            if regime in ("hierarchy", "review"):
                for key in ("unauthorized_accepted", "invalid_grants", "budget_excess", "post_revocation"):
                    self.assertEqual(m[key], 0, (sc, regime, key))
            if sc["id"] == "false_alarm" and regime == "review":
                self.assertEqual(m["false_hold_blocks"], delay)
                self.assertEqual(m["legitimate_completed"], 20-delay)
            if sc["id"] == "missing_input":
                self.assertEqual(m["legitimate_completed"], 20-delay if regime == "review" else 10)
            if sc["id"] == "suppressed_minority" and regime == "review":
                self.assertEqual(m["unsafe_accepted"], 0)
                self.assertEqual(m["resolved"], 1)
                self.assertTrue(next(e for e in w.events if e["kind"] == "report")["direct_bypass"])
            self.assertEqual([e["seq"] for e in w.events], list(range(len(w.events))))
        self.assertEqual(count, 192)

    def test_coverage_counterexample(self):
        sc = next(s for s in CFG["scenarios"] if s["id"] == "suppressed_minority")
        good = summarize(episode(sc, "review", 2, 3), sc, 2, 3)
        bad = summarize(episode(sc, "review", 2, 3, coverage=False), sc, 2, 3)
        self.assertEqual(good["unsafe_accepted"], 0)
        self.assertEqual(bad["unsafe_accepted"], 10)
        self.assertEqual(bad["unauthorized_accepted"], 8)


if __name__ == "__main__":
    unittest.main()
