import argparse, sys
from pathlib import Path
from .model import load_metadata
from .generate import render_all

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="fabric-metadata-starter")
    sub = ap.add_subparsers(dest="cmd", required=True)
    v = sub.add_parser("validate"); v.add_argument("metadata")
    g = sub.add_parser("generate"); g.add_argument("metadata"); g.add_argument("--out", default="generated")
    a = ap.parse_args(argv)
    md = load_metadata(a.metadata)
    if a.cmd == "validate":
        errs = md.validate()
        print("\n".join(errs) if errs else "ok"); return 1 if errs else 0
    files = render_all(md)
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    for name, text in files.items():
        (out / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(files)} notebooks to {out}"); return 0

if __name__ == "__main__":
    sys.exit(main())
