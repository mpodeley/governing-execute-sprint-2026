# Governing Execute

**Institutional Controls for Organizations of AI Agents**  
Alejandro Garibotti · Apart Research AI Incident Response Sprint · September 2026

[Read the paper](report/governing-execute.pdf) · [Resumen en español](docs/resumen-es.md) ·
[Operational protocol](docs/protocol.md) · [Results](results/analysis/summary.md) ·
[Annotated incident](docs/incident-trace.md)

An offline protocol and reference simulator for shared budgets, attenuated delegation,
transitive revocation and direct review access. The new work complements *Agent
Delegate* by Matías Podeley and Agustín Brusco, which is cited rather than reattributed.

**Status:** public v0.1 working draft and executable artifact. Author review and
sprint submission remain pending. No affiliation is asserted.

[Public project page](https://mpodeley.github.io/governing-execute-sprint-2026/) ·
[Download release](https://github.com/mpodeley/governing-execute-sprint-2026/releases/tag/v0.1.0)

## Finding and its boundary

In 192 authored deterministic configurations, logging admits 66 out-of-mandate
effects and individual limits admit 54; hierarchy admits zero under full mediation.
Review increases valid work from 288 to 316 of 348 opportunities, but causes 16
false-hold blocks. A separate broker-bypass challenge admits 10 hazardous effects,
including eight after the relevant authority is withdrawn.

These counts describe the fixtures, not independent trials, model behavior or
historical prevention. Complete enforcement is an assumption; correct review and
timely seeded reports are assumptions. Permissions can themselves authorize harm.

## Reproduce in one command

From this folder, with Python 3.10+:

```bash
python3 scripts/reproduce.py
```

The core uses only the standard library. This runs twelve tests, verifies retained
artifact hashes, recomputes metric counts from traces, and replays every configuration
into a temporary directory with byte-for-byte comparison. No installation, API keys,
model server, internet access or real-world actions are involved.

To retain a fresh run (the output path must not already exist):

```bash
python3 -m governing_execute run --out /tmp/execute-new-run
```

Regenerate figures and the PDF with Matplotlib, pypdf, Poppler and Tectonic installed:

```bash
python3 scripts/build_paper.py
```

Set `TECTONIC=/path/to/tectonic` if it is not on PATH. A first Tectonic build may need
to download TeX packages; experiment reproduction remains fully offline. The included
LaTeX ZIP already contains vector figures, counts and licensed fonts and can compile
without Python using Tectonic or XeLaTeX, BibTeX, XeLaTeX twice.

## What is included

| Location | Contents |
|---|---|
| `governing_execute/` | Simulation API, scenarios, scoring and CLI |
| `configs/` | Scenario grid and local pre-final-run source/design freeze |
| `tests/` | Budget, inheritance, queue, expiry, review and bypass tests |
| `results/final/` | 192-cell CSV, JSONL traces, hashes and separate coverage challenge |
| `results/analysis/` | Recomputed summary and totals |
| `docs/` | Protocol, frozen design, Spanish summary, trace and source audit |
| `report/` | PDF, editable LaTeX, bibliography, source ZIP and build checks |
| `data/` | Local-source provenance hashes |

The core API uses trusted Python identities and logical clocks. It is not a production
credential service or OS security boundary. Read [the design](docs/design.md) for
ordering and denominators and [the source audit](docs/source-audit.md) for scope.

Source edits invalidate the design freeze. Preserve prior freezes and results when
making a new design; use `python3 -m governing_execute freeze --out NEW.json`, then
run with `--freeze NEW.json --out NEW_DIRECTORY`. This local procedure is not
external preregistration.

## Requirements and attribution

Core: Python >=3.10, standard library. Figures: Matplotlib (tested 3.11.0). PDF checks:
pypdf and Poppler. Compilation: Tectonic or a compatible XeLaTeX installation.
No claims of cross-version PDF byte reproducibility are made; exact comparison applies
to the deterministic data artifacts.

The manuscript includes assistance disclosure and the required limitations/dual-use
appendix. Old Standard font files retain their included SIL Open Font License.
The local LaTeX layout adapts the supplied Apart template's roles and dimensions;
it is not an official Apart class. All external publications retain their own rights.
