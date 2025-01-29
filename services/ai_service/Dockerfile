FROM python:3.10-slim

WORKDIR /app

# Install Poetry and upgrade pip
RUN pip install --upgrade pip && pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Set PYTHONPATH to include /app
ENV PYTHONPATH="/app"

# Use a build argument to specify the environment (default to development)
ARG ENV=development

# Install dependencies based on the environment
#RUN poetry config virtualenvs.create false \
 #   && if [ "$ENV" = "production" ]; then \
  #      poetry install --no-root --without dev; \
   # else \
    #    poetry install --no-root; \
    #fi
    RUN poetry install --no-root

# Copy source code
COPY ./src ./src
COPY ./tests ./tests
COPY ./libs /app/libs

# Expose the port for FastAPI
EXPOSE 8001

CMD ["poetry", "run", "uvicorn", "src.ai_service.ml_main:app", "--host", "0.0.0.0", "--port", "8001"]
