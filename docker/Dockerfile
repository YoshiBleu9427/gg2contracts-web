FROM python:3.12

RUN apt install uv

COPY src src

RUN uv install

WORKDIR src
ENTRYPOINT [ "python" ]

CMD ["contracts/gg2/main.py"]
