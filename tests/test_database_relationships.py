from pathlib import Path

import pandas as pd
import pytest
from database.load import load


@pytest.fixture(scope="session")
def data(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("test_data")

    load(Path(tmp_path), save_to_csv=True)

    return {
        "analysis": pd.read_csv(tmp_path / "analysis.csv"),
        "analyzers": pd.read_csv(tmp_path / "analyzers.csv"),
        "malware_families": pd.read_csv(tmp_path / "malware_families.csv"),
        "samples": pd.read_csv(tmp_path / "samples.csv"),
        "tags": pd.read_csv(tmp_path / "tags.csv"),
        "tag_types": pd.read_csv(tmp_path / "tag_types.csv"),
    }


def assert_relationships(data: dict, target: str, relations: list):
    for relation in relations:
        assert (
            data[target][f"{relation}_id"].isin(data[f"{relation}s"]["id"]).all()
        ), f"Faulty relation between table '{target}' and '{relation}' (missing ids)"


def test_analysis_table_relationships(data: dict):
    assert_relationships(data, "analysis", ["sample", "analyzer"])


def test_tags_relationships(data: dict):
    assert_relationships(data, "tags", ["tag_type", "sample"])
