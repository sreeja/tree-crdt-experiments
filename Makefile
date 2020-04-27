run-dev:
	docker-compose docker-compose.yml up

run-dev-build:
	docker-compose docker-compose.yml --build

down:
	docker-compose down -v --remove-orphans
