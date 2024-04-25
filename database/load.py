"""
Loads the extracted data into the PostgresSQL base
"""
import os
from pathlib import Path

import pandas as pd
from database.extract import ExtractData
from database.models import Table
from sqlalchemy import MetaData, create_engine


def data_to_list(entries: list[Table], fields: list[str]) -> list[dict]:
    rows = []

    for entry in map(vars, entries):
        row = []

        for f in fields:
            if isinstance(value := entry[f], Table):
                row.append(value.id)
            else:
                row.append(value)

        rows.append(row)

    return rows


def load_data(
    engine, entries: list[Table], file_path: Path, save_to_csv: bool
) -> pd.DataFrame:
    fields = vars(entries[0]).keys()
    fieldnames = [
        f"{f}_id" if isinstance(vars(entries[0])[f], Table) else f for f in fields
    ]

    df = pd.DataFrame(data_to_list(entries, fields), columns=fieldnames)

    # Saving to csv is used for testing only
    if save_to_csv:
        df.to_csv(file_path)
    else:
        df.to_sql(name=file_path.stem, con=engine)


def drop_table(engine, name: str) -> None:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_to_drop = metadata.tables.get(name)

    if table_to_drop is not None:
        table_to_drop.drop(engine)


def load(dir: Path, save_to_csv: bool = False) -> None:
    print("Starting population script...")
    data = ExtractData()
    engine = create_engine("postgresql://root:root@postgres:5432/database")

    if os.environ.get("RESET_DB", "false") == "true":
        print("Cleaning existing data...")
        drop_table(engine, "malware_families")
        drop_table(engine, "tag_types")
        drop_table(engine, "tags")
        drop_table(engine, "analysis")
        drop_table(engine, "analyzers")
        drop_table(engine, "samples")

    nb_rows = int(os.environ.get("NB_ROWS", 20))

    print(f"Starting generation ({nb_rows} rows)")

    print("Generating MalwareFamilies")
    malware_families = data.list_malware_families()
    load_data(engine, malware_families, dir / "malware_families.csv", save_to_csv)

    print("Generating TagTypes")
    tag_types = data.list_tag_types()
    load_data(engine, tag_types, dir / "tag_types.csv", save_to_csv)

    print("Generating Samples")
    samples = data.list_samples(nb_rows)
    load_data(engine, samples, dir / "samples.csv", save_to_csv)

    print("Generating Analysis")
    analysis = data.list_analysis(nb_rows)
    load_data(engine, analysis, dir / "analysis.csv", save_to_csv)

    print("Generating Analyzers")
    analyzers = data.list_analyzers(nb_rows)
    load_data(engine, analyzers, dir / "analyzers.csv", save_to_csv)

    print("Generating Tags")
    tags = data.list_tags(nb_rows)
    load_data(engine, tags, dir / "tags.csv", save_to_csv)

    print("Data generation ended successfully")
