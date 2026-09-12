"""Timing counterexamples: arrival, response and precautionary hold are separate inputs."""
from governing_execute.study import setup


def episode(arrival, delay, immediate_hold):
    w = setup("review", 3)
    for tick in range(1, 11):
        if tick == arrival:
            w.report(tick, "hazard", "hazard", 20 if delay is None else delay,
                     suppressed=True)
            if not immediate_hold:
                w.frozen.clear()
        w.resolve_due(tick)
        w.act(tick, "a", unsafe=True, legitimate=False)
        w.act(tick, "b", action="aux")
    actions = [e for e in w.events if e["kind"] == "action"]
    return dict(arrival=arrival, delay=delay, immediate_hold=immediate_hold,
                hazardous_effects=sum(e["accepted"] and e["unsafe"] for e in actions),
                auxiliary_effects=sum(e["accepted"] and e["action"] == "aux" for e in actions),
                committed_cost=w.nodes["root"].subtree_spent,
                unresolved=sum(r["resolved"] is None for r in w.reports.values()),
                events=w.events)


def run(cases):
    return [episode(**case) for case in cases]
