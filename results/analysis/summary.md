# Results: deterministic fixture coverage

192 configurations; 48 per regime. Counts are not independent trials.

| Regime | Unauthorized effects | Excess units | Unsafe effects | Valid work | False-hold blocks |
|---|---:|---:|---:|---:|---:|
| Logging | 66 | 360 | 60 | 288/348 | 0 |
| Local limits | 54 | 360 | 60 | 288/348 | 0 |
| Hierarchy | 0 | 0 | 60 | 288/348 | 0 |
| Hierarchy + review | 0 | 0 | 0 | 316/348 | 16 |

## One-cell contrasts (delay 2, depth 3)

| Scenario | Regime | Violations | Valid work | False blocks | Unsafe |
|---|---|---:|---:|---:|---:|
| legitimate | log | 0 | 4/4 | 0 | 0 |
| legitimate | local | 0 | 4/4 | 0 | 0 |
| legitimate | hierarchy | 0 | 4/4 | 0 | 0 |
| legitimate | review | 0 | 4/4 | 0 | 0 |
| split_budget | log | 2 | 2/2 | 0 | 0 |
| split_budget | local | 2 | 2/2 | 0 | 0 |
| split_budget | hierarchy | 0 | 2/2 | 0 | 0 |
| split_budget | review | 0 | 2/2 | 0 | 0 |
| overdelegate | log | 2 | 0/0 | 0 | 0 |
| overdelegate | local | 2 | 0/0 | 0 | 0 |
| overdelegate | hierarchy | 0 | 0/0 | 0 | 0 |
| overdelegate | review | 0 | 0/0 | 0 | 0 |
| expired | log | 5 | 1/1 | 0 | 0 |
| expired | local | 3 | 1/1 | 0 | 0 |
| expired | hierarchy | 0 | 1/1 | 0 | 0 |
| expired | review | 0 | 1/1 | 0 | 0 |
| revoked_pending | log | 2 | 1/1 | 0 | 0 |
| revoked_pending | local | 2 | 1/1 | 0 | 0 |
| revoked_pending | hierarchy | 0 | 1/1 | 0 | 0 |
| revoked_pending | review | 0 | 1/1 | 0 | 0 |
| missing_input | log | 0 | 10/20 | 0 | 0 |
| missing_input | local | 0 | 10/20 | 0 | 0 |
| missing_input | hierarchy | 0 | 10/20 | 0 | 0 |
| missing_input | review | 0 | 18/20 | 0 | 0 |
| false_alarm | log | 0 | 20/20 | 0 | 0 |
| false_alarm | local | 0 | 20/20 | 0 | 0 |
| false_alarm | hierarchy | 0 | 20/20 | 0 | 0 |
| false_alarm | review | 0 | 18/20 | 2 | 0 |
| suppressed_minority | log | 0 | 10/10 | 0 | 10 |
| suppressed_minority | local | 0 | 10/10 | 0 | 10 |
| suppressed_minority | hierarchy | 0 | 10/10 | 0 | 10 |
| suppressed_minority | review | 0 | 10/10 | 0 | 0 |

Budget excess totals sum separate 100-unit organizations; they are not one organization's balance.
Hazardous work can remain inside an initially valid mandate. Review receives a correct seeded report;
its advantage is an added response capability, not evidence of better agent intentions.
See coverage.json: bypass permits 10 hazardous effects, including 8 after authority removal.
