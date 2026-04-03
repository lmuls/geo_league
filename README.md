# Geo League

A personal leaderboard app for tracking GeoGuessr results among a friend group.

## What it does

Players save a GeoGuessr results page as an HTML file and upload it through the app. The backend parses the HTML to extract player names and scores, then updates the leaderboard. The leaderboard shows total points per player with an expandable view of per-game history and links back to the original GeoGuessr result page.

## Tech stack

| Layer | Tech |
|---|---|
| Frontend | React 18 + TypeScript, Material UI v5, React Router v6 |
| Backend | Python / FastAPI, SQLAlchemy ORM, BeautifulSoup4 for HTML parsing |
| Database | PostgreSQL |
| Infra | Docker + Docker Compose, Nginx (SPA + reverse proxy), GitHub Actions CI/CD |

## Project structure

```
geo_league/
├── backend/
│   ├── main.py              # FastAPI routes
│   ├── batch/parse_html.py  # GeoGuessr HTML scraper
│   ├── database/            # ORM models, schemas, DB session
│   ├── service/service.py   # Business logic / DB queries
│   └── alembic/             # DB migrations
├── frontend/
│   ├── src/
│   │   ├── comps/           # NavArea, CollapsibleTable, SubTable
│   │   └── routing/         # Home, Leaderboard, NewGame pages
│   └── nginx/nginx.conf     # Serves SPA + proxies /api/ to FastAPI
└── deployment/
    ├── docker-compose.yml       # Production
    └── docker-compose.dev.yml   # Dev (builds from source, includes test DB)
```

## Running locally

**Dev (builds from source):**
```bash
cd deployment
docker compose -f docker-compose.dev.yml up --build
```

**Production:**
```bash
cd deployment
docker compose up
```

The app is served at `http://localhost` (port 80). Nginx routes `/api/*` to FastAPI and everything else to the React SPA.

## API endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/leaderboard/` | Full leaderboard with per-player game history |
| `POST` | `/api/new-game/` | Upload a GeoGuessr HTML results file |
| `GET` | `/api/players` | List all players |
| `GET` | `/api/delete-game/{game_id}` | Delete a game and its scores |

## CI/CD

Pushing to `main` triggers a GitHub Actions workflow that builds and pushes Docker images to Docker Hub (`yolobreaker/geoleague_backend`, `yolobreaker/geoleague_frontend`).
