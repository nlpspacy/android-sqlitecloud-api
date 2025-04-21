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
    body = await request.json()
    sql = body.get("sql")
    try:
        conn = sqlitecloud.connect(DB_URL)
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        result = [dict(zip(column_names, row)) for row in rows]
        conn.close()
        return {"success": True, "rows": result}
    except Exception as e:
        return {"success": False, "error": str(e)}
