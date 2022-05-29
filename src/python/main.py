from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import PlainTextResponse, Response
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="src/template")


async def ping(request: Request) -> Response:
    return PlainTextResponse("pong")


routes = [
    Mount("/static", StaticFiles(directory="src/static"), name="Static content"),
    Route("/ping", ping, methods=["GET"], name="ping endpoint"),
]


application = Starlette(debug=True, routes=routes)
