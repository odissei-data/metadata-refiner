FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup --system refiner && adduser --system --ingroup refiner refiner

WORKDIR /app
COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential && \
    pip install --no-cache-dir poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root && \
    apt-get remove -y build-essential && apt-get autoremove -y && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY src/ /app/src
RUN chown -R refiner:refiner /app

USER refiner

WORKDIR /app/src