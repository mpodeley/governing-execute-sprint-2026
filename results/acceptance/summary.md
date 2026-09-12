# Acceptance results — v0.2

| Probe | Reference | Local spend | Stale ancestry |
|---|---|---|---|
| C1 Grant attenuation | PASS | PASS | PASS |
| C2 Shared sibling pool | PASS | FAIL | PASS |
| C3 Current ancestor expiry | PASS | PASS | FAIL |
| C4 Revoked queue and sibling | PASS | PASS | FAIL |
| C5 Historical expenditure | PASS | PASS | PASS |
| C6 Direct intake and scoped hold | PASS | PASS | PASS |
| C7 Silence supplies no input | PASS | PASS | PASS |
| C8 Request authority binding | PASS | PASS | PASS |

## Report timing: hazardous effects out of ten opportunities

| Arrival | Response delay | Hold on receipt | Decision only |
|---|---|---|---|
| 1 | 0 | 0 | 0 |
| 1 | 2 | 0 | 2 |
| 1 | 6 | 0 | 6 |
| 1 | No response | 0 | 10 |
| 4 | 0 | 3 | 3 |
| 4 | 2 | 3 | 5 |
| 4 | 6 | 3 | 9 |
| 4 | No response | 3 | 10 |
| Absent | -- | 10 | 10 |

Each timing row pairs two deterministic traces; auxiliary effects are 10/10 throughout.
No accepted effect violates its active grant. Receipt timing and response are fixture inputs.
The pass/fail matrix is a contract diagnostic, not a security-rate estimate.
