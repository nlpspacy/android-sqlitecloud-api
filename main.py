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
async def query_sql(payload: dict):
    sql = payload.get("sql")
    if not sql:
        raise HTTPException(status_code=400, detail="SQL statement required")
    try:
        conn = sqlitecloud.connect(DB_URL)
        cursor = conn.execute(sql)

        rows = cursor.fetchall()

        # ⚡ Correct format: values = list of lists
        values = []
        if cursor.description:
            col_names = [description[0] for description in cursor.description]
            for row in rows:
                values.append([row.get(col, None) for col in col_names])

        conn.close()

        return {
            "success": True,
            "columns": [desc[0] for desc in cursor.description] if cursor.description else [],
            "values": values  # ✅ Proper list-of-lists format
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

