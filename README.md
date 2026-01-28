# Vodomat API

## Overview
System for remote monitoring and control of vending water machines ("Vodomat"). This repository contains a FastAPI application that exposes a versioned REST API (v1) and a token-based security endpoint.

## Project status
- Basic API v1 implemented with multiple endpoints under `app/api/v1`.
- Authentication implemented in `app/api/v1/security.py` using JWTs.

## Requirements
- Python >= 3.12.6 (pyproject specifies 3.12.6)
- FastAPI >= 0.115.6
- MySQL >= 8.4
- Redis >= 5.2.1

## Quick start (local development)

1. Clone and enter the project
```bash
git clone <repo-url>
cd vodomat_api
```

2. Prepare environment
```bash
cp .env-example .env
```

3. Create venv and install dependencies (using `uv` to sync)
```bash
uv sync --frozen --no-cache
```

4. Run (development)
```bash
uv run fastapi dev
```

## Docker (build & run)

The project includes a `Dockerfile` and `docker-compose.yml` that wire an `api` service and a `redis` service. The compose file maps port 7000.

Build and run with docker-compose:

```bash
docker-compose up --build
```

This will build the `api` image and start Redis. The API will be available on port 7000 by default.

## API docs & usage

- Swagger UI (human-friendly API docs):
  - GET /v1/docs  (served by FastAPI; the app mounts the v1 docs at that path)
  - OpenAPI JSON: /v1/openapi.json

- Authentication
  - Obtain a token via the OAuth2 password flow:

```bash
curl -X POST "http://localhost:7000/security/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=<USERNAME>&password=<PASSWORD>"
```

The response contains an `access_token` and a `permission` field. Use the token in subsequent requests:

```bash
curl -H "Authorization: Bearer <TOKEN>" http://localhost:7000/v1/some-endpoint
```

## Project layout (top-level)

- app/
  - main.py                # application entrypoint
  - api/                   # API routers, v1 and v2 (v1 implemented)
    - v1/
      - endpoints/         # individual endpoint routers (city, street, avtomat, etc.)
      - schemas/
      - services/
  - core/
    - config.py            # configuration loaded from env
    - logger.py            # logging config
  - models/                # ORM / domain models
  - db/                    # DB and redis helpers
- static/                  # static files (favicon, icons)
- Dockerfile
- docker-compose.yml
- requirements.txt
- pyproject.toml
