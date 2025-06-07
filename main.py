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
        data = await request.json()
        sql = data["sql"]

        # Connect to the SQLite Cloud database
        conn = sqlitecloud.connect(DB_URL)
        cursor = conn.execute(sql)

        # Get column names
        column_names = [description[0] for description in cursor.description]

        # Get values (list of lists, not list of dicts)
        values = [list(row) for row in cursor.fetchall()]

        conn.close()

        return {
            "success": True,
            "columns": column_names,
            "values": values
        }

    except Exception as e:
        return {"success": False, "error": str(e)}

@app.post("/insert")
async def insert_sql(request: Request):
    try:
        data = await request.json()
        sql = data["sql"]

        # Connect and execute the insert/update/delete SQL
        conn = sqlitecloud.connect(DB_URL)
        conn.execute(sql)
        conn.commit()  # optional, depending on driver settings
        conn.close()

        return {"success": True, "message": "Insert executed successfully."}
    except Exception as e:
        return {"success": False, "error": str(e)}
