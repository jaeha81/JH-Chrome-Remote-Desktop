import os
import httpx
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from handlers.telegram import router as telegram_router

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 웹훅 자동 등록
    if BOT_TOKEN and WEBHOOK_URL:
        webhook_endpoint = f"{WEBHOOK_URL}/telegram/webhook"
        async with httpx.AsyncClient() as client:
            res = await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook",
                json={"url": webhook_endpoint},
            )
            print(f"[Webhook] 등록 결과: {res.json()}")
    else:
        print("[Webhook] BOT_TOKEN 또는 WEBHOOK_URL 미설정 — 웹훅 등록 건너뜀")
    yield


app = FastAPI(title="JH Dispatch Bot", lifespan=lifespan)
app.include_router(telegram_router, prefix="/telegram")


@app.get("/health")
async def health():
    return {"status": "ok", "bot": "@leejaehabot"}
