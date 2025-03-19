FROM python:3.12

RUN apt install uv

COPY src src
COPY alembic.ini alembic.ini
COPY pyproject.toml pyproject.toml
COPY uv.lock uv.lock

RUN uv sync

WORKDIR src
ENTRYPOINT [ "uv", "run" ]

CMD ["src/main.py"]
