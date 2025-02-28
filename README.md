# Gang Garrison 2 Haxxy Awards 2025 Webapp

Python webapp that does a lot of things for the 2025 edition of the Gang Garrison 2 Haxxy Awards

Python 3.12 with uv

## Dev

### Python components

- **Commons**: Shared data models, persistence
- **Backend**: The part that talks with the actual game. Uses raw TCP
- **Website**: FastAPI website
- **Discord bot**: Discord bot

## Deploy

A singular Dockerfile allows building the different components of the app

Then the compose stack, compose.yml, uses those components and bundles them nicely behind an nginx reverse proxy. `docker compose up`