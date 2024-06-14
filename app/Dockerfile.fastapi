# Use Python 3.11 as the base image
FROM python:3.11 as python-base

# Set the working directory to /lemonade
WORKDIR /app

# Copy poetry configuration files directly into /lemonade
COPY pyproject.toml poetry.lock ./

# Install Poetry, configure it to not create a virtual environment,
# and install dependencies defined in pyproject.toml
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# Copy the entire app directory into /lemonade/app
COPY . .

# Specify the command to start the application using Gunicorn with Uvicorn workers

## FOR PRODUCTION  ONLY
# CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8000"]

## FOR DEVELOPMENT

CMD ["uvicorn", "main:app", "--reload", "--proxy-headers", "--host", "0.0.0.0", "--port", "8000"]