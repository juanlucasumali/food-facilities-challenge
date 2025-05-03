.PHONY: run test truncate-db init-db

run:
	docker compose up --build

test:
	pytest -q

init-db:
	python scripts/init_and_load.py

truncate-db:
	python scripts/truncate_db.py