"""Recount published metrics from events without invoking the simulation engine."""
from collections import defaultdict
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    grouped = defaultdict(list)
    for line in (ROOT/"results/final/traces.jsonl").read_text().splitlines():
        e = json.loads(line)
        grouped[e["run_id"]].append(e)
    rows = list(csv.DictReader((ROOT/"results/final/metrics.csv").open()))
    assert len(rows) == len(grouped) == 192
    for row in rows:
        es = grouped[row["run_id"]]
        assert [e["seq"] for e in es] == list(range(len(es)))
        assert [e["tick"] for e in es] == sorted(e["tick"] for e in es)
        a = [e for e in es if e["kind"] == "action"]
        acc = [e for e in a if e["accepted"]]
        rs = [e for e in es if e["kind"] == "resolution"]
        reports = [e for e in es if e["kind"] == "report"]
        spend = 0
        for e in a:
            if e["accepted"]:
                spend += e["cost"]
            assert spend == e["root_spent"], (row["run_id"], "ledger")
        values = dict(attempted=len(a), accepted=len(acc),
            unauthorized_accepted=sum(bool(e["violations"]) for e in acc),
            invalid_grants=sum(e["accepted"] and bool(e["violations"])
                               for e in es if e["kind"] == "delegate"),
            budget_excess=max(0, spend-100), spent=spend,
            post_revocation=sum("revoked" in e["violations"] for e in acc),
            unsafe_accepted=sum(e["unsafe"] for e in acc),
            legitimate_opportunities=sum(e["legitimate"] for e in a),
            legitimate_completed=sum(e["legitimate"] and not e["violations"] for e in acc),
            legitimate_blocked=sum(e["legitimate"] and not e["accepted"] for e in a),
            false_hold_blocks=sum(e["legitimate"] and e["reason"] == "review_hold" for e in a),
            reports=len(reports), resolved=len(rs), unresolved=len(reports)-len(rs),
            resolution_latency=sum(e["latency"] for e in rs) if rs else "")
        for k, v in values.items():
            assert row[k] == str(v), (row["run_id"], k, row[k], v)
    # Independent arithmetic checks on the authored grid, including benign costs.
    expected = {"log": (66, 360, 288, 60), "local": (54, 360, 288, 60),
                "hierarchy": (0, 0, 288, 60), "review": (0, 0, 316, 0)}
    keys = ("unauthorized_accepted", "budget_excess", "legitimate_completed", "unsafe_accepted")
    for regime, values in expected.items():
        assert tuple(sum(int(r[k]) for r in rows if r["regime"] == regime) for k in keys) == values
    print("PASS: all metric cells recounted from traces; ledgers and aggregate arithmetic agree.")


if __name__ == "__main__":
    verify()
