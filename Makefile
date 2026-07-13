.PHONY: run-api run-frontend db-init test docker-up

run-api:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

run-frontend:
	streamlit run frontend/Home.py

db-init:
	python -c "from app.db.session import init_db; init_db()"

test:
	pytest -v

docker-up:
	docker-compose up --build

eval:
	python scripts/run_evaluation.py