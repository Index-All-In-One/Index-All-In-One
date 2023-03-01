FROM python:3.10.10-slim-buster

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY create_index.py .

ENTRYPOINT ["python", "create_index.py"]
