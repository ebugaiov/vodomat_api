FROM python:3.12.6-slim

WORKDIR /api

COPY pyproject.toml uv.lock ./
COPY /static ./static
COPY /app ./app

RUN pip install uv && uv sync --frozen --no-cache

EXPOSE 7000

CMD ["/api/.venv/bin/fastapi", "run", "app/main.py", "--proxy-headers", "--host", "0.0.0.0", "--port", "7000"]