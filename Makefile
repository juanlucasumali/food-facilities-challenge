.PHONY: run test

run:
	docker compose up --build

test:
	pytest -q