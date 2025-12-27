import argparse
import sys
from pathlib import Path

from .loader import load_personality
from .validator import validate_personality


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="mpf",
        description="Validate MPF (Modular Personality Format) personality files.",
    )
    parser.add_argument(
        "file",
        help="Path to an MPF JSON file to validate.",
    )
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"[mpf] Error: file not found: {path}", file=sys.stderr)
        return 1

    try:
        data = load_personality(str(path))
        validate_personality(data)
    except Exception as exc:
        print(f"[mpf] Validation failed: {exc}", file=sys.stderr)
        return 1

    print(f"[mpf] OK: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
