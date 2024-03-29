"""
Loads the extracted data into the PostgresSQL base
"""
import os
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, MetaData

from database.extract import ExtractData
from database.models import Table


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


def data_to_postgres(engine, entries: list[Table], file_path: Path) -> None:
    fields = vars(entries[0]).keys()
    fieldnames = [
        f"{f}_id" if isinstance(vars(entries[0])[f], Table) else f for f in fields
    ]

    pd.DataFrame(data_to_list(entries, fields), columns=fieldnames).to_sql(
        name=file_path.stem, con=engine
    )


def drop_table(engine, name: str) -> None:
    metadata = MetaData()
    metadata.reflect(bind=engine)
    table_to_drop = metadata.tables.get(name)

    if table_to_drop is not None:
        table_to_drop.drop(engine)


def load(dir: Path) -> None:
    print('Starting population script...')
    data = ExtractData()
    engine = create_engine("postgresql://root:root@postgres:5432/database")

    if os.environ.get('RESET_DB', 'false') == 'true':
        print('Cleaning existing data...')
        drop_table(engine, 'malware_families')
        drop_table(engine, 'tag_types')
        drop_table(engine, 'tags')
        drop_table(engine, 'analysis')
        drop_table(engine, 'analyzers')
        drop_table(engine, 'samples')

    nb_rows = int(os.environ.get('NB_ROWS', 20))

    print(f'Starting generation ({nb_rows} rows)')

    print('Generating MalwareFamilies')
    data_to_postgres(engine, data.list_malware_families(), dir / "malware_families.csv")
    
    print('Generating TagTypes')
    data_to_postgres(engine, data.list_tag_types(), dir / "tag_types.csv")

    print('Generating Samples')
    data_to_postgres(engine, data.list_samples(nb_rows), dir / "samples.csv")

    print('Generating Analysis')
    data_to_postgres(engine, data.list_analysis(nb_rows), dir / "analysis.csv")

    print('Generating Analyzers')
    data_to_postgres(engine, data.list_analyzers(nb_rows), dir / "analyzers.csv")

    print('Generating Tags')
    data_to_postgres(engine, data.list_tags(nb_rows), dir / "tags.csv")

    print('Data generation ended successfully')