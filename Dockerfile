# Base Python Image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install Poetry
RUN pip install --upgrade pip \
    && pip install poetry

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
# Expose ports for orchestration
EXPOSE 8000 8001

# Set environment variables dynamically
ENV ENV=$ENV
ENV PYTHONUNBUFFERED=1

# Default command for the container
CMD ["bash"]
