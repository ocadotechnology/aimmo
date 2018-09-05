FROM python:2

MAINTAINER code@ocado.com

ENV WORKER_MANAGER=kubernetes

COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD ["python", "./service.py", "0.0.0.0", "5000"]
