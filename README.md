# Gang Garrison 2 Haxxy Awards 2025 Webapp

Python webapp that does a lot of things for the 2025 edition of the Gang Garrison 2 Haxxy Awards

Python 3.12 with uv, FastAPI, Nextcord, Sqlite

## Dev

Format with ruff

```bash
ruff format
ruff check --fix
```

### Python components

- **common**: Shared data models, persistence
- **gg2**: The part that talks with the actual game. Uses raw TCP
- **webapp**: FastAPI website
- **discordbot**: Discord bot

## Deploy

### Code

A singular Dockerfile allows building the different components of the app

Then the compose stack, compose.yml, uses those components and bundles them nicely behind an nginx reverse proxy. `docker compose up`

### Database

Sqlite file, created at `./database.db`.

Delete it manually when updating db models and running db migrations. Yeah that's bad, maybe setup alembic instead