# Mapstack

## Basic Commands

You can use the shortcuts from Makefile. Type ``make`` on your terminal, and you'll see all available targets.

```
help                     Show make targets.
build-frontend           Build the frontend image.
build                    Build necessary stuff.
enter-backend            Enter the backend container.
first-run                Run migrations.
start                    Start containers with docker-compose and attach to logs.
stop                     Stop all running containers.
```

## Getting Started

### Prerequisites

- [GNU Make](https://www.gnu.org/software/make/)
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running locally

1. Build the applications by running the command ```make build```
2. Start the applications by running the command ```make start```# testing
