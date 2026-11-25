FROM python:3-alpine
LABEL authors="claud"

WORKDIR /app

COPY main.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "main:app", "--host", "0.0.0.0"]