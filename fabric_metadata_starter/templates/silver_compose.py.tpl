# GENERATED from metadata — do not edit by hand. Business object: $object_name (owner: $owner)
# Cell 1 (tag: parameters)
run_date = "1900-01-01"

# Cell 2
from fabric_notebook_kit import resolve, NotebookRun, merge_by_key
from fabric_cdc_silver import CdcSpec, to_silver

p = resolve(globals(), required=["run_date"], sentinels={"run_date": "1900-01-01"})
with NotebookRun(run_id=f"$object_id-{p.run_date}") as run:
    header = to_silver(spark.table("bronze.$header"), CdcSpec.datasphere($join_key))
    df = header
    for item in [$items]:
        df = df.join(to_silver(spark.table(f"bronze.{item}"), CdcSpec.datasphere($join_key)), $join_key, "left")
    metrics = merge_by_key(spark, df, "silver.$object_id", keys=$join_key, run_id=run.payload["run_id"])
    run.finish("ok", **metrics)
