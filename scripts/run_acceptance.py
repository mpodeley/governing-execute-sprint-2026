"""Retain or replay contract probes and timing cases against a local source freeze."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from acceptance_contract.probes import evaluate, factory_from_path
from acceptance_contract.timing import run as timing_run


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_hashes():
    paths = sorted([*ROOT.glob("acceptance_contract/*.py"),
                    *ROOT.glob("acceptance_tests/*.py"),
                    ROOT/"governing_execute/model.py", ROOT/"governing_execute/study.py",
                    ROOT/"configs/acceptance.json", ROOT/"docs/acceptance-contract.md",
                    Path(__file__).resolve()])
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def run(out):
    freeze = json.loads((ROOT/"configs/acceptance-freeze.json").read_text())
    if freeze["files"] != source_hashes():
        raise RuntimeError("Acceptance source differs from its retained freeze")
    cfg = json.loads((ROOT/"configs/acceptance.json").read_text())
    out = Path(out)
    out.mkdir(parents=True, exist_ok=False)
    matrix = []
    for name, factory in cfg["adapters"].items():
        matrix.extend(evaluate(factory_from_path(factory), name))
    timing = timing_run(cfg["timing_cases"])
    write_json(out/"matrix.json", matrix)
    write_json(out/"timing.json", timing)
    write_json(out/"manifest.json", dict(design=freeze,
               artifacts={p.name: digest(p) for p in sorted(out.iterdir())}))
    return matrix, timing


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--freeze", action="store_true")
    args = parser.parse_args()
    if args.freeze:
        target = ROOT/"configs/acceptance-freeze.json"
        if target.exists():
            raise SystemExit("Preserve the old freeze before creating another")
        write_json(target, dict(version="0.2.0", procedure="Local source freeze after development tests; not preregistration", files=source_hashes()))
    elif args.out:
        matrix, timing = run(args.out)
        print(f"Retained {len(matrix)} contract outcomes and {len(timing)} timing traces")
    else:
        parser.error("Provide --freeze or --out")
