#!/bin/bash

# CRLF 자동 변환 (윈도우 환경에서 문제 방지)
sed -i 's/\r$//' "$0"

# 실행 권한 자동 부여
chmod +x "$0"

## .env 파일 로드 (환경 변수 없을 경우 대비)
#if [ -f .env ]; then
#    export $(grep -v '^#' .env | xargs)
#fi

# 필수 환경 변수 체크
REQUIRED_VARS=("MYSQL_USER" "MYSQL_PASSWORD" "MYSQL_HOST" "MYSQL_DATABASE")
for VAR in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!VAR}" ]; then
        echo "[ERROR]: $VAR 환경 변수가 설정되지 않았습니다."
        exit 1
    fi
done

# 환경 변수 설정
DB_USER=$MYSQL_USER
DB_PASS=$MYSQL_PASSWORD
DB_HOST=$MYSQL_HOST
DB_NAME=$MYSQL_DATABASE

# 사용된 환경 변수 표시
echo "====================================================================================================="
echo "✔︎ 사용된 환경 변수"
echo "====================================================================================================="
echo "DB_USER: $DB_USER"
echo "DB_HOST: $DB_HOST"
echo "DB_NAME: $DB_NAME"
echo "DB_PASS: ********"

# SQLACodegen 설치 확인 및 자동 설치
if ! command -v sqlacodegen &> /dev/null; then
    echo "====================================================================================================="
    echo "✔︎ SQLACodegen 설치 중..."
    echo "====================================================================================================="
    pip install sqlacodegen pymysql
fi

# 모델 생성 (윈도우 특수문자 대비)
echo "====================================================================================================="
echo "✔︎ 모델 생성"
echo "====================================================================================================="
SQLALCHEMY_URL="mysql+pymysql://${DB_USER}:${DB_PASS}@${DB_HOST}/${DB_NAME}"

# 윈도우 환경에서 `&` 등의 특수문자 문제 방지
SQLALCHEMY_URL_ESCAPED=$(printf "%q" "$SQLALCHEMY_URL")

echo "데이터베이스 연결: $SQLALCHEMY_URL_ESCAPED"
sqlacodegen "$SQLALCHEMY_URL" > ./src/models/models.py

# 결과 확인
echo "====================================================================================================="
echo "✔︎ 모델 생성 결과"
echo "====================================================================================================="
if [ $? -eq 0 ]; then
    echo "모델 생성 완료: ./src/db/models.py"
else
    echo "[ERROR]: 모델 생성 실패"
fi
