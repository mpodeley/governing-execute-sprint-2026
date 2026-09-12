# Frozen study design v1.0

Author: Alejandro Garibotti. AI-assisted implementation, September 2026.

Question: what failures remain when organizational delegation is checked only at
individual identities, and what does a responsive review service add to a complete
hierarchical reference monitor? This is executable protocol validation, not an LLM
experiment. No historical counterfactual or statistical treatment effect is estimated.

## Design

Eight authored schedules × four regimes × delays 0/2/6 × depths 1/3 = 192 cells.
Every cell lasts twelve integer steps (0–11). Each chain has a root, zero or two
intermediate entities, and sibling workers a/b at the requested depth. All nodes
have a nominal 100-unit budget; in hierarchical arms this is a ceiling on subtree
spending, not an independently spendable allocation. Requests at the same tick
are serialized in file-defined order, worker a/work before b/aux. No randomness.

All arms see the same requests, costs and exogenous root changes. Actual states
diverge when controls reject requests. A missing input physically prevents work in
all arms. Only the review arm obtains input through the scripted service. This is
a structural information-access difference, not a benefit of representative framing.

Log: identities and physical prerequisites only, no authorization gate.
Local: own permission, expiry, revocation flag and own cumulative spending.
Hierarchy: complete lineage validity and subtree budgets; inherited expiry and
revocation; issuance checks scope, budget, expiry and maximum depth.
Review: hierarchy plus direct intake, scoped holds and a correct scripted reviewer.

The local arm intentionally lacks parent checks at issuance. Its accepted expanded
grants are a diagnosed omission, not a claim that all flat IAM implementations fail.
The expired fixture includes both ordinary expired credentials and a new credential
request with an impermissibly longer lease, allowing inherited expiry to be observed.

## Schedule and timing

Routine: four 10-unit actions, alternating siblings at ticks 1–4.
Split: four 40-unit actions at ticks 1–4; only the first two are task-legitimate
under the 100-unit envelope. No partial-fill or retry is attempted.
Overdelegation: tick-1 child request beyond maximum depth, then two action attempts.
Expiry: ancestor and initial children expire at tick 4; a tick-1 child request
claims expiry 12. Both ordinary and extended children act at ticks 3,5,7.
Revocation: one valid effect at tick 0; action queued at 1; ancestor revoked at 2;
queue executes at 3, sibling acts at 4. Pending actions are rechecked at execution.
Missing input / false alarm / suppressed minority: report at 1; ten work and ten
unrelated auxiliary opportunities at ticks 1–10. Work requires the missing input
only in that fixture. In the minority fixture, work is hazardous despite initial
authorization; hazard is an evaluator label, never a controller input to act().

Reports precede due responses, which precede effects. A zero-delay response occurs
before the same tick's effect. A report freezes work in the false-alarm and hazard
cases only in the review arm. The correct scheduled response provides missing
input, dismisses the false alarm, or removes work authority from every grant.
Aux remains authorized. Suppressed relay messages still reach the review service
through its direct path. No response exists in the three other arms.

## Metrics fixed before final execution

Primary: accepted effects violating the full mandate; root budget excess.
Secondary: invalid grants accepted, effects after revocation, hazardous effects,
legitimate opportunities/completions, blocked legitimate opportunities, false-hold
blocks, report resolutions and resolution latency. Legitimate task status is
authored separately from authorization. Completion requires both task legitimacy
and absence of a full-mandate violation. All blocked attempts stay in denominators.
Budget violation is assessed BEFORE commit, and accepted spend updates ALL ancestor
ledgers in every regime. A ledger is accounting, not enforcement.

Resolution latency is blank for unresolved/no-report cells, never zero. There is
one report per reporting cell. Each effect corresponds to one scheduled opportunity;
the study measures lost opportunities, not final completion of a retried task.

No confidence intervals, p-values, or model behavior claims: delays and depths
often duplicate outcomes. Pooled totals describe this fixture grid only. Present
scenario-level and delay-level contrasts so duplicated cells do not imply evidence.

## Acceptance and counterexamples

Under complete mediation, hierarchical regimes must accept no out-of-mandate effects,
overspend, or invalid grants. Review must preserve direct intake under relay
suppression and preserve auxiliary activity during work holds. False reports must
expose their availability cost. Baselines must fail the deliberately missing checks.
Passing these tests proves neither comprehensive security nor behavioral alignment.

A separately labeled coverage challenge lets work effects bypass the broker in
the minority scenario at delay 2/depth 3. It is excluded from 192-cell summaries.
An omniscient simulation ledger records bypass effects; a real broker might not see
them. Expected failure is a boundary test, not an exploit or observed deployment.

Design and source hashes are frozen locally after development tests, before the
final grid. Any subsequent change requires a retained superseding freeze and rerun.
