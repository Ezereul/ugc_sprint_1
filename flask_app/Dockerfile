FROM python:3.11-slim

WORKDIR /flask_app
ENV PATH /flask_app/.venv/bin:$PATH
ENV PYTHONPATH /:$PYTHONPATH

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN python -m pip install --no-cache-dir poetry==1.8.2 \
    && poetry config virtualenvs.in-project true \
    && poetry install --no-interaction --no-ansi

COPY . .

ENTRYPOINT ["bash", "/flask_app/docker-entrypoint.sh"]
