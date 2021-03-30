from fastapi import FastAPI
from fastapi_discord import Unauthorized, RateLimited
from routes import discord

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


app.include_router(discord.router)

app.add_exception_handler(Unauthorized, discord.unauthorized_error_handler)
app.add_exception_handler(RateLimited, discord.ratelimit_error_handler)
