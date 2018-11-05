FROM python:3.7 as builder
MAINTAINER code@ocado.com
# RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev
RUN pip install pipenv
COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]
RUN pipenv install --system --deploy

FROM python:3.7-alpine as base
COPY --from=builder /usr/local/lib/python3.7/site-packages /usr/local/lib/python3.7/site-packages
COPY . .


FROM base as runner
ENV WORKER_MANAGER=kubernetes
ENV FLASK_ENV='development'
CMD python ./service.py 0.0.0.0 $PORT $DATA_URL


FROM base as tester
ENV WORKER_MANAGER=kubernetes
CMD  python setup.py test