import aiohttp
from fastapi import Request

from contracts.common.logging import logger
from contracts.common.settings import settings

DISCORD_API_URL = "https://discord.com/api/v10"
DISCORD_OAUTH_URL = f"{DISCORD_API_URL}/oauth2"
DISCORD_TOKEN_URL = f"{DISCORD_OAUTH_URL}/token"
DISCORD_TOKEN_REVOKE_URL = f"{DISCORD_TOKEN_URL}/revoke"
DISCORD_OAUTH_AUTHENTICATION_URL = f"{DISCORD_OAUTH_URL}/authorize"


class DiscordOAuthClient:
    client_session: aiohttp.ClientSession

    def __init__(self):
        self.client_session = aiohttp.ClientSession()

    async def request(self, route: str, bearer_token: str):
        headers = {"Authorization": f"Bearer {bearer_token}"}
        async with self.client_session.get(
            f"{DISCORD_API_URL}{route}", headers=headers
        ) as resp:
            resp.raise_for_status()
            data = await resp.json()

        return data

    async def username(self, access_token: str) -> str:
        response_data = await self.request("/users/@me", access_token)
        return response_data["username"]

    async def get_access_token(self, code: str) -> str:
        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": settings.discord_oauth_redirect_uri,
        }

        async with self.client_session.post(
            DISCORD_TOKEN_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=aiohttp.BasicAuth(
                login=settings.discord_oauth_client_id,
                password=settings.discord_oauth_client_secret,
            ),
        ) as resp:
            resp.raise_for_status()
            response_data = await resp.json()

        return response_data["access_token"]

    async def revoke_access_token(self, access_token: str):
        payload = {"token": access_token, "token_type_hint": "access_token"}

        async with self.client_session.post(
            DISCORD_TOKEN_REVOKE_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            auth=aiohttp.BasicAuth(
                login=settings.discord_oauth_client_id,
                password=settings.discord_oauth_client_secret,
            ),
        ) as resp:
            resp.raise_for_status()


def get_oauth_login_url(state: str | None = None):
    client_id = settings.discord_oauth_client_id
    redirect_uri = settings.discord_oauth_redirect_uri
    scopes = "identify"
    state = f"&state={state}" if state else ""
    return f"{DISCORD_OAUTH_AUTHENTICATION_URL}?client_id={client_id}&redirect_uri={redirect_uri}&scope={scopes}&response_type=code{state}"


async def get_discord_username(oauth_code: str) -> str | None:
    try:
        discord_client = DiscordOAuthClient()
        access_token = await discord_client.get_access_token(code=oauth_code)
        discord_username = await discord_client.username(access_token=access_token)
        await discord_client.revoke_access_token(access_token)
    except aiohttp.ClientResponseError as e:
        logger.warning(f"Failed to fetch username from discord ({e.status})")
        return None
    except Exception as e:
        logger.error("Failed to fetch username from discord")
        logger.exception(e)
        return None

    return discord_username


def is_trying_to_login_with_discord(request: Request) -> bool:
    if request.query_params.get("code"):
        return True
    return False


def is_oauth_enabled() -> bool:
    return settings.discord_oauth_client_id != ""
