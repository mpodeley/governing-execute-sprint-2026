# An Acceptance Contract for Delegating Agent Brokers

Alejandro Garibotti · Apart Research AI Incident Response Sprint · September 2026

[Paper](report/governing-execute.pdf) · [Project page](https://mpodeley.github.io/governing-execute-sprint-2026/) ·
[Release v0.2.0](https://github.com/mpodeley/governing-execute-sprint-2026/releases/tag/v0.2.0) ·
[Resumen en español](docs/resumen-es.md)

A reusable acceptance contract for a broker that delegates authority to agents.
Check that sibling grants share one budget, queued work loses revoked authority,
and historical expenditure survives revocation. Test the reporting path separately:
a permitted effect can still be harmful.

The contribution is a contract, reference adapter and diagnostic evidence package.
It builds on capability security and hierarchical quotas. Eight probes pass in the
reference. Removing shared accounting fails C2; removing current ancestor liveness
checks fails C3 and C4. These are isolated ablations, not production-system baselines.
Eighteen timing traces include early, late, absent and unanswered reports.

## Read the contract

- [Acceptance obligations and adapter API](docs/acceptance-contract.md)
- [Pass/fail matrix and complete timing table](results/acceptance/summary.md)
- [Five-event revocation trace and incident mapping](docs/incident-trace.md)
- [Primary sources and attribution](docs/source-audit.md)

The four integration records link root mandate, grant, request/decision and outcome.
A production adapter must obtain independently observed effects and ledger values;
the supplied adapter uses a trusted in-process reference model. Full mediation,
authentication, concurrency and crash recovery remain integration requirements.

## Reproduce offline

With Python 3.10+ and no extra packages:

```bash
python3 scripts/reproduce.py
```

Runs 16 unittest methods, verifies source/artifact hashes, recounts retained records,
and checks byte-for-byte replay of both the current suite and the archived v0.1 grid.
No model calls, keys, network access or external effects are involved.

Run only the acceptance suite:

```bash
python3 -m acceptance_contract
```

Run the same probes against your own trusted adapter in an isolated test environment:

```bash
python3 -m acceptance_contract --adapter your_module:factory --out new-results.json
```

The output path must not exist. Exit 0 means all probes pass; exit 1 reports a failure.
The interface is specified in [the contract](docs/acceptance-contract.md).
To retain a fresh complete reference/ablation/timing run:

```bash
python3 scripts/run_acceptance.py --out /tmp/broker-new-run
```

## Build the paper and site assets

PDF compilation needs pypdf, Poppler and Tectonic:

```bash
python3 scripts/build_paper.py
python3 scripts/prepare_publication.py
```

Set `TECTONIC=/path/to/tectonic` if needed. A first TeX build may download packages;
data reproduction is fully offline. The standalone LaTeX ZIP contains tables and
licensed fonts. Compile it with Tectonic, or XeLaTeX/BibTeX/XeLaTeX twice. PDF bytes
can depend on the TeX environment; exact replay guarantees apply to data artifacts.

## Version history and files

Version 0.2 reorients the earlier *Governing Execute* draft around its acceptance
contract. It removes aggregate fixture totals from the abstract, adds isolated
ablations and late/absent reporting cases, and positions the mechanisms against
capabilities, SPKI/SDSI, Macaroons, Biscuit, cgroups v2 and ResourceQuota.
The original [v0.1.0 release](https://github.com/mpodeley/governing-execute-sprint-2026/releases/tag/v0.1.0)
remains available. Project URL and PDF filename remain stable.

| Location | Contents |
|---|---|
| `acceptance_contract/` | Reference adapter, isolated ablations, reusable probes and timing fixtures |
| `acceptance_tests/` | Regression and mutation checks for the current suite |
| `configs/acceptance*.json` | Current cases and local source freeze |
| `results/acceptance/` | Contract outcomes, timing traces, hashes and summary |
| `governing_execute/`, `tests/`, `configs/study.json`, `configs/freeze.json` | Unchanged v0.1 model, tests and design freeze |
| `results/final/`, `results/analysis/`, `docs/design.md` | Archived grid records, diagnostic totals and original design |
| `report/` | Current PDF, editable sources and build checks |
| `docs/` | Current site, contract, source audit and Spanish summary |

Source freezes are local integrity records created after development tests, not
external preregistration. Preserve old freezes/results when revising the design.

*Agent Delegate*, by Matías Podeley and Agustín Brusco, is cited for the separation
of intake, response and execution authority; its experiments are not reused here.
The paper discloses LLM assistance and includes the required limitations and dual-use
appendix. This public artifact is prepared for the sprint; publication is not a
claim of submission, acceptance or organizer endorsement. Original code and
project documentation are MIT licensed; included fonts retain their OFL license.
