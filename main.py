from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlitecloud

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = "sqlitecloud://cgdjyovjhk.g2.sqlite.cloud:8860/play_navigation.db?apikey=SFR0f2mYTxb3bbOiaALxEyatvEt2WDn5hYygAXiuE2o"

# ✅ Add this new /query endpoint
@app.post("/query")
async def run_sql_query(request: Request):
    data = await request.json()
    sql = data.get("sql")

    try:
        conn = sqlitecloud.connect(DB_URL)
        cursor = conn.execute(sql)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()

        # Reformat to match the expected structure
        response_data = {
            "columns": columns,
            "values": [list(row) for row in rows]
        }
        conn.close()
        return response_data
    except Exception as e:
        return {"error": str(e)}
