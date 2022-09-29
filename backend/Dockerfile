FROM python:3.9.14-alpine

ENV PYTHONPATH=/app/
ENV DB_PORT=5432
ENV TEST_DB_PORT=5432
ENV DB_URL=postgresql://geouser:geoPASS123@db:${DB_PORT}/geoleague
ENV TEST_DB_URL=postgresql://geouser:geoPASS123@test-db:${TEST_DB_PORT}/geoleague

WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add postgresql-dev gcc python3-dev musl-dev g++


RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]