# fabric-metadata-starter

**The problem.** The tenth source table gets the tenth hand-written notebook. Each one slightly
different, each one reviewed from scratch, each one carrying the same three bugs. "Metadata-driven"
is on every architecture slide, but most platforms have a metadata *catalog*, not metadata that
*generates* anything. The difference: a new source should be a new row, not a new notebook.

**What this does.** The smallest metadata model that makes Fabric pipelines generated instead of
written, and the generator that does it.

Three tables in `metadata/` as YAML (a fourth, `pipeline_run`, is written by the notebooks at runtime):

| Table | One row per | Drives |
| --- | --- | --- |
| `source_system` | source system | which ingestion template is used |
| `source_object` | source table | bronze load, CDC collapse |
| `business_object` | silver object | header + items composition, ownership |

```
fabric-metadata-starter validate metadata/
fabric-metadata-starter generate metadata/ --out generated/
```

```
wrote 4 notebooks to generated/
  nb_bronze_vbak.py  nb_bronze_vbap.py  nb_silver_sales_order.py  nb_orchestrator.py
```

Same metadata → same output, so `generated/` is golden-file testable and reviewable in a PR.
Import the notebooks into Fabric, or wire the generator into your deployment pipeline.

## Rules the validator enforces

- every source object has a business key
- a business object's join key is a prefix of its header table's key (VBAK→VBAP joins on VBELN,
  not on something VBAK does not have)
- every business object has a named owner — a person, not a team
- **no logic in metadata.** Column names, keys, flags: yes. SQL snippets in a cell: no. The day
  you store transformation logic as strings you have built a programming language without a debugger.

## What the generated notebooks use

[fabric-notebook-kit](https://github.com/Krusmaster/fabric-notebook-kit) for parameters, exit
and merge; [fabric-cdc-silver](https://github.com/Krusmaster/fabric-cdc-silver) for the CDC
collapse. The bronze templates have one placeholder — `read_datasphere_export()` — because every
landing zone looks different. Replace that line and the rest is yours.

## What to build later, not first

Lineage graph, catalog UI, quality-rule engine. They come once these three tables have done their
job for six months. Before that they are decoration.

## Install

```
pip install git+https://github.com/Krusmaster/fabric-metadata-starter
```

## Works on

| Platform | Status |
| --- | --- |
| Fabric | yes — generated notebooks target Fabric |
| Databricks | model + validator yes; notebook templates need a Databricks variant |
| Snowflake | model + validator yes; no templates |
| Local Python | yes — validate and generate run anywhere |

## License

MIT
