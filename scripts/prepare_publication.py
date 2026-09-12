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
shutil.copy2(ROOT/"report/latex/figures/architecture.png", assets/"architecture.png")
rows = list(csv.DictReader((ROOT/"results/final/metrics.csv").open()))
values = []
for delay in (0, 2, 6):
    selection = {r["scenario"]: r for r in rows if r["regime"] == "review"
                 and r["depth"] == "3" and r["delay"] == str(delay)}
    values.append(dict(delay=delay,
                       completed=int(selection["missing_input"]["legitimate_completed"]),
                       blocked=int(selection["false_alarm"]["false_hold_blocks"])))
(assets/"results.js").write_text("window.reviewResults = "+json.dumps(values)+";\n")
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
