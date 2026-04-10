import subprocess


def get_tmux_status() -> str:
    try:
        result = subprocess.run(
            ["tmux", "list-sessions"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            sessions = result.stdout.strip()
            count = len(sessions.splitlines())
            return f"✅ tmux 세션 활성: {count}개\n```\n{sessions}\n```"
        return "⚠️ 활성 tmux 세션 없음"
    except FileNotFoundError:
        return "❌ tmux 미설치 또는 경로 없음"
    except subprocess.TimeoutExpired:
        return "❌ tmux 응답 timeout"


def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        output = result.stdout.strip() or result.stderr.strip()
        if not output:
            return "✅ 실행 완료 (출력 없음)"
        return f"```\n{output[:3000]}\n```"
    except subprocess.TimeoutExpired:
        return "❌ 실행 timeout (30초 초과)"
    except Exception as e:
        return f"❌ 실행 오류: {str(e)}"


def get_log(lines: int = 50) -> str:
    try:
        result = subprocess.run(
            ["tmux", "capture-pane", "-p", "-S", f"-{lines}"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        log = result.stdout.strip()
        if not log:
            return "⚠️ 로그 없음"
        return f"```\n{log[-3000:]}\n```"
    except Exception as e:
        return f"❌ 로그 조회 오류: {str(e)}"


def stop_session(session_name: str = "") -> str:
    try:
        if session_name:
            target = session_name
        else:
            result = subprocess.run(
                ["tmux", "list-sessions", "-F", "#{session_name}"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            sessions = result.stdout.strip().splitlines()
            if not sessions:
                return "⚠️ 중단할 세션 없음"
            target = sessions[0]

        subprocess.run(
            ["tmux", "send-keys", "-t", target, "C-c", ""],
            timeout=5,
        )
        return f"🛑 세션 `{target}` 실행 중단 신호 전송"
    except Exception as e:
        return f"❌ 중단 오류: {str(e)}"
