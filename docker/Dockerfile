FROM python:3.12 AS build-common

RUN apt install uv

COPY gg2haxxy25 gg2haxxy25

RUN uv install

FROM build-common AS backend

CMD [ "python", "gg2haxxy25/backend/main.py" ]

FROM build-common AS discordbot

CMD [ "python", "gg2haxxy25/discordbot/main.py" ]

FROM build-common AS website

CMD [ "python", "gg2haxxy25/website/main.py" ]