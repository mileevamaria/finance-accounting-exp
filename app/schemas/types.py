from decimal import Decimal
from typing import Annotated

from pydantic import Field

Money = Annotated[
    Decimal,
    Field(max_digits=15, decimal_places=2),
]
