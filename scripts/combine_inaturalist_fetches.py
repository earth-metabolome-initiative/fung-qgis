#!/usr/bin/env python3
"""Combine and deduplicate iNaturalist species-count CSV files."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


DEFAULT_OUTPUT = Path("data/inaturalist/switzerland_species_observations.csv")


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def merge_rows(paths: list[Path]) -> tuple[list[str], list[dict[str, str]]]:
    headers: list[str] = []
    seen_headers: set[str] = set()
    rows_by_name: dict[str, dict[str, str]] = {}

    for path in paths:
        file_headers, rows = read_csv(path)
        for header in file_headers:
            if header not in seen_headers:
                headers.append(header)
                seen_headers.add(header)
        for row in rows:
            name = (row.get("scientific_name") or "").strip()
            if not name:
                continue
            existing = rows_by_name.get(name)
            if existing is None:
                rows_by_name[name] = dict(row)
                continue
            for field in ("observations_in_region", "inat_observations_global"):
                existing_value = int(existing.get(field) or 0)
                new_value = int(row.get(field) or 0)
                existing[field] = str(max(existing_value, new_value))
            for field, value in row.items():
                if value and not existing.get(field):
                    existing[field] = value

    return headers, sorted(rows_by_name.values(), key=lambda row: row["scientific_name"].casefold())


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    headers, rows = merge_rows(args.inputs)
    write_csv(args.output, headers, rows)
    print(f"Wrote {len(rows)} deduplicated species rows to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
