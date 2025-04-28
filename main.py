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

@app.post("/query")
async def query_sql(request: Request):
    try:
        body = await request.json()
        sql = body.get("sql")
        conn = sqlitecloud.connect(DB_URL)
        cursor = conn.execute(sql)
        columns = [description[0] for description in cursor.description]

        rows = []
        for row in cursor.fetchall():
            row_data = dict(zip(columns, row))

            # Safely handle voice fields even if missing
            row_data["voice_model"] = row_data.get("voice_model", "")
            row_data["voice_instructions"] = row_data.get("voice_instructions", "")

            rows.append(row_data)

        conn.close()

        return {"success": True, "rows": rows}
    except Exception as e:
        return {"success": False, "error": str(e)}
