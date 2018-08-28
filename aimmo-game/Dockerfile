FROM python:2

MAINTAINER code@ocado.com

ENV WORKER_MANAGER=kubernetes

ONBUILD COPY Pipfile Pipfile
ONBUILD COPY Pipfile.lock Pipfile.lock

ONBUILD RUN pip install pipenv

ONBUILD RUN pipenv install --system

CMD ["python", "./service.py", "0.0.0.0", "5000"]
