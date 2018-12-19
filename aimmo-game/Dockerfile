FROM python:3.6 as builder
MAINTAINER code@ocado.com
RUN pip install pipenv
COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]
RUN pipenv install --system --deploy

FROM python:3.6-alpine as base
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY . .

FROM base as tester
STOPSIGNAL SIGINT
RUN pip install coverage
CMD exec coverage run setup.py test

FROM base as runner
ENV WORKER_MANAGER=kubernetes
CMD python ./service.py 0.0.0.0 5000
