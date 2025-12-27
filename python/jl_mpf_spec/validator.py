import json, jsonschema
from pathlib import Path
from .schema_version import SCHEMA_VERSION
from .types import JsonDict

def validate_personality(data: JsonDict):
    schema = json.loads(Path(__file__).resolve().parents[2].joinpath(
        "schema/mpf-jl-extensions-v1.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError("Unexpected schema_version")
    jsonschema.validate(data, schema)
