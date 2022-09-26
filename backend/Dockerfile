FROM python:3.9.14-alpine
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt

RUN apk add postgresql-dev gcc python3-dev musl-dev g++


RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY . /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]