FROM python:3.10.10-slim-buster

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir ./flask_utils && mkdir -p ./plugin_management/plugins

COPY ../Index-All-In-One-Flask.py .
COPY ../flask_utils/*.py ./flask_utils/
COPY ../plugin_management/plugins/*.py ./plugin_management/plugins/

COPY ../scripts/flask-docker-dev.sh .
RUN chmod +x flask-docker-dev.sh
ENTRYPOINT ["./flask-docker-dev.sh"]
