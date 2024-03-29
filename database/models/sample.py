from dataclasses import dataclass

from database.models import Table


@dataclass(eq=True, frozen=True)
class Sample(Table):
    hash: str
    filename: str
    mime: str
    magic: str
