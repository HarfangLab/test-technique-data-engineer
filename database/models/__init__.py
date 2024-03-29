from dataclasses import dataclass
from uuid import UUID


@dataclass(eq=True, frozen=True)
class Table:
    """A base class that defines a Table with a unique identifier"""

    id: UUID
