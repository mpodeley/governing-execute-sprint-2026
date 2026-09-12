# Annotated incident trace

Scenario: revoked_pending; hierarchy; depth 3; delay 2 (unused).
This is an authored fixture, not a reconstruction of the historical intrusion.

| Tick | Event | Interpretation |
|---:|---|---|
| 0 | action: ok | Effect committed; later revocation cannot undo it. |
| 1 | queued: delayed | Request retained, with no expenditure or irrevocable effect yet. |
| 2 | revoke: branch2 | Parent authority withdrawn; descendants must be rechecked. |
| 3 | action: revoked | Effect rejected at execution; no budget is consumed. |
| 4 | action: revoked | Effect rejected at execution; no budget is consumed. |

The tick-0 10-unit effect remains. The queued tick-3 action and tick-4 sibling action are rejected.
In the local-limits arm both later effects are accepted: only the parent's local flag was revoked.
