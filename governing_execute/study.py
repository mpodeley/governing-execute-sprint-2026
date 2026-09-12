"""Authored fixture schedules and descriptive metrics, not behavioral sampling."""
import csv
import hashlib
import itertools
import json
from pathlib import Path
from .model import World

ROOT = Path(__file__).resolve().parents[1]


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def setup(regime, depth, budget=100):
    w = World(regime, depth, budget)
    parent = "root"
    for d in range(1, depth):
        name = f"branch{d}"
        w.delegate(0, parent, name, budget, 12, {"work", "aux"})
        parent = name
    for name in ("a", "b"):
        w.delegate(0, parent, name, budget, 12, {"work", "aux"})
    return w


def episode(scenario, regime, delay, depth, horizon=12, budget=100, coverage=True):
    w = setup(regime, depth, budget)
    schedule = scenario["schedule"]
    if schedule == "missing":
        w.input_available = False
    if schedule == "expired":
        # Valid initial descendants inherit the shortened lease. A new request
        # then tries to obtain a longer lease from the same parent.
        for n in w.nodes.values():
            n.expires = 4
    for t in range(horizon):
        if t == 1:
            if schedule == "overdelegate":
                w.delegate(t, "a", "rogue", budget, 12, {"work"})
            elif schedule == "expired":
                parent = w.nodes["a"].parent
                w.delegate(t, parent, "extended", budget, 12, {"work"})
            elif schedule == "revoked":
                w.queue(t, "delayed", name="a", action="work", cost=10,
                        legitimate=False)
            elif schedule in ("missing", "false", "suppressed"):
                kind = {"missing": "missing_input", "false": "false_alarm",
                        "suppressed": "hazard"}[schedule]
                w.report(t, "r1", kind, delay, suppressed=schedule == "suppressed")
        if schedule == "revoked" and t == 2:
            w.revoke(t, w.nodes["a"].parent)
        # Reports arrive before responses; due responses precede this tick's effects.
        w.resolve_due(t)
        if schedule == "routine" and 1 <= t <= 4:
            w.act(t, "a" if t % 2 else "b", cost=10)
        elif schedule == "split" and 1 <= t <= 4:
            w.act(t, "a" if t % 2 else "b", cost=40, legitimate=t <= 2)
        elif schedule == "overdelegate" and t in (2, 3):
            w.act(t, "rogue", cost=10, legitimate=False)
        elif schedule == "expired" and t in (3, 5, 7):
            w.act(t, "a", cost=10, legitimate=t < 4)
            w.act(t, "extended", cost=10, legitimate=False)
        elif schedule == "revoked":
            if t == 0:
                w.act(t, "a", cost=10)
            elif t == 3:
                w.execute_pending(t, "delayed")
            elif t == 4:
                w.act(t, "b", cost=10, legitimate=False)
        elif schedule in ("missing", "false", "suppressed") and 1 <= t <= 10:
            w.act(t, "a", cost=1, legitimate=schedule != "suppressed",
                  unsafe=schedule == "suppressed", covered=coverage)
            w.act(t, "b", action="aux", cost=1)
    return w


def summarize(w, scenario, delay, depth):
    actions = [e for e in w.events if e["kind"] == "action"]
    accepted = [e for e in actions if e["accepted"]]
    resolutions = [e for e in w.events if e["kind"] == "resolution"]
    return dict(scenario=scenario["id"], regime=w.regime, delay=delay, depth=depth,
        attempted=len(actions), accepted=len(accepted),
        unauthorized_accepted=sum(bool(e["violations"]) for e in accepted),
        invalid_grants=sum(e["accepted"] and bool(e["violations"])
                           for e in w.events if e["kind"] == "delegate"),
        budget_excess=max(0, w.nodes["root"].subtree_spent-w.budget),
        post_revocation=sum("revoked" in e["violations"] for e in accepted),
        unsafe_accepted=sum(e["unsafe"] for e in accepted),
        legitimate_opportunities=sum(e["legitimate"] for e in actions),
        legitimate_completed=sum(e["legitimate"] and not e["violations"] for e in accepted),
        legitimate_blocked=sum(e["legitimate"] and not e["accepted"] for e in actions),
        false_hold_blocks=sum(e["legitimate"] and e["reason"] == "review_hold" for e in actions),
        reports=len(w.reports), resolved=len(resolutions),
        resolution_latency=sum(e["latency"] for e in resolutions) if resolutions else "",
        unresolved=sum(r["resolved"] is None for r in w.reports.values()),
        spent=w.nodes["root"].subtree_spent)


def design_files():
    return sorted([*ROOT.glob("governing_execute/*.py"), *ROOT.glob("tests/*.py"),
                   ROOT/"configs/study.json", ROOT/"docs/design.md"])


def design_hashes():
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in design_files()}


def run(out, freeze):
    frozen = json.loads(Path(freeze).read_text())
    if frozen["files"] != design_hashes():
        raise RuntimeError("Design differs from freeze; preserve old freeze and create a new one.")
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    cfg = json.loads((ROOT/"configs/study.json").read_text())
    rows = []
    with (out/"traces.jsonl").open("w") as trace:
        for scenario, regime, delay, depth in itertools.product(
                cfg["scenarios"], cfg["regimes"], cfg["delays"], cfg["depths"]):
            w = episode(scenario, regime, delay, depth, cfg["horizon"], cfg["root_budget"])
            run_id = f'{scenario["id"]}-{regime}-d{delay}-h{depth}'
            for event in w.events:
                trace.write(canonical(dict(run_id=run_id, **event))+"\n")
            rows.append(dict(run_id=run_id, **summarize(w, scenario, delay, depth)))
    with (out/"metrics.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    # Separate coverage counterexample, excluded from the 192 cells.
    sc = next(s for s in cfg["scenarios"] if s["id"] == "suppressed_minority")
    coverage = []
    for covered in (True, False):
        w = episode(sc, "review", 2, 3, coverage=covered)
        coverage.append(dict(covered=covered, metrics=summarize(w, sc, 2, 3), events=w.events))
    (out/"coverage.json").write_text(canonical(coverage)+"\n")
    manifest = dict(design=frozen, configurations=len(rows),
                    artifacts={p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                               for p in sorted(out.iterdir())})
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
    return rows
