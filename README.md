# URL 단축 서비스

---

## 프로젝트 개요
* 긴 URL 을 짧은 URL 로 변환해주는 서비스를 제공한다.

---

##  시스템 요구사항
* **Language:** Python 3.12
* **Framework:** FastAPI
* **Database:** MySQL 8.0

---

## 설치 & 실행 방법
Docker 를 이용해서 `FastAPI 서버`와 `MySQL 서버`를 실행시킨다.
</br></br>

1. **환경변수 파일 설정:**
   - `short-url/` 디렉토리 하위에 `.env` 파일, `.env.mysql` 파일을 설정한다.
2. **Docker Compose 로 실행:**
   ```
   $ docker compose up -d
   ```
   
---
