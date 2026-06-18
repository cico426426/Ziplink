# Ziplink

A URL shortener built while learning system design — implements Base62 encoding, FastAPI + PostgreSQL backend, and a React frontend.

## Features

- Shortens long URLs into Base62 IDs.
- Reuses an existing short URL when the same long URL is submitted again.
- Redirects short URLs with HTTP `302`.
- Stores URL mappings in PostgreSQL.
- Provides a small React frontend for creating and opening short links.

## Tech Stack

- Backend: FastAPI, SQLAlchemy, PostgreSQL, psycopg2
- Frontend: React, Vite
- Package/runtime tooling: uv, npm

## Project Structure

```text
Ziplink/
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── base62.py
├── frontend/
│   ├── src/
│   ├── package.json
│   └── vite.config.js
├── pyproject.toml
└── README.md
```

## Backend Setup

Create a `.env` file in the project root:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/ziplink
```

If the backend runs in WSL and PostgreSQL runs on Windows, `localhost` may not work. Use the Windows host gateway instead:

```env
DATABASE_URL=postgresql://postgres:your_password@172.19.80.1:5432/ziplink
```

If your password contains special characters, URL encode them. For example, `#` becomes `%23`.

Run the backend:

```bash
cd backend
uv run main.py
```

Backend URL:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

## Frontend Setup

Install dependencies and start the Vite dev server:

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
POST /shorten?long_url=https://example.com
```

Response:

```json
{
  "short_url": "1"
}
```

### Redirect

```http
GET /1
```

Response:

```text
302 Redirect
Location: https://example.com
```

## Base62 Encoding

Ziplink converts the database ID into a Base62 string using:

```text
0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
```

Example:

```text
1 -> "1"
62 -> "10"
```
