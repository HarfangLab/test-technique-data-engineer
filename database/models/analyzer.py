from dataclasses import dataclass

from database.models import Table
from pendulum import Date


@dataclass(eq=True, frozen=True)
class Analyzer(Table):
    name: str
    analyzer_date: Date
