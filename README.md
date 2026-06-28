# Ziplink

Ziplink is a small URL shortener built as a system-design learning project. It uses a FastAPI backend, PostgreSQL persistence, Redis-backed rate limiting, Base62 short codes, and a React/Vite frontend.

## Features

- Shortens long URLs into compact Base62 IDs.
- Returns the existing short code when the same long URL is submitted again.
- Redirects short URLs with HTTP `302`.
- Stores URL mappings in PostgreSQL.
- Rate-limits `POST /shorten` requests with Redis.
- Provides a React frontend for creating and opening short links.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL, psycopg2, Redis
- Frontend: React, Vite
- Tooling: uv, npm

## Project Structure

```text
Ziplink/
├── backend/
│   ├── base62.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── rate_limiter.py
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── .env.example
├── pyproject.toml
└── README.md
```

## Prerequisites

- Python 3.11+
- uv
- Node.js and npm
- PostgreSQL
- Redis

## Environment

Create a root-level `.env` file:

```bash
cp .env.example .env
```

Update the values for your local services:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ziplink
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
```

Create the configured PostgreSQL database before starting the backend. The backend creates the `urls` table automatically on startup.

If the backend runs in WSL and PostgreSQL runs on Windows, `localhost` may not resolve to the Windows PostgreSQL server. Use your Windows host gateway in `DATABASE_URL`, for example:

```env
DATABASE_URL=postgresql://postgres:your_password@172.19.80.1:5432/ziplink
```

If the database password contains special characters, URL-encode them. For example, `#` becomes `%23`.

## Run Locally

Start PostgreSQL and Redis first.

Run the backend:

```bash
cd backend
uv run main.py
```

Backend URLs:

```text
API:  http://127.0.0.1:8000
Docs: http://127.0.0.1:8000/docs
```

In a second terminal, run the frontend:

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://127.0.0.1:5173
```

## API

### Shorten a URL

```http
POST /shorten?long_url=https%3A%2F%2Fexample.com
```

Successful response:

```json
{
  "short_url": "1"
}
```

Rate-limited response:

```json
{
  "detail": "Too Many Requests"
}
```

The current sliding-window limiter allows 5 shorten requests per client IP per 60 seconds.

### Redirect

```http
GET /1
```

Successful response:

```text
302 Redirect
Location: https://example.com
```

Missing short code response:

```json
{
  "error": "URL not found"
}
```

## Base62 Encoding

Ziplink converts the database ID into a Base62 string using:

```text
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

Examples:

```text
1  -> "1"
62 -> "10"
```

## Useful Commands

Backend:

```bash
cd backend
uv run main.py
```

Frontend:

```bash
cd frontend
npm run dev
npm run build
npm run lint
```
