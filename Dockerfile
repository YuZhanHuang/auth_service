FROM python:3.9.16-slim-bullseye AS app
WORKDIR /app
COPY pyproject.toml ./
RUN mkdir -p /app/logs
RUN apt-get update && apt-get install -y gcc build-essential vim --no-install-recommends \
    && apt install libffi-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean \
    && /usr/local/bin/python -m pip install --upgrade pip \
    && pip install poetry==1.5 \
    && poetry install --no-root
COPY . .
COPY ./docker_entrypoint/service/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]