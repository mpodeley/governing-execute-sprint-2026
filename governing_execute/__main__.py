import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from .study import design_hashes, run

p = argparse.ArgumentParser(description="Offline organizational control simulator")
sub = p.add_subparsers(dest="command", required=True)
f = sub.add_parser("freeze")
f.add_argument("--out", required=True)
r = sub.add_parser("run")
r.add_argument("--out", required=True)
r.add_argument("--freeze", default="configs/freeze.json")
args = p.parse_args()
if args.command == "freeze":
    with Path(args.out).open("x") as out:
        json.dump(dict(created_utc=datetime.now(timezone.utc).isoformat(),
                       status="Local design freeze, not external preregistration",
                       files=design_hashes()), out, indent=2)
        out.write("\n")
else:
    print(f"Completed {len(run(args.out, args.freeze))} deterministic configurations.")
