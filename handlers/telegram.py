import os
from fastapi import APIRouter, Request
from dotenv import load_dotenv
from handlers.executor import get_tmux_status, run_command, get_log, stop_session
from utils.responder import send_message
from utils.claude import ask_claude

load_dotenv()

router = APIRouter()

ALLOWED_USER_ID = str(os.getenv("ALLOWED_USER_ID", ""))


def is_allowed(user_id: str) -> bool:
    return user_id == ALLOWED_USER_ID


async def handle_ping(chat_id: str) -> None:
    await send_message(chat_id, "✅ JH Dispatch Bot 정상 가동 중")


async def handle_status(chat_id: str) -> None:
    status = get_tmux_status()
    await send_message(chat_id, f"📊 *서버 상태*\n{status}")


async def handle_run(chat_id: str, args: str) -> None:
    cmd = args.strip() if args else "echo '실행할 명령을 입력하세요. 예: /run npm run dev'"
    await send_message(chat_id, f"🚀 실행 중: `{cmd}`")
    result = run_command(cmd)
    await send_message(chat_id, result)


async def handle_log(chat_id: str) -> None:
    log = get_log(50)
    await send_message(chat_id, f"📋 *최근 로그*\n{log}")


async def handle_stop(chat_id: str, args: str) -> None:
    session = args.strip() if args else ""
    result = stop_session(session)
    await send_message(chat_id, result)


async def handle_ask(chat_id: str, args: str) -> None:
    question = args.strip()
    if not question:
        await send_message(chat_id, "❓ 질문을 입력해주세요. 예: `/ask 파이썬으로 파일 읽는 법`")
        return
    await send_message(chat_id, "🤔 Claude에게 물어보는 중...")
    answer = ask_claude(question)
    await send_message(chat_id, answer)


async def handle_help(chat_id: str) -> None:
    text = (
        "📌 *JH Dispatch Bot 명령 목록*\n\n"
        "/ping — 서버 생존 확인\n"
        "/status — tmux 세션 상태\n"
        "/run [명령] — 명령 실행\n"
        "/log — 최근 로그 50줄\n"
        "/stop [세션명] — 실행 중단\n"
        "/ask [질문] — Claude에게 질문\n"
        "/help — 명령 목록"
    )
    await send_message(chat_id, text)


COMMAND_MAP = {
    "/ping": handle_ping,
    "/status": handle_status,
    "/run": handle_run,
    "/log": handle_log,
    "/stop": handle_stop,
    "/ask": handle_ask,
    "/help": handle_help,
}


@router.post("/webhook")
async def telegram_webhook(request: Request):
    body = await request.json()

    message = body.get("message", {})
    if not message:
        return {"ok": True}

    chat_id = str(message.get("chat", {}).get("id", ""))
    user_id = str(message.get("from", {}).get("id", ""))
    text = message.get("text", "").strip()

    if not is_allowed(user_id):
        return {"ok": True}

    if not text:
        return {"ok": True}

    parts = text.split(" ", 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    handler = COMMAND_MAP.get(command)
    if handler:
        if command in ("/run", "/stop", "/ask"):
            await handler(chat_id, args)
        else:
            await handler(chat_id)
    else:
        await send_message(chat_id, f"❓ 알 수 없는 명령: `{command}`\n/help 로 명령 목록 확인")

    return {"ok": True}
