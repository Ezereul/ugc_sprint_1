FROM jupyter/base-notebook

RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install --no-dev
