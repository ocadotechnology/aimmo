FROM python:2-alpine

MAINTAINER code@ocado.com

COPY . .

RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "./service.py"]
