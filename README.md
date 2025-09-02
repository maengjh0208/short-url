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

## Coding Style
- python code style 을 자동으로 맞추기 위해 `flake8`, `black`, `isort` 을 사용한다.
- 변경된 소스 코드가 github 에 commit 되기 전에, pre-commit 으로 위 라이브러리들이 실행되도록 한다.
- 아래와 명령어를 한번 실행하면, commit 명령어를 실행할 떄마다 자동으로 코드 점검이 진행된다.
  ```
  $ pip install pre-commit
  $ pre-commit install
  ```

---

## SQLAlchemy 모델 자동 생성 방법
`sqlacodegen` 모듈을 이용하면 SQLAlchemy 모델을 수기로 작성하지 않고, 현재 바라보고 있는 DB 를 기준으로 해서 모델을 자동으로 생성할 수 있다.

- `scripts/generate-models.sh`: 모델 자동 생성 스크립트가 작성되어 있음
- `Makefile`: Makefile 에 작성된 명령어를 통해 위 스크립트를 간단히 실행시킬 수 있음

**실행 방법:**
```
$ make generate-models
```

---
