FROM python:3.10-slim

WORKDIR /app

# Install Poetry and upgrade pip
RUN pip install --upgrade pip && pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

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

# Expose the port for FastAPI
EXPOSE 8002

CMD ["poetry", "run", "uvicorn", "src.weather_service.main:app", "--host", "0.0.0.0", "--port", "8002"]
