"""Run the reusable acceptance suite against a named local adapter factory."""
import argparse
import json
from pathlib import Path
from .probes import evaluate, factory_from_path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--adapter", default="acceptance_contract.broker:reference")
parser.add_argument("--out", type=Path)
args = parser.parse_args()
rows = evaluate(factory_from_path(args.adapter), args.adapter)
if args.out:
    with args.out.open("x") as stream:
        stream.write(json.dumps(rows, indent=2) + "\n")
for row in rows:
    print(f'{row["probe"]} {"PASS" if row["passed"] else "FAIL"} {row["title"]}')
raise SystemExit(0 if all(r["passed"] for r in rows) else 1)
