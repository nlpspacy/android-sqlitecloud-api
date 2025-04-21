# android-sqlitecloud-api

This is a lightweight FastAPI proxy that connects an Android app to SQLiteCloud via a simple HTTP `/query` endpoint.

## Usage

- POST raw SQL queries like `{ "sql": "SELECT * FROM play_character" }`
- Returns structured JSON rows

## Deployment

1. Push this repo to GitHub
2. Deploy it on [Railway](https://railway.app) by connecting your GitHub repo
3. Use the public URL in your Android app
