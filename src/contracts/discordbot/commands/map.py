import json
import random
from urllib.parse import quote
from urllib.request import urlopen

from nextcord.ext import commands

from contracts.common.logging import logger

REPO_OWNER: str = "Derpduck"
REPO_NAME: str = "GG2-Map-Archive"
BRANCH_NAME: str = "master"


class MalformedResponse(Exception):
    pass


class MapArchive:
    maps_by_name: dict[str, str] = {}

    def update(self) -> None:
        target_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/branches/{BRANCH_NAME}?recursive=1"
        response = urlopen(target_url)
        data = json.loads(response.read().decode("utf-8"))
        try:
            tree_url = data["commit"]["commit"]["tree"]["url"]
        except KeyError:
            raise MalformedResponse

        target_url = f"{tree_url}?recursive=1"
        response = urlopen(target_url)
        data = json.loads(response.read().decode("utf-8"))
        try:
            is_truncated = data["truncated"]
            tree_items = data["tree"]
        except KeyError:
            raise MalformedResponse

        if is_truncated:
            logger.warning(
                "Map Archive got truncated result from github; some maps may be missing"
            )
            # raise TruncatedTreeError
            pass

        for tree_item in tree_items:
            # TODO pydantic models would work nicely here
            if tree_item["type"] == "blob":
                path: str = tree_item["path"]
                if path.endswith(".png"):
                    map_name = path.split("/")[-1][:-4].lower()
                    self.maps_by_name[map_name] = path

        logger.info(f"Updated Map Archive: {len(self.maps_by_name)} items")

    def update_if_empty(self) -> None:
        if len(self.maps_by_name) == 0:
            self.update()

    def _map_url(self, path: str) -> str:
        return f"https://raw.githubusercontent.com/{REPO_OWNER}/{REPO_NAME}/{BRANCH_NAME}/{quote(path)}"

    def random_name(self) -> str:
        return random.choice(list(self.maps_by_name.keys()))

    def find(self, name: str) -> str:
        if name in self.maps_by_name:
            return self._map_url(self.maps_by_name[name])
        raise FileNotFoundError


_mapArchive = MapArchive()


@commands.command()
async def map(ctx: commands.Context, map_name: str | None):
    """
    Returns a gg2 map

    Fetches a map by name from Derpduck's map archive on github,
    or returns a random one.
    """
    logger.debug(map_name)

    try:
        _mapArchive.update_if_empty()
    except MalformedResponse:
        logger.error("Malformed response from github")
        await ctx.send("Error: Malformed response from github")
        raise

    logger.debug(f"Archive count: {len(_mapArchive.maps_by_name)}")

    if not map_name:
        map_name = _mapArchive.random_name()

    try:
        result_text = _mapArchive.find(map_name)
    except FileNotFoundError:
        # TODO find by similarity
        result_text = "Not Found"

    await ctx.send(result_text)
