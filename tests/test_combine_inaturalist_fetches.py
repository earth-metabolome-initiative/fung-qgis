from __future__ import annotations

import csv

from scripts.combine_inaturalist_fetches import merge_rows


def write_csv(path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "taxon_id",
                "scientific_name",
                "observations_in_region",
                "inat_observations_global",
                "query_taxon_name",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def test_merge_rows_deduplicates_by_scientific_name(tmp_path) -> None:
    first = tmp_path / "first.csv"
    second = tmp_path / "second.csv"
    write_csv(
        first,
        [
            {
                "taxon_id": "1",
                "scientific_name": "Agaricus campestris",
                "observations_in_region": "2",
                "inat_observations_global": "20",
                "query_taxon_name": "Basidiomycota",
            }
        ],
    )
    write_csv(
        second,
        [
            {
                "taxon_id": "1",
                "scientific_name": "Agaricus campestris",
                "observations_in_region": "5",
                "inat_observations_global": "12",
                "query_taxon_name": "Trees",
            }
        ],
    )

    _, rows = merge_rows([first, second])

    assert rows == [
        {
            "taxon_id": "1",
            "scientific_name": "Agaricus campestris",
            "observations_in_region": "5",
            "inat_observations_global": "20",
            "query_taxon_name": "Basidiomycota",
        }
    ]
