"""Render notebooks from metadata + templates. Golden-file testable: same metadata -> same output."""
from __future__ import annotations

from pathlib import Path
from string import Template

from .model import Metadata

TEMPLATES = Path(__file__).resolve().parent / "templates"


def _tpl(name: str) -> Template:
    return Template((TEMPLATES / name).read_text(encoding="utf-8"))


def render_bronze(md: Metadata) -> dict[str, str]:
    out = {}
    for o in md.active_objects():
        sysm = md.systems[o.system_id]
        out[f"nb_bronze_{o.name.lower()}.py"] = _tpl(f"bronze_{sysm.type}.py.tpl").substitute(
            table=o.name, table_lc=o.name.lower(), system=sysm.id, connection_ref=sysm.connection_ref,
            keys=repr(o.business_key), order_col=o.order_col, op_col=repr(o.op_col))
    return out


def render_silver(md: Metadata) -> dict[str, str]:
    out = {}
    for b in md.business_objects.values():
        items = ", ".join(f'"{t.lower()}"' for t in b.items)
        out[f"nb_silver_{b.id}.py"] = _tpl("silver_compose.py.tpl").substitute(
            object_id=b.id, object_name=b.name, header=b.header.lower(), items=items,
            join_key=repr(b.join_key), owner=b.owner)
    return out


def render_orchestrator(md: Metadata) -> str:
    steps = "\n".join(f'    ("nb_bronze_{o.name.lower()}", {{"run_date": run_date}}),' for o in md.active_objects())
    silver = "\n".join(f'    ("nb_silver_{b.id}", {{"run_date": run_date}}),' for b in md.business_objects.values())
    return _tpl("orchestrator.py.tpl").substitute(bronze_steps=steps, silver_steps=silver)


def render_all(md: Metadata) -> dict[str, str]:
    errs = md.validate()
    if errs:
        raise ValueError("metadata invalid:\n  " + "\n  ".join(errs))
    files = {**render_bronze(md), **render_silver(md), "nb_orchestrator.py": render_orchestrator(md)}
    return files
