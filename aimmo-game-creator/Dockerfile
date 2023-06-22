FROM python:3.8.17-buster as builder
LABEL Author='codeforlife@ocado.com'
RUN pip install pipenv=="2018.11.26"
COPY ["Pipfile", "Pipfile.lock", "setup.py", "./"]
RUN pipenv install --system --deploy

FROM python:3.8.17-buster as base
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY . .

FROM base as tester
RUN pip install coverage
CMD ./run_tests.sh -c

FROM base as runner
ENV WORKER=kubernetes
CMD python ./service.py 0.0.0.0

