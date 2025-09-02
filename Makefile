 # Docker에서 SQLACodegen으로 모델 직접 생성 (.env 환경변수 사용)
generate-models:
	@echo "Docker 환경에서 SQLACodegen으로 SQLAlchemy 모델 생성 중..."
	docker exec -it short-url-backend bash scripts/generate-models.sh

help:
	@echo "Available commands:"
	@echo "   - generate-models: DB 모델 자동 생성 (src/models/models.py)"
