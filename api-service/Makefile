.PHONY : build run dev test network prune clean

default: run

build:
	@echo '### BUILDING GO BINARY'
	@go build -o api cmd/main.go

run:
	@go run cmd/main.go

dev:
	@echo '### STARTING PROD ENV'
	@cp .env.prod .env;

test:
	@go test -v ./...

api-test:
	@go test -v ./cmd/

network:
	@docker network create uty-net

prune:
	@echo '### PRUNING DOCKER SYSTEM'
	@docker system prune -a

compose:
	docker-compose up -d

composedown:
	docker-compose down

clean:
	@docker rm -vf $$(docker ps -aq)
	@docker rmi -f $$(docker images -a -q)