FROM python:3.8

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN set -xe \
    && apt-get update -q \
    && apt-get install -y -q \
    graphviz

COPY ./app /code/app

EXPOSE 3000/tcp

CMD ["uvicorn", "app.main:app", "--port", "3000"]
