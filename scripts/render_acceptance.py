"""Render paper/site tables from retained contract evidence; verify independent counts."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def render():
    matrix = json.loads((ROOT/"results/acceptance/matrix.json").read_text())
    timing = json.loads((ROOT/"results/acceptance/timing.json").read_text())
    generated = ROOT/"report/latex/generated"
    lines = [r"\begin{tabularx}{\linewidth}{@{}lXccc@{}}\toprule",
             r" & Obligation & Reference & Local spend & Stale ancestry\\\midrule"]
    summary = ["# Acceptance results — v0.2", "", "| Probe | Reference | Local spend | Stale ancestry |", "|---|---|---|---|"]
    for code in (f"C{i}" for i in range(1, 9)):
        rows = {r["adapter"]: r for r in matrix if r["probe"] == code}
        first = rows["reference"]
        cells = ["PASS" if rows[a]["passed"] else "FAIL" for a in
                 ("reference", "local_accounting", "stale_ancestry")]
        lines.append(" & ".join([code, first["title"], *cells]) + r"\\")
        summary.append("| " + " | ".join([code+" "+first["title"], *cells]) + " |")
    lines += [r"\bottomrule\end{tabularx}"]
    (generated/"acceptance.tex").write_text("\n".join(lines)+"\n")
    timing_lines = [r"\begin{tabular}{@{}llrr@{}}\toprule",
                    r"Report arrival & Response delay & Hold on receipt & Decision only\\\midrule"]
    summary += ["", "## Report timing: hazardous effects out of ten opportunities", "",
                "| Arrival | Response delay | Hold on receipt | Decision only |", "|---|---|---|---|"]
    for arrival, delay in [(a, d) for a in (1, 4) for d in (0, 2, 6, None)] + [(None, None)]:
        pair = {r["immediate_hold"]: r for r in timing if r["arrival"] == arrival and r["delay"] == delay}
        values = []
        for hold in (True, False):
            r = pair[hold]
            accepted = [e for e in r["events"] if e["kind"] == "action" and e["accepted"]]
            # Recount by named action, independently of the unsafe scoring annotation.
            assert sum(e["action"] == "work" for e in accepted) == r["hazardous_effects"]
            assert sum(e["action"] == "aux" for e in accepted) == r["auxiliary_effects"] == 10
            assert sum(e["cost"] for e in accepted) == r["committed_cost"]
            assert not any(e["violations"] for e in accepted)
            values.append(str(r["hazardous_effects"]))
        labels = [str(arrival) if arrival is not None else "Absent",
                  str(delay) if delay is not None else ("No response" if arrival else "--")]
        timing_lines.append(" & ".join(labels+values)+r"\\")
        summary.append("| " + " | ".join(labels+values)+" |")
    timing_lines += [r"\bottomrule\end{tabular}"]
    (generated/"timing.tex").write_text("\n".join(timing_lines)+"\n")
    rows = list(csv.DictReader((ROOT/"results/final/metrics.csv").open()))
    expected = {"legitimate": (4,4), "split_budget": (4,2), "overdelegate": (2,0),
                "expired": (6,1), "revoked_pending": (3,1), "missing_input": (20,20),
                "false_alarm": (20,20), "suppressed_minority": (20,10)}
    denominators = [r"\begin{tabular}{@{}lrr@{}}\toprule", r"Schedule & Attempts & Legitimate opportunities\\\midrule"]
    for scenario, counts in expected.items():
        selected = [r for r in rows if r["scenario"] == scenario]
        assert len(selected) == 24
        assert {(int(r["attempted"]), int(r["legitimate_opportunities"])) for r in selected} == {counts}
        denominators.append(scenario.replace("_", r"\_")+f" & {counts[0]} & {counts[1]}"+r"\\")
    denominators += [r"\midrule One schedule set & 79 & 58\\", r"Per regime (six sets) & 474 & 348\\", r"\bottomrule\end{tabular}"]
    (generated/"denominators.tex").write_text("\n".join(denominators)+"\n")
    summary += ["", "Each timing row pairs two deterministic traces; auxiliary effects are 10/10 throughout.",
                "No accepted effect violates its active grant. Receipt timing and response are fixture inputs.",
                "The pass/fail matrix is a contract diagnostic, not a security-rate estimate."]
    (ROOT/"results/acceptance/summary.md").write_text("\n".join(summary)+"\n")
    return matrix, timing


if __name__ == "__main__":
    render()
    print("Rendered and checked acceptance, timing and historical denominator tables")
