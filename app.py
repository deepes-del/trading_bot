from fastapi import FastAPI
from pydantic import BaseModel
from main import start_bot, running_bots

app = FastAPI()


class BotConfig(BaseModel):
    user_id: str
    mode: str = "default"
    sl: int = 10
    target: int = 20
    index: str = "NIFTY"


@app.post("/start-bot")
def start_bot_api(config: BotConfig):
    user_config = {
        "user_id": config.user_id,
        "mode": config.mode,
        "sl": config.sl,
        "target": config.target,
        "index": config.index,
        "is_running": True,
        "stop_requested": False
    }

    started = start_bot(config.user_id, user_config)

    if started:
        return {"status": f"Bot started for user {config.user_id}"}
    else:
        return {"error": f"Bot already running for user {config.user_id}"}


@app.post("/stop-bot")
def stop_bot_api(user_id: str):
    if user_id in running_bots:
        running_bots[user_id]["config"]["stop_requested"] = True
        return {"status": f"Stop requested for user {user_id}"}

    return {"error": "Bot not running for this user"}
