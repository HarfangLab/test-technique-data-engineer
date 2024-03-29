from dataclasses import dataclass

from database.models import Table
from database.models.sample import Sample


@dataclass(eq=True, frozen=True)
class TagType(Table):
    name: str


@dataclass(eq=True, frozen=True)
class Tag(Table):
    value: str
    tag_type: TagType
    sample: Sample
