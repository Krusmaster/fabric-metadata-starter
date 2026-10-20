# GENERATED from metadata — do not edit by hand. Source: $system / $table
# Cell 1 (tag: parameters)
run_date = "1900-01-01"

# Cell 2
from fabric_notebook_kit import resolve, NotebookRun
from fabric_cdc_silver import CdcSpec, to_silver

p = resolve(globals(), required=["run_date"], sentinels={"run_date": "1900-01-01"})
with NotebookRun(run_id=f"$table_lc-{p.run_date}") as run:
    secret = notebookutils.credentials.getSecret(KEY_VAULT_URL, "$connection_ref")
    df = read_sql_server_cdc_export(secret, "$table", p.run_date)   # your landing-zone reader
    df.write.format("delta").mode("append").saveAsTable("bronze.$table_lc")
    run.finish("ok", rows=df.count())
