# jh-dispatch-bot

텔레그램(@leejaehabot)으로 사무실 PC를 원격 제어하는 디스패치 봇

---

## 설치 순서

### 1. Python 환경
```bash
python -m venv .venv
.venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### 2. .env 설정
```bash
copy .env.example .env
```
`.env` 파일 열어서 입력:
```
BOT_TOKEN=발급받은_텔레그램_토큰
ALLOWED_USER_ID=본인_텔레그램_ID
WEBHOOK_URL=https://your-domain.trycloudflare.com
```

> 텔레그램 ID 확인: @userinfobot 에 /start 전송

### 3. Cloudflare Tunnel 설치 (PC)
```bash
# https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
# cloudflared.exe 다운로드 후

cloudflared tunnel login
cloudflared tunnel create jh-dispatch
cloudflared tunnel route dns jh-dispatch your-subdomain.your-domain.com

# 실행
cloudflared tunnel --url http://localhost:8000 run jh-dispatch
```

> 임시 도메인 테스트 시 (계정 없이):
> ```
> cloudflared tunnel --url http://localhost:8000
> ```
> 출력된 URL을 WEBHOOK_URL에 입력 (재시작마다 변경됨)

### 4. 봇 서버 실행
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
또는 `start.bat` 더블클릭

### 5. Windows 시작프로그램 등록
```
Win + R → shell:startup
start.bat 바로가기 붙여넣기
```

---

## 명령 목록

| 명령 | 설명 |
|------|------|
| `/ping` | 서버 생존 확인 |
| `/status` | tmux 세션 상태 |
| `/run [명령]` | 명령 실행 (예: `/run npm run dev`) |
| `/log` | 최근 로그 50줄 |
| `/stop [세션명]` | 실행 중단 |
| `/help` | 명령 목록 |

---

## 태블릿 화면 수신 설정

1. PC: [Tailscale](https://tailscale.com) 설치 → 로그인
2. 태블릿: Tailscale 설치 → 동일 계정 로그인
3. PC: [Chrome Remote Desktop](https://remotedesktop.google.com) 설치 → 원격 액세스 활성화
4. 태블릿: Chrome Remote Desktop 앱 → PC 선택 → 뷰어 모드

---

## 보안 주의

- `.env` 파일 절대 git 커밋 금지
- `ALLOWED_USER_ID` 반드시 본인 ID로 설정
- 토큰 채팅/이미지 노출 금지
