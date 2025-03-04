import pathlib

from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
templates = Jinja2Templates(
    directory=[
        BASE_DIR / "templates",
    ]
)
