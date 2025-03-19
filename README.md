# Gang Garrison 2 Contracts Webapp

Python webapp and backend for the Contracts plugin for Gang Garrison 2

Python 3.12 with uv, FastAPI, Nextcord, Sqlite

## Dev

Install with uv

```bash
uv sync
```

Format with ruff

```bash
ruff format
ruff check --fix
```

Typing with mypy

```bash
mypy src
```

### Components

src/
├─ alembic/                 DB migrations
├─ cli/                     CLI for interacting directly with the backend
├─ contracts/               Main source files:
│  ├─ common/                   Shared data models, persistence
│  ├─ discordbot/               Discord bot
│  ├─ gg2/                      The part that talks with the actual game. Uses raw TCP
│  ├─ webapp/                   FastAPI website
├─ static/                  Website static assets
├─ templates/               Website templates
├─ main.py                  Runs the main web app
├─ run_discord_bot.py       Runs the discord bot
├─ run_gg2_backend.py       Runs the gg2 TCP backend


## Deploy

### Code

A singular Dockerfile allows building the different components of the app

Then the compose stack, compose.yml, uses those components and bundles them nicely behind an nginx reverse proxy. `docker compose up`

### Database

Sqlite file, created at `./database.db`.

Database migrations managed by alembic. `alembic upgrade head`
