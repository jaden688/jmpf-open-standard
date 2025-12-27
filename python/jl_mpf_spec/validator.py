import json
import jsonschema
from pathlib import Path
from .schema_version import SCHEMA_VERSION
from .types import JsonDict


def _load_schema() -> JsonDict:
    """
    Load the MPF + JL extensions schema from the installed package data.
    This works both when running from the repo and from an installed wheel.
    """
    here = Path(__file__).resolve().parent
    schema_path = here / "schema" / "mpf-jl-extensions-v1.json"

    if not schema_path.exists():
        raise FileNotFoundError(f"Schema file not found at: {schema_path}")

    return json.loads(schema_path.read_text(encoding="utf-8"))


def validate_personality(data: JsonDict) -> None:
    """
    Validate a personality dictionary against the MPF schema.

    - Checks schema_version matches the expected SCHEMA_VERSION.
    - Validates the structure/content via jsonschema.
    """
    schema = _load_schema()

    if data.get("schema_version") != SCHEMA_VERSION:
        raise ValueError(
            f"Unexpected schema_version: {data.get('schema_version')!r} "
            f"(expected {SCHEMA_VERSION!r})"
        )

    jsonschema.validate(data, schema)
