from num2words import num2words

from dice.model import DiceRoll, DiceRollResult


def roll_flavor_text(roll: DiceRoll) -> str:
    sides_english = _integer_to_english(roll.sides)
    num_english = _integer_to_english(roll.number)
    mod_english = _modifier_flavor_text(roll)

    if roll.number == 1:
        return f"You roll your lucky {sides_english}-sided die{mod_english}{'!' if roll.modifier == 0 else ''}"
    else:
        return f"You carefully select {num_english} of your best {sides_english}-sided dice{' and ' if roll.modifier == 0 else ', '}throw them ferociously on the table{'!' if roll.modifier == 0 else ''}{mod_english}"


def investigation_flavor_text(roll: DiceRoll) -> str:
    return (
        "You analyze the the mess before you."
        if roll.number > 1
        else "You investigate the die."
    ) + " The result is"


def result_flavor_text(result: DiceRollResult) -> str:
    return _integer_to_english(result)


def _modifier_flavor_text(roll: DiceRoll) -> str:
    if roll.modifier == 0:
        return ""

    if roll.modifier > 0:
        return f" and add a modifier of {_integer_to_english(roll.modifier)} to the result!"

    return f" and subtract {_integer_to_english(-roll.modifier)} from the result!"


def _integer_to_english(integer: int) -> str:
    return num2words(integer)
