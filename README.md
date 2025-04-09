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

```
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
├─ run_cli.py               Runs the cli
├─ run_discord_bot.py       Runs the discord bot
├─ run_gg2_backend.py       Runs the gg2 TCP backend
```


## Deploy

### Environment variables

See [compose.env](./compose.env)

| Name | Default | Description |
| --- | --- | --- |
| DEBUG | true | Run the app in debug mode (mostly impacts uvicorn settings) |
| GG2_PORT | 51061 | TCP port for gg2 backend |
| WEBAPP_PORT | 51062 | TCP port for uvicorn webapp |
| SQLITE_FILE_NAME | ./database.db | File path to the sqlite database file, if postgres is not used |
| POSTGRES_HOST |  | Postgres db host. Should be "db" when used with compose. Leave empty to use sqlite instead |
| POSTGRES_PORT | 5432 | Postgres port |
| POSTGRES_USER |  | Postgres user name |
| POSTGRES_PASSWORD |  | Postgres db password |

### Code

A singular Dockerfile allows building the different components of the app

Then the compose stack, compose.yml, uses those components and bundles them nicely behind an nginx reverse proxy.

```bash
docker compose --env-file compose.env -f compose.yml up -d
```

Add `--profile postgres` when using postgres instead of sqlite:

```bash
docker compose --env-file compose.env -f compose.yml --profile postgres up -d
```

### Database

Sqlite file, created at `./database.db`.

Database migrations managed by alembic. `alembic upgrade head`

### Let's Encrypt

Stolen from https://phoenixnap.com/kb/letsencrypt-docker

Setup:
```bash
docker compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot/ --dry-run -d [domain-name]
```

Renew:
```bash
docker compose run --rm certbot renew
```