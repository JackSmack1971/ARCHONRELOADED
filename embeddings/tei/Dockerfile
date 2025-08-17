# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN adduser --system --uid 1001 appuser

COPY config/config.yml /app/config.yml
COPY models/ /app/models/
RUN chown -R appuser:appuser /app && chmod 640 /app/config.yml

USER appuser

ENV TEI_API_TOKEN=${TEI_API_TOKEN}
ENV TEI_API_URL=${TEI_API_URL}
ENV TEI_MODEL_NAME=${TEI_MODEL_NAME:-default-model}

RUN pip install --no-cache-dir tei

ENTRYPOINT ["python", "-m", "tei", "--config", "/app/config.yml", "--model", "${TEI_MODEL_NAME}"]
