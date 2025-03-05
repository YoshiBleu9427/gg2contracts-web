FROM python:3.12

RUN apt install uv

COPY src src

RUN uv install

WORKDIR src
ENTRYPOINT [ "python" ]

CMD ["gg2haxxy25/gg2/main.py"]
