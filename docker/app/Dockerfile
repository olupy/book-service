FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y gcc python3-dev musl-dev libmagic1 libffi-dev git netcat-traditional
RUN apt-get install -y wkhtmltopdf
#RUN pip install --no-cache-dir poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN pip install poetry==2.0.0
RUN poetry config virtualenvs.create false
RUN poetry install --no-root


COPY app /app

EXPOSE 8000

