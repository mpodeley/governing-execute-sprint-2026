"""Regenerate evidence tables, compile and validate the report body."""
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LATEX = ROOT/"report/latex"
subprocess.run([sys.executable, str(ROOT/"scripts/verify_records.py")], check=True, cwd=ROOT)
analysis = subprocess.run([sys.executable, str(ROOT/"scripts/render_acceptance.py")],
                          check=True, cwd=ROOT, text=True, capture_output=True)
binary = os.environ.get("TECTONIC") or shutil.which("tectonic")
if not binary:
    candidate = Path.home()/"miniforge3/envs/tex/bin/tectonic"
    if candidate.exists():
        binary = str(candidate)
if not binary:
    raise SystemExit("Set TECTONIC to an installed binary, or put tectonic on PATH.")
compiled = subprocess.run([binary, "--keep-logs", "--keep-intermediates", "main.tex"],
                          check=True, cwd=LATEX, capture_output=True, text=True)
(ROOT/"report/compiler-output.txt").write_text(compiled.stdout+compiled.stderr)
log = (LATEX/"main.log").read_text(errors="replace")
for problem in ("Overfull", "undefined references", "Citation `", "Missing character"):
    if problem in log:
        raise RuntimeError(f"Inspect compilation log: {problem}")
reader = PdfReader(LATEX/"main.pdf")
texts = [p.extract_text() for p in reader.pages]
normalized = [re.sub(r"\s+", "", t) for t in texts]
narrative_pages = next(i for i,t in enumerate(normalized) if t.startswith("CodeandData"))
# Conservatively include the page containing the statements and start of references.
body_pages = next(i+1 for i,t in enumerate(texts) if "\nReferences\n" in t)
assert body_pages <= 8, body_pages
assert "AlejandroGaribotti" in normalized[0]
assert any("LimitationsandDual-UseConsiderations" in t for t in normalized)
assert any("LLMUsageStatement" in t for t in normalized)
assert "AcceptanceContractforDelegatingAgentBrokers" in normalized[0]
assert not any("RelationtoPacingtheFrontier" in t or "Authorsupplied" in t for t in normalized)
abstract = (LATEX/"abstract.tex").read_text()
macros = dict(re.findall(r"\\newcommand\{\\(\w+)\}\{(\d+)\}", (LATEX/"generated/counts.tex").read_text()))
for name, value in macros.items():
    abstract = abstract.replace("\\"+name+"{}", value)
words = len(abstract.split())
assert 150 <= words <= 250, words
(ROOT/"report/abstract.txt").write_text(abstract)
shutil.copy2(LATEX/"main.pdf", ROOT/"report/governing-execute.pdf")
subprocess.run(["pdftotext", "-layout", str(ROOT/"report/governing-execute.pdf"),
                str(ROOT/"report/paper.txt")], check=True)
validation = dict(body_pages=body_pages, narrative_pages=narrative_pages,
                  body_count_note="Includes the statements page where references begin",
                  total_pages=len(reader.pages), abstract_words=words,
                  author="Alejandro Garibotti", model_calls=0, contract_outcomes=24, timing_traces=18,
                  verified="Automated compilation, artifact replay and internal consistency checks",
                  source_freeze_sha256=hashlib.sha256((ROOT/"configs/acceptance-freeze.json").read_bytes()).hexdigest(),
                  pdf_sha256=hashlib.sha256((ROOT/"report/governing-execute.pdf").read_bytes()).hexdigest(),
                  compiler=subprocess.run([binary,"--version"],capture_output=True,text=True,check=True).stdout.strip(),
                  warnings=[line.strip() for line in compiled.stderr.splitlines() if "warning:" in line])
(ROOT/"report/build-validation.json").write_text(json.dumps(validation, indent=2)+"\n")
with zipfile.ZipFile(ROOT/"report/latex-source.zip", "w", zipfile.ZIP_DEFLATED) as z:
    for p in sorted(LATEX.rglob("*")):
        if p.is_file() and (p.suffix in (".tex", ".sty", ".bib", ".ttf", ".txt") or
                            (p.parent.name == "figures" and p.suffix == ".pdf")):
            z.write(p, p.relative_to(LATEX))
print(json.dumps(validation, indent=2))
