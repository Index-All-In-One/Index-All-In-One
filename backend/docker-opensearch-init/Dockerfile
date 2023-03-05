FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./opensearch
COPY opensearch/index.json ./opensearch/
COPY opensearch/*.py ./opensearch/

COPY opensearch/scripts/init-docker-dev.sh .
RUN chmod +x init-docker-dev.sh
ENTRYPOINT ["./init-docker-dev.sh"]
