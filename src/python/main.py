import random


from pydantic import BaseModel
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from dice.model import DiceRoll, DiceRollResult
from dice.dice import parse_dice_roll, roll_dice
from dice.flavor import investigation_flavor_text, result_flavor_text, roll_flavor_text

templates = Jinja2Templates(directory="src/template")


class DiceRollResponse(BaseModel):
    roll: DiceRoll
    result: DiceRollResult
    roll_flavor: str
    investigation_flavor: str
    result_flavor: str


async def handle_dice_roll(request: Request) -> Response:
    roll_string = request.path_params["dice_roll"]
    roll = parse_dice_roll(roll_string)
    result = roll_dice(roll)

    response = DiceRollResponse(
        roll=roll,
        result=result,
        roll_flavor=roll_flavor_text(roll),
        investigation_flavor=investigation_flavor_text(roll),
        result_flavor=result_flavor_text(result),
    )

    accept_header = request.headers["accept"]

    if accept_header.startswith("text/html"):
        return templates.TemplateResponse(
            "roll.html", {"res": response, "request": request}
        )

    if accept_header.startswith("application/json"):
        return JSONResponse(response.dict())

    response_string = f"{response.roll_flavor} {response.investigation_flavor} {response.result_flavor}!"
    return PlainTextResponse(response_string)


routes = [
    Mount("/static", StaticFiles(directory="src/static"), name="Static content"),
    Route("/{dice_roll:str}", handle_dice_roll),
]

random.seed()
application = Starlette(debug=True, routes=routes)
