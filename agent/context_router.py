import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def _read_text(rel):
    return (ROOT / rel).read_text(encoding="utf-8")

def select_docs(prompt, manifest="context/manifest.json", max_docs=3):
    p = prompt.lower()
    manifest = json.loads(_read_text(manifest))
    scored = []
    for d in manifest["docs"]:
        hits = sum(1 for k in d["when"] if k in p)
        if hits:
            scored.append((hits, d["path"]))
    scored.sort(reverse=True)
    return [p for _, p in scored[:max_docs]]

def build_system_context(prompt):
    base = _read_text("context/base.md")
    docs = select_docs(prompt)
    extra = "\n\n".join([_read_text(d) for d in docs])
    return base + ("\n\n" + extra if extra else "")
