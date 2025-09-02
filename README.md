# URL 단축 서비스

## 프로젝트 개요
* 긴 URL 을 짧은 URL 로 변환해주는 서비스를 제공한다.

---

##  기술 스택

**Backend:**
```aiignore
- Language: Python 3.12
- FastAPI + Uvicorn
- SQLAlchemy (ORM)
- Alembic (DB 마이그레이션)
- Pydantic (데이터 검증)
```

**Database:**
```aiignore
- MySQL 8.0
- Redis (자주 사용되는 URL 정보)
```

---

## 설치 및 실행 방법
Docker 를 이용해서 `FastAPI`와 `MySQL`를 실행시킨다.

1. **환경변수 파일 설정:**
   - `short-url/` 디렉토리 하위에 `.env` 파일, `.env.mysql` 파일을 설정한다.
   - 두 파일은 `.gitignore` 에 포함되어 있어서, 따로 전달받아야 한다.
2. **Docker Compose 로 실행:**
   ```
   $ docker compose up -d
   ```
3. **로컬에서 실행 시 API 요청 테스트:**
   - GET http://127.0.0.1:8000/health-check

---
