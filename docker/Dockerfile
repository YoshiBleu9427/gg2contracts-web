FROM python:alpine

RUN apt install uv

WORKDIR /opt/contracts

COPY src src
COPY alembic.ini alembic.ini
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv sync

ENTRYPOINT [ "uv", "run" ]

CMD ["src/main.py"]
