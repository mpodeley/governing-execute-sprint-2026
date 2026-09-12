"""One-command offline verification and exact replay into a fresh temporary directory."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from governing_execute.study import run
from verify_records import verify

subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
               cwd=ROOT, check=True)
verify()
expected = ROOT/"results/final"
manifest = json.loads((expected/"manifest.json").read_text())
for name, digest in manifest["artifacts"].items():
    assert hashlib.sha256((expected/name).read_bytes()).hexdigest() == digest, name
with tempfile.TemporaryDirectory(prefix="governing-execute-") as tmp:
    new = Path(tmp)/"replay"
    run(new, ROOT/"configs/freeze.json")
    for name in ("metrics.csv", "traces.jsonl", "coverage.json", "manifest.json"):
        assert (expected/name).read_bytes() == (new/name).read_bytes(), name
print("PASS: tests, artifact hashes, and exact replay of all 192 configurations + coverage challenge.")
