FROM python:3.6 as builder
MAINTAINER code@ocado.com
# RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev
RUN pip install pipenv
COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]
RUN pipenv install coverage
RUN pipenv install --system --deploy

FROM python:3.6-alpine as base
COPY --from=builder /usr/local/lib/python3.6/site-packages /usr/local/lib/python3.6/site-packages
COPY . .

FROM base as tester
ENV WORKER_MANAGER=kubernetes
CMD ["python", "setup.py", "test"]

FROM base as coverage_tester
ENV WORKER_MANAGER=kubernetes
ENV WITH_COVERAGE='True'
RUN apk add bash
COPY --from=builder /usr/local/bin/coverage /usr/local/bin/coverage
CMD python setup.py test

FROM base as runner
ENV WORKER_MANAGER=kubernetes
CMD ["python", "./service.py", "0.0.0.0"]
