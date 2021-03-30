from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi_discord import DiscordOAuthClient, Unauthorized, RateLimited

router = APIRouter(
    prefix='/discord',
    tags=['discord']
)

client_id = ""
client_secret = ""
discord = DiscordOAuthClient(client_id, client_secret, "http://localhost:8000/discord/callback",
                             ("identify", "guilds", "email"))  # scopes


@router.get("/login")
async def login():
    return {
        "url": discord.oauth_login_url
    }


@router.get("/callback")
async def callback(code: str):
    print(code)
    token, refresh_token = await discord.get_access_token(code)
    return {
        "access_token": token,
        "refresh_token": refresh_token
    }


@router.get("/hello")
@discord.requires_authorization
async def hello(request: Request):
    # Request Header
    # Authorization: Bearer [AccessToken]
    return await discord.user(request)
    return f'Hello {user.username}#{user.discriminator}!'


@router.get('/authenticated')
async def auth(request: Request):
    # Request Header
    # Authorization: Bearer [AccessToken]
    try:
        token = discord.get_token(request)
        auth = await discord.isAuthenticated(token)
        return f'{auth}'
    except Unauthorized:
        return 'False'


@router.get("/require_auth")
@discord.requires_authorization
async def test(request: Request):
    return 'Hello!'


async def unauthorized_error_handler(request: Request, e: Unauthorized):
    return JSONResponse({
        "error": "Unauthorized"
    })


async def ratelimit_error_handler(request: Request, e: RateLimited):
    return JSONResponse({
        "error": "RateLimited",
        "retry": e.retry_after,
        "message": e.message
    })
