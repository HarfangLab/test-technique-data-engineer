from dataclasses import dataclass

from database.models import Table
from database.models.analyzer import Analyzer
from database.models.sample import Sample
from pendulum import Date


@dataclass(eq=True, frozen=True)
class Analysis(Table):
    sample: Sample
    analyzer: Analyzer
    analysis_date: Date

    is_malware: bool | None = None
