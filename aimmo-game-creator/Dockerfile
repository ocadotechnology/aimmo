FROM python:2-alpine

MAINTAINER code@ocado.com

RUN apk add --no-cache gcc musl-dev python-dev libffi-dev openssl-dev bash curl

RUN pip install pipenv

COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]

RUN pipenv install --system --deploy

COPY docker-entrypoint.sh /usr/local/bin/

RUN ["/usr/local/bin/docker-entrypoint.sh"]

COPY . .

CMD ["python", "./service.py"]
