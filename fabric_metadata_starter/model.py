"""Four tables. Everything else is an addition. Metadata is code: it lives in the repo as YAML."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

TYPES = {"datasphere", "fabric_mirroring", "sql_server_cdc", "api"}


@dataclass
class SourceSystem:
    id: str
    type: str
    connection_ref: str
    cdc_style: str = "log"


@dataclass
class SourceObject:
    system_id: str
    name: str
    business_key: list[str]
    order_col: str
    op_col: str | None = None
    active: bool = True


@dataclass
class BusinessObject:
    id: str
    name: str
    header: str
    items: list[str] = field(default_factory=list)
    join_key: list[str] = field(default_factory=list)
    owner: str = ""


@dataclass
class Metadata:
    systems: dict[str, SourceSystem]
    objects: dict[str, SourceObject]
    business_objects: dict[str, BusinessObject]

    def validate(self) -> list[str]:
        errs = []
        for s in self.systems.values():
            if s.type not in TYPES:
                errs.append(f"source_system {s.id}: unknown type {s.type}")
        for o in self.objects.values():
            if o.system_id not in self.systems:
                errs.append(f"source_object {o.name}: unknown system {o.system_id}")
            if not o.business_key:
                errs.append(f"source_object {o.name}: business_key is empty")
        for b in self.business_objects.values():
            for t in [b.header, *b.items]:
                if t not in self.objects:
                    errs.append(f"business_object {b.id}: table {t} not in source_object")
            hk = self.objects.get(b.header)
            if hk and b.join_key and hk.business_key[: len(b.join_key)] != b.join_key:
                errs.append(f"business_object {b.id}: join_key {b.join_key} is not a prefix of {b.header}'s key {hk.business_key}")
            if not b.owner:
                errs.append(f"business_object {b.id}: owner is required")
        return errs

    def active_objects(self) -> list[SourceObject]:
        return [o for o in self.objects.values() if o.active]


def _read(path: Path, name: str) -> list[dict]:
    p = path / f"{name}.yaml"
    return yaml.safe_load(p.read_text(encoding="utf-8")) or [] if p.exists() else []


def load_metadata(path: str | Path) -> Metadata:
    path = Path(path)
    systems = {r["id"]: SourceSystem(**r) for r in _read(path, "source_system")}
    objects = {r["name"]: SourceObject(**r) for r in _read(path, "source_object")}
    bos = {r["id"]: BusinessObject(**r) for r in _read(path, "business_object")}
    return Metadata(systems, objects, bos)
