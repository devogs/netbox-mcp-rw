FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first for better layer caching
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY server.py netbox_client.py http_server.py ./

RUN useradd --system --no-create-home mcp
USER mcp

ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# Streamable HTTP on :8000/mcp; NETBOX_URL and NETBOX_TOKEN come from the environment
CMD ["python", "http_server.py"]
