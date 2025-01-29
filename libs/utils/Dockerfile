FROM python:3.10-slim

WORKDIR /libs/utils

# Install Poetry and upgrade pip
RUN pip install --upgrade pip && pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Use a build argument to specify the environment (default to development)
ARG ENV=development

# Install dependencies based on the environment
RUN poetry config virtualenvs.create false \
    && if [ "$ENV" = "production" ]; then \
        poetry install --no-root --without dev; \
    else \
        poetry install --no-root; \
    fi

# Copy library code
COPY ./src ./src
