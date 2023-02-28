FROM python:3.10.10-slim-buster

WORKDIR /app

COPY ../requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ./plugin_management/plugins

COPY ../plugin_management/*.py ./plugin_management/
COPY ../plugin_management/plugins/*.py ./plugin_management/plugins/

ENTRYPOINT ["python", "plugin_management/manager.py"]
