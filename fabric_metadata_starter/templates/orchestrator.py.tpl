# GENERATED from metadata — do not edit by hand.
# Cell 1 (tag: parameters)
run_date = "1900-01-01"

# Cell 2
from fabric_notebook_kit import resolve, parse_exit_value
p = resolve(globals(), required=["run_date"], sentinels={"run_date": "1900-01-01"})
run_date = p.run_date

BRONZE = [
$bronze_steps
]
SILVER = [
$silver_steps
]

def run_step(name, params):
    r = notebookutils.notebook.run(name, 3600, params)
    s = parse_exit_value(r if isinstance(r, str) else getattr(r, "exitValue", None))
    if s.get("status") != "ok":
        raise RuntimeError(f"{name} failed: {s}")
    print(name, "ok", {k: v for k, v in s.items() if k != "status"})

for name, params in BRONZE: run_step(name, params)
for name, params in SILVER: run_step(name, params)
