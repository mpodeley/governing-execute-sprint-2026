"""Generate tables and vector figures from retained records, without inference."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/"results/final"
OUT = ROOT/"results/analysis"
OUT.mkdir(exist_ok=True)
FIG = ROOT/"report/latex/figures"
FIG.mkdir(exist_ok=True)
GEN = ROOT/"report/latex/generated"
GEN.mkdir(exist_ok=True)
REGIMES = ["log", "local", "hierarchy", "review"]
NAMES = ["Logging", "Local limits", "Hierarchy", "Hierarchy + review"]
manifest = json.loads((SOURCE/"manifest.json").read_text())
for name, digest in manifest["artifacts"].items():
    assert hashlib.sha256((SOURCE/name).read_bytes()).hexdigest() == digest
rows = list(csv.DictReader((SOURCE/"metrics.csv").open()))
for row in rows:
    for k in row:
        if k not in ("run_id", "scenario", "regime") and row[k] != "":
            row[k] = int(row[k])
assert len(rows) == 192
fields = ["attempted", "unauthorized_accepted", "invalid_grants", "budget_excess",
          "post_revocation", "unsafe_accepted", "legitimate_opportunities",
          "legitimate_completed", "false_hold_blocks", "resolved", "unresolved"]
totals = {r: {k: sum(x[k] for x in rows if x["regime"] == r) for k in fields} for r in REGIMES}
(OUT/"totals.json").write_text(json.dumps(totals, indent=2)+"\n")

def cell(scenario, regime, delay=2, depth=3):
    return next(x for x in rows if (x["scenario"], x["regime"], x["delay"], x["depth"]) ==
                (scenario, regime, delay, depth))

lines = [r"\begin{tabular}{@{}lrrrr@{}}", r"\toprule",
         r"Regime & Violations & Excess & Unsafe & Valid work\\", r"\midrule"]
for regime, name in zip(REGIMES, NAMES):
    t = totals[regime]
    lines.append(f'{name} & {t["unauthorized_accepted"]} & {t["budget_excess"]} & '
                 f'{t["unsafe_accepted"]} & {t["legitimate_completed"]}/{t["legitimate_opportunities"]}'+r"\\")
lines += [r"\bottomrule", r"\end{tabular}"]
(GEN/"totals.tex").write_text("\n".join(lines)+"\n")
macro = []
for regime, prefix in zip(REGIMES, ("Log", "Local", "Hierarchy", "Review")):
    for field, suffix in (("unauthorized_accepted", "Violations"), ("budget_excess", "Excess"),
                          ("unsafe_accepted", "Unsafe"), ("legitimate_completed", "Completed"),
                          ("false_hold_blocks", "FalseBlocks")):
        macro.append("\\newcommand{\\"+prefix+suffix+"}{"+str(totals[regime][field])+"}")
(GEN/"counts.tex").write_text("\n".join(macro)+"\n")

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False,
                     "pdf.fonttype": 42, "savefig.bbox": "tight"})
colors = ["#929aa1", "#657789", "#205f82", "#177b72"]
fig, axes = plt.subplots(1, 2, figsize=(8, 2.65), constrained_layout=True)
for ax, key, title in zip(axes, ("unauthorized_accepted", "budget_excess"),
                           ("Out-of-mandate effects", "Root budget excess (units)")):
    vals = [totals[r][key] for r in REGIMES]
    ax.bar(range(4), vals, color=colors)
    for i, val in enumerate(vals):
        ax.text(i, val + max(vals)*.025, str(val), ha="center", fontsize=10)
    ax.set_xticks(range(4), ["Log", "Local", "Hierarchy", "+ review"])
    ax.set_title(title, fontsize=11)
    ax.set_ylim(0, max(vals)*1.23)
fig.savefig(FIG/"controls.pdf")
fig.savefig(FIG/"controls.png", dpi=160)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(8, 2.65), constrained_layout=True)
delays = [0, 2, 6]
ax = axes[0]
ax.plot(delays, [cell("missing_input", "review", d)["legitimate_completed"] for d in delays],
        "o-", color=colors[3], label="Hierarchy + review")
ax.plot(delays, [cell("missing_input", "hierarchy", d)["legitimate_completed"] for d in delays],
        "s--", color=colors[2], label="Hierarchy")
ax.set(title="Missing input: valid work / 20", xlabel="Review delay (logical steps)",
       xticks=delays, ylim=(0, 21), yticks=[0, 5, 10, 15, 20])
ax.legend(frameon=False, fontsize=8, loc="lower right")
ax = axes[1]
ax.plot(delays, [cell("false_alarm", "review", d)["false_hold_blocks"] for d in delays],
        "o-", color="#ad6843", label="Valid work blocked")
ax.set(title="False complaint: lost work / 10", xlabel="Review delay (logical steps)",
       xticks=delays, ylim=(-.3, 10.5), yticks=[0, 2, 4, 6, 8, 10])
ax.text(.15, 8.7, "All 10 auxiliary actions survive", fontsize=9)
fig.savefig(FIG/"latency.pdf")
fig.savefig(FIG/"latency.png", dpi=160)
plt.close(fig)

fig, ax = plt.subplots(figsize=(8, 3.1))
ax.set_xlim(0, 10); ax.set_ylim(0, 4); ax.axis("off")
def box(x, y, w, h, text, color="#edf3f5"):
    ax.add_patch(FancyBboxPatch((x,y), w,h, boxstyle="round,pad=0.08", linewidth=1,
                              edgecolor="#476273", facecolor=color))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=9)
def arrow(a, b, label=None):
    ax.annotate("", xy=b, xytext=a, arrowprops=dict(arrowstyle="->", color="#476273"))
    if label:
        ax.text((a[0]+b[0])/2, (a[1]+b[1])/2+.09, label, fontsize=8, ha="center")
box(.2, 2.8, 2.5, .8, "Human mandate owner\nversion · budget · expiry")
box(3.7, 2.8, 2.5, .8, "Independent broker\nlineage + shared ledger")
box(7.3, 2.8, 2.4, .8, "Mock effect boundary\ncommit or reject")
box(.2, .5, 2.5, .8, "Root → branches\n→ workers\nattenuated grants")
box(3.7, .5, 2.5, .8, "Direct concern intake\noptional delegate relay")
box(7.3, .5, 2.4, .8, "Review / appeal\nhold / amendment")
arrow((2.8,3.2),(3.6,3.2))
arrow((6.3,3.2),(7.2,3.2))
arrow((1.45,1.4),(4,2.7), "request")
arrow((2.8,.9),(3.6,.9))
arrow((6.3,.9),(7.2,.9))
arrow((8.5,1.4),(6,2.7), "decision")
ax.text(5, .02, "Audit records connect grant → request → decision → effect. Review is scripted in the simulator.",
        ha="center", fontsize=9)
fig.savefig(FIG/"architecture.pdf")
fig.savefig(FIG/"architecture.png", dpi=160)
plt.close(fig)

md = ["# Results: deterministic fixture coverage", "", "192 configurations; 48 per regime. Counts are not independent trials.", "",
      "| Regime | Unauthorized effects | Excess units | Unsafe effects | Valid work | False-hold blocks |",
      "|---|---:|---:|---:|---:|---:|"]
for r, name in zip(REGIMES, NAMES):
    t = totals[r]
    md.append(f'| {name} | {t["unauthorized_accepted"]} | {t["budget_excess"]} | '
              f'{t["unsafe_accepted"]} | {t["legitimate_completed"]}/{t["legitimate_opportunities"]} | '
              f'{t["false_hold_blocks"]} |')
md += ["", "## One-cell contrasts (delay 2, depth 3)", "",
       "| Scenario | Regime | Violations | Valid work | False blocks | Unsafe |", "|---|---|---:|---:|---:|---:|"]
for sc in json.loads((ROOT/"configs/study.json").read_text())["scenarios"]:
    for r in REGIMES:
        c = cell(sc["id"], r)
        md.append(f'| {sc["id"]} | {r} | {c["unauthorized_accepted"]} | '
                  f'{c["legitimate_completed"]}/{c["legitimate_opportunities"]} | '
                  f'{c["false_hold_blocks"]} | {c["unsafe_accepted"]} |')
md += ["", "Budget excess totals sum separate 100-unit organizations; they are not one organization's balance.",
       "Hazardous work can remain inside an initially valid mandate. Review receives a correct seeded report;",
       "its advantage is an added response capability, not evidence of better agent intentions.",
       "See coverage.json: bypass permits 10 hazardous effects, including 8 after authority removal."]
(OUT/"summary.md").write_text("\n".join(md)+"\n")

events = [json.loads(line) for line in (SOURCE/"traces.jsonl").read_text().splitlines()]
trace = [e for e in events if e["run_id"] == "revoked_pending-hierarchy-d2-h3"]
text = ["# Annotated incident trace", "", "Scenario: revoked_pending; hierarchy; depth 3; delay 2 (unused).",
        "This is an authored fixture, not a reconstruction of the historical intrusion.", "",
        "| Tick | Event | Interpretation |", "|---:|---|---|"]
for e in trace:
    if e["kind"] == "delegate":
        continue
    description = {"queued": "Request retained, with no expenditure or irrevocable effect yet.",
                   "revoke": "Parent authority withdrawn; descendants must be rechecked.",
                   "action": ("Effect committed; later revocation cannot undo it." if e.get("accepted")
                              else "Effect rejected at execution; no budget is consumed.")}[e["kind"]]
    text.append(f'| {e["tick"]} | {e["kind"]}: {e.get("reason", e.get("target", e.get("request_id", "")))} | {description} |')
text += ["", "The tick-0 10-unit effect remains. The queued tick-3 action and tick-4 sibling action are rejected.",
         "In the local-limits arm both later effects are accepted: only the parent's local flag was revoked."]
(ROOT/"docs/incident-trace.md").write_text("\n".join(text)+"\n")
print(json.dumps(totals, indent=2))
