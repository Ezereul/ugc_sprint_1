FROM python:3.11-slim

RUN apt-get update && apt-get install -y netcat-openbsd curl

WORKDIR /etl
ENV PYTHONPATH /etl:$PYTHONPATH

COPY . /etl

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev

RUN chmod +x /etl/entrypoint.sh

ENTRYPOINT ["/etl/entrypoint.sh"]
