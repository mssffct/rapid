# (Build stage)
FROM python:3.13-slim-bookworm AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# compile byte code
# no cache in container
# environment
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/app/.venv

WORKDIR /app

# copy dependencies
COPY ./server/pyproject.toml .
COPY ./server/uv.lock .

# install
RUN uv sync --frozen --no-install-project

# copy source code
COPY server/ .

# sync project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# (Runtime stage)
FROM python:3.13-slim-bookworm

# non root user
RUN groupadd -r appgroup && useradd -r -g appgroup -s /bin/false appuser

WORKDIR /app

# copy files from build stage
COPY --from=builder --chown=appuser:appgroup /app /app

# app env to path
ENV PATH="/app/.venv/bin:$PATH"

# python bytecode
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# using non root user
USER appuser

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8014", "--reload"]
