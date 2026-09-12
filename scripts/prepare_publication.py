"""Refresh static site assets and an archive suitable for a public release."""
import csv
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
assets = ROOT/"docs/assets"
assets.mkdir(exist_ok=True)
shutil.copy2(ROOT/"report/governing-execute.pdf", assets/"governing-execute.pdf")
matrix = json.loads((ROOT/"results/acceptance/matrix.json").read_text())
timing = json.loads((ROOT/"results/acceptance/timing.json").read_text())
values = dict(matrix=[r for r in matrix if r["probe"] == "C4"],
              timing=[{k:v for k,v in r.items() if k != "events"} for r in timing])
(assets/"results.js").write_text("window.contractResults = "+json.dumps(values)+";\n")
excluded = {".aux", ".blg", ".log", ".out", ".pyc"}
files = [p for p in sorted(ROOT.rglob("*")) if p.is_file()
         and "__pycache__" not in p.parts and ".git" not in p.relative_to(ROOT).parts
         and p.suffix not in excluded and p != ROOT/"report/latex/main.pdf"
         and p != ROOT/"data/release-integrity.json"]
manifest = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
(ROOT/"data/release-integrity.json").write_text(json.dumps(manifest, indent=2)+"\n")
files.append(ROOT/"data/release-integrity.json")
out = ROOT.parent/"governing-execute-artifact.zip"
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for p in files:
        z.write(p, Path(ROOT.name)/p.relative_to(ROOT))
print(f"Prepared {len(files)} files: {out}")
