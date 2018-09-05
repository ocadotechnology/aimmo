FROM python:2

MAINTAINER code@ocado.com

COPY . .

RUN pip install pipenv

RUN pipenv install --system --deploy

CMD python service.py 0.0.0.0 5000 $DATA_URL
