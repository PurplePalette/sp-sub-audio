FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    ca-certificates \
    ffmpeg
COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.0.* && \
    CURL_CA_BUNDLE="" && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . ./

CMD gunicorn -k uvicorn.workers.UvicornWorker --workers 4 --bind=0.0.0.0:8000 src.main:app