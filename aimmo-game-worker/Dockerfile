FROM python:2-alpine

MAINTAINER code@ocado.com

RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev bash curl

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]

RUN pipenv install --system --deploy

COPY . .

CMD python service.py 0.0.0.0 5000 $DATA_URL
