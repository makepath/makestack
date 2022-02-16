ENTER_BACKEND:=docker-compose exec backend

.PHONY: help
help: ## Show make targets.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; \
		{printf "\033[36m%-25s", $$1} \
		/#__danger/ {printf "\033[31m%s ", "DANGER"} \
		{gsub(/#__danger /, ""); printf "\033[0m%s\n", $$2}'

.PHONY: backend-coverage
backend-coverage: ## Enter the running backend container and get coverage tests.
	$(ENTER_BACKEND) coverage run -m pytest
	$(ENTER_BACKEND) coverage report
	$(ENTER_BACKEND) coverage html -d coverage_html

.PHONY: backend-test
backend-test: ## Enter the running backend container and run tests.
	$(ENTER_BACKEND) pytest

.PHONY: build-frontend
build-frontend: ## Build the frontend image.
	docker build --platform linux/amd64 -t frontend ./docker/frontend/
	docker run --user non-privileged \
		-v ${PWD}/frontend:/code frontend /bin/bash \
		-c "yarn install;yarn build"
	cp -a ${PWD}/frontend/build/ ${PWD}/backend/frontend

.PHONY: build
build: build-frontend ## Build necessary stuff.
	docker-compose build

.PHONY: enter-backend
enter-backend: ## Enter the backend container.
	$(ENTER_BACKEND) bash

.PHONY: first-run
first-run: ## Run migrations and create a default user.
	$(ENTER_BACKEND) python manage.py migrate --no-input
	$(ENTER_BACKEND) python manage.py create_super_user --email admin@admin.com --password admin --first_name admin --last_name user

.PHONY: start
start: ## Start containers with docker-compose and attach to logs.
	docker-compose up --no-build

.PHONY: stop
stop: ## Stop all running containers.
	docker-compose stop