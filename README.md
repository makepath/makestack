# Mapstack

## Environment

For default, all the below services are already pre-configured and available to be used.

- Backend (Django)
- Celery
- Frontend (React App)
- GeoServer
- Mapshader
- Nginx
- PostgreSQL
- Redis

## Basic Commands

You can use the shortcuts from Makefile. Type ``make`` on your terminal, and you'll see all available targets.

```
help                     Show make targets.
backend-coverage         Enter the running backend container and get coverage tests.
backend-test             Enter the running backend container and run tests.
build-frontend           Build the frontend image.
build                    Build necessary stuff.
enter-backend            Enter the backend container.
first-run                Run migrations and create a default user.
publish                  Tag and push the docker images to registry.
start                    Start containers with docker-compose and attach to logs.
stop                     Stop all running containers.
```

## Getting Started

### Prerequisites

- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [GNU Make](https://www.gnu.org/software/make/)
- [Kubernetes command-line tool](https://kubernetes.io/docs/tasks/tools/)
- [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli?in=terraform/azure-get-started)

### Running locally

1. Build the applications by running the command ```make build```
2. Start the applications by running the command ```make start```
