# Ziplink Frontend

React/Vite frontend for Ziplink. The app sends long URLs to the FastAPI backend and displays the generated short link.

## Prerequisites

- Node.js and npm
- Ziplink backend running at `http://127.0.0.1:8000`

## Run Locally

Install dependencies:

```bash
npm install
```

Start the Vite dev server:

```bash
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## Scripts

```bash
npm run dev      # Start local dev server
npm run build    # Build production assets
npm run preview  # Preview production build
npm run lint     # Run ESLint
```

## Backend Contract

The frontend currently calls:

```http
POST http://127.0.0.1:8000/shorten?long_url=<encoded-url>
```

Expected response:

```json
{
  "short_url": "1"
}
```

Generated links point to:

```text
http://127.0.0.1:8000/<short_url>
```
