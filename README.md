# FastAPI

## Engine
- [fastApiServer] : API 엔진 (인증을 위한 JWT 토큰 필요)

## 필요 항목
- Config 파일 경로 참조하도록 설정: ./api.cfg

## 엔진 빌드 방법
- pyinstaller -F fastApiServer.py --hidden-import passlib --hidden-import passlib.handlers.bcrypt

## API 호출 목록
- fastApiServer