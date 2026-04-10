import os
import anthropic
from dotenv import load_dotenv

load_dotenv()

_client = None


def _get_client() -> anthropic.Anthropic:
    global _client
    if _client is None:
        _client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    return _client


def ask_claude(question: str) -> str:
    try:
        client = _get_client()
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[{"role": "user", "content": question}],
        )
        return message.content[0].text
    except anthropic.AuthenticationError:
        return "❌ ANTHROPIC_API_KEY가 유효하지 않습니다. .env를 확인해주세요."
    except Exception as e:
        return f"❌ Claude 호출 오류: {str(e)}"
