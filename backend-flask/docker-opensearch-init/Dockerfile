FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY plugin_management/plugins/*.py .

COPY docker-opensearch-init/index.json .

COPY docker-opensearch-init/opensearch-init-entry.sh .
RUN chmod +x opensearch-init-entry.sh
ENTRYPOINT ["./opensearch-init-entry.sh"]
