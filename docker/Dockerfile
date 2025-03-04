FROM python:3.12 AS build-common

RUN apt install uv

COPY src src

RUN uv install

WORKDIR src

FROM build-common AS backend

CMD [ "python", "gg2haxxy25/gg2/main.py" ]

FROM build-common AS discordbot

CMD [ "python", "gg2haxxy25/discordbot/main.py" ]

FROM build-common AS website

CMD [ "python", "gg2haxxy25/main.py" ]