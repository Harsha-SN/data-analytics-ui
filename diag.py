import sys
from importlib.metadata import entry_points, version

print("DIAG python:", sys.version, flush=True)

for pkg in ["shillelagh", "python-jsonpath", "yarl", "requests-cache", "apsw"]:
    try:
        print("DIAG version:", pkg, version(pkg), flush=True)
    except Exception as exc:
        print("DIAG version FAILED:", pkg, exc, flush=True)

for ep in entry_points(group="shillelagh.adapter"):
    try:
        ep.load()
        print("DIAG adapter OK:", ep.name, flush=True)
    except Exception as exc:
        print("DIAG adapter LOAD FAILED:", ep.name, repr(exc), flush=True)

from sqlalchemy import create_engine

URL = "https://analytics-api-82mg.onrender.com/api/product-performance/categories"
tests = [
    ("shillelagh://", {}),
    ("shillelagh://", {"connect_args": {"adapters": ["genericjsonapi"]}}),
    ("shillelagh+safe://", {}),
]
for uri, kwargs in tests:
    try:
        with create_engine(uri, **kwargs).connect() as conn:
            rows = conn.exec_driver_sql(f'SELECT * FROM "{URL}" LIMIT 2').fetchall()
        print("DIAG query OK:", uri, kwargs, rows, flush=True)
    except Exception as exc:
        print("DIAG query FAILED:", uri, kwargs, repr(exc), flush=True)
