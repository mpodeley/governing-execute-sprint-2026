# Acceptance trace and incident mapping

The executable C4 probe submits the following events to an isolated broker.

| Tick | Event | Reference | Stale ancestry ablation |
|---:|---|---|---|
| 0 | Worker a commits 10 | Accepted; root spent 10 | Accepted; root spent 10 |
| 1 | Worker a queues 10 | Pending; root spent 10 | Pending; root spent 10 |
| 2 | Parent revoked | Both workers depend on inactive parent | Parent status changes |
| 3 | Commit queued action | Rejected; root spent 10 | Accepted; root spent 20 |
| 4 | Sibling b requests 10 | Rejected; root spent 10 | Accepted; root spent 30 |

C5 separately checks that revoking a parent does not erase historical expenditure.
The retained observations and complete events are in `results/acceptance/matrix.json`.

| Incident observation | Acceptance question | Status |
|---|---|---|
| METR: unsanctioned message board | Are communication and other effect channels mediated? | Integration precondition, not a Boolean challenge result |
| METR: out-of-scope collective workstreams | Is each request tied to the current mandate? | C1 attenuation and C8 request binding |
| Hugging Face: compromised credentials, followed by revocation/rotation | Does withdrawal reach queued and dependent authority? | C3–C5 response extensions; no claim that stolen credentials were expired |
| METR: tool-call spoofing | Can an external witness reconcile actual effects? | Outcome-record requirement; model events are not independent witnesses |
| No specific incident analogue | Are shared expenditure and direct review preserved? | C2 and C6–C7 engineering extensions |

Sources: [METR investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/)
and [Hugging Face disclosure](https://huggingface.co/blog/security-incident-july-2026).
These mappings derive acceptance questions; the five events are not a historical reconstruction.
