FROM python:3-alpine

MAINTAINER code@ocado.com

ENV WORKER_MANAGER=kubernetes

COPY . .

RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "./service.py", "0.0.0.0", "5000"]
