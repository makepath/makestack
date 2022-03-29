VERSION ?= latest
ENV ?= dev
REGISTRY_URL = mapstackregistry.azurecr.io

BACKEND_IMAGE_NAME = $(REGISTRY_URL)/backend:$(VERSION)
GEOSERVER_IMAGE_NAME = $(REGISTRY_URL)/geoserver:$(VERSION)
MAPSHADER_IMAGE_NAME = $(REGISTRY_URL)/mapshader:$(VERSION)
NGINX_IMAGE_NAME = $(REGISTRY_URL)/nginx:$(VERSION)

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
	docker build -t frontend ./docker/frontend/
	docker run --user non-privileged \
		-v ${PWD}/frontend:/code frontend /bin/bash \
		-c "yarn install;yarn build"
	cp -a ${PWD}/frontend/build/ ${PWD}/backend/frontend

.PHONY: build
build: build-frontend ## Build necessary stuff.
	docker-compose build --build-arg ENV=$(ENV)

.PHONY: enter-backend
enter-backend: ## Enter the backend container.
	$(ENTER_BACKEND) bash

.PHONY: first-run
first-run: ## Run migrations and create a default user.
	$(ENTER_BACKEND) python manage.py migrate --no-input
	$(ENTER_BACKEND) python manage.py create_super_user --email admin@admin.com --password admin --first_name admin --last_name user

.PHONY: publish
publish: ## Tag and push the docker images to registry.
	docker tag mapstack/backend $(BACKEND_IMAGE_NAME)
	docker tag mapstack/geoserver $(GEOSERVER_IMAGE_NAME)
	docker tag mapstack/mapshader $(MAPSHADER_IMAGE_NAME)
	docker tag mapstack/nginx $(NGINX_IMAGE_NAME)
	docker push $(BACKEND_IMAGE_NAME)
	docker push $(GEOSERVER_IMAGE_NAME)
	docker push $(MAPSHADER_IMAGE_NAME)
	docker push $(NGINX_IMAGE_NAME)

.PHONY: start
start: ## Start containers with docker-compose and attach to logs.
	docker-compose up --no-build

.PHONY: stop
stop: ## Stop all running containers.
	docker-compose stop

.PHONY: docs
docs: ## Build docs.
	make -C docs html
