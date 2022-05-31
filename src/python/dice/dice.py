import re
from random import randint
from dice.model import DiceRoll, DiceRollResult

from starlette.routing import Match

ROLL_REGEX = "^(?P<number>[0-9]+)?[dD](?P<sides>[0-9]+)?(?P<modifier>[+-][0-9]+)?$"


class DiceException(Exception):
    pass


def parse_dice_roll(dice_roll_string: str) -> DiceRoll:
    match = re.match(ROLL_REGEX, dice_roll_string)
    if not match:
        raise DiceException("Error while parsing dice roll")

    number = _group_or_default(match, "number", "1")
    sides = _group_or_default(match, "sides", "6")
    modifier = _group_or_default(match, "modifier", "0")

    return DiceRoll(number=int(number), sides=int(sides), modifier=int(modifier))


def roll_dice(roll: DiceRoll) -> DiceRollResult:
    dice_to_be_rolled = [roll.sides] * roll.number
    result = sum([randint(1, dice) for dice in dice_to_be_rolled]) + roll.modifier
    return DiceRollResult(result)


def _group_or_default(match: Match, group_name: str, default_value: str) -> str:
    group = match.group(group_name)
    return group if group else default_value
