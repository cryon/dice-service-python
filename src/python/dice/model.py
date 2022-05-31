from typing import NewType
from pydantic import BaseModel


class DiceRoll(BaseModel):
    number: int
    sides: int
    modifier: int

    def __str__(self):
        return (
            f"{self.number}d{self.sides}"
            f"{'+' if self.modifier > 0 else ''}"
            f"{self.modifier if self.modifier != 0 else ''}"
        )


DiceRollResult = NewType("DiceRollResult", int)
