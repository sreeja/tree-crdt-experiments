run-dev:
	docker-compose up

run-dev-build:
	docker-compose up --build

down:
	docker-compose down -v --remove-orphans
