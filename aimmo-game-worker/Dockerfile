FROM python:3-alpine

MAINTAINER code@ocado.com

RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]

RUN pipenv install --system --deploy

COPY . .

ENV FLASK_ENV='development'

CMD python service.py 0.0.0.0 $PORT $DATA_URL
