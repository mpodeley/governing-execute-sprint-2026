# Sources, attribution and submission fit — v0.2

Checked September 12, 2026. This is a targeted claim audit, not an exhaustive
literature review. No full copyrighted articles or private conversation transcripts
are redistributed. Source citations in the paper distinguish prior mechanisms,
incident observations and engineering extensions.

| Source | Claim used | Verification and boundary |
|---|---|---|
| [METR investigation](https://metr.org/blog/2026-08-26-openai-hugging-face-incident-investigation/) | Unsanctioned coordination, out-of-scope workstreams and tool-call spoofing | Primary investigation retrieved; no historical prevention or grievance-causation estimate |
| [Hugging Face disclosure](https://huggingface.co/blog/security-incident-july-2026) | Compromised information/credentials and revocation/rotation in response | Primary disclosure, “What happened” and “What we did”; compromise is not expiry |
| [Miller, Robust Composition (2006)](https://erights.org/talks/thesis/markm-thesis.pdf) | Object capabilities and constrained composition | Author's thesis abstract and indexed primary PDF; no new capability mechanism claimed |
| [Hardy, The Confused Deputy (1988)](https://doi.org/10.1145/54289.871709) | Request authority must not be silently replaced by a deputy's privileges | Original hosting unavailable to the reader; concept cross-checked in the primary capability analysis [Capability Myths Demolished](https://papers.agoric.com/assets/pdf/papers/capability-myths-demolished.pdf), which cites Hardy. C8 is an API binding probe, not a prompt-injection evaluation |
| [SPKI Certificate Theory, RFC 2693](https://www.rfc-editor.org/rfc/rfc2693.html) | Naming, authorization, validity and delegation chains; SDSI relation | Primary RFC retrieved; Experimental, not an Internet Standard |
| [Macaroons (2014)](https://research.google/pubs/macaroons-cookies-with-contextual-caveats-for-decentralized-authorization-in-the-cloud/) | Attenuation with contextual caveats | Primary publication page; no cryptography implemented |
| [Biscuit specifications](https://doc.biscuitsec.org/reference/specifications) | Offline attenuation with added checks and authorizer context | Primary specification retrieved; stateful authorizers remain possible |
| [cgroups v2](https://cdn.kernel.org/doc/html/latest/admin-guide/cgroup-v2.html) | Hierarchical enforcement and overcommitted child limits | Primary kernel documentation, “Limits”; the paper models cumulative spending, not Linux resource-controller details |
| [Kubernetes Resource Quotas](https://kubernetes.io/docs/concepts/policy/resource-quotas/) | Aggregate consumption per namespace | Primary documentation; no native recursive cross-namespace quota claimed |
| [AgentCgroup v3](https://arxiv.org/abs/2602.09345v3) | Hierarchical OS controls aligned with agent tool-call boundaries | Primary abstract; its performance measurements are not imported |
| [Agent Delegate](https://mpodeley.github.io/agent-delegate-sprint-2026/) | Separation of intake, response and execution authority | Matías Podeley and Agustín Brusco retain authorship; local manuscript consulted, experiments not reused |
| [Apart Research sprint](https://apartresearch.com/sprints/ai-incident-response-sprint-2026-09-11-to-2026-09-13) | Submission requirements and limitations/dual-use appendix | Primary requirements and supplied template; publication does not imply submission |

## Revision scope

The earlier Amodei discussion is removed from the current manuscript. It contributed
policy context rather than acceptance evidence. Version 0.1 remains in its public
release and repository tag, including its original bibliography and artifacts.

The current contribution is the reusable acceptance package: four linked records,
fixed probes, a broker adapter, isolated ablations and reporting-boundary traces.
Attenuation, shared quotas and revocation are established mechanisms. The paper
uses ordinary authorization terminology and makes no priority claim for “execute.”

The source freeze for the new suite is separate from the unchanged historical grid.
Both are local integrity records produced after development tests, not external
preregistration. The manuscript's LLM statement describes assistance without
claiming independent human review. Local provenance hashes remain in
`data/local-provenance.json`; underlying private notes are not redistributed.

## Submission fit

The current build checks a 150–250-word abstract, the author name, required statements,
page count and compilation integrity. `report/build-validation.json` records actual
counts. The layout adapts the official template's Letter geometry, one-inch margins
and 11-point text, with a single limitations/dual-use appendix. It is not an official
Apart LaTeX class. No video, sprint form submission or acceptance is claimed.
