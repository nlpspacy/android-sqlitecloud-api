from fastapi import FastAPI, HTTPException, Request
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

def get_connection():
    return sqlitecloud.connect(DB_URL)

@app.post("/query")
async def query_sql(request: Request):
    data = await request.json()
    sql = data.get("sql")
    if not sql:
        raise HTTPException(status_code=400, detail="No SQL provided")
    
    conn = get_connection()
    cursor = conn.execute(sql)
    columns = [description[0] for description in cursor.description]
    rows = cursor.fetchall()
    conn.close()

    formatted = [dict(zip(columns, row)) for row in rows]
    return {"success": True, "rows": formatted}

@app.post("/create_user")
async def create_user(payload: dict):
    username = payload.get("username")
    if not username:
        return {"status": "error", "message": "Username required"}

    conn = sqlitecloud.connect(DB_URL)
    cursor = conn.cursor()

    # ✅ 1. Check if user already exists
    cursor.execute("SELECT 1 FROM play_character_user WHERE username = ?", (username,))
    exists = cursor.fetchone()

    if exists:
        conn.close()
        return {"status": "ok", "message": "User already exists"}

    # ✅ 2. Otherwise clone from play_character
    cursor.execute("""
        INSERT INTO play_character_user (play_code, character_nr, character_full_name, character_short_name, character_description, is_a_group, is_in_group, is_user, voice, text_color, voice_pace, username)
        SELECT play_code, character_nr, character_full_name, character_short_name, character_description, is_a_group, is_in_group, is_user, voice, text_color, voice_pace, ?
        FROM play_character
    """, (username,))

    conn.commit()
    conn.close()

    return {"status": "ok", "message": "User created"}

# ✅ Update selection when checkbox toggled
@app.post("/update_selection")
async def update_selection(request: Request):
    data = await request.json()
    username = data.get("username")
    character_name = data.get("character_full_name")
    is_user = data.get("is_user")

    if not username or not character_name:
        raise HTTPException(status_code=400, detail="Username and character name are required")

    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(f"""
        UPDATE play_character_user
        SET is_user = {1 if is_user else 0}
        WHERE username = '{username}'
        AND character_full_name = '{character_name}'
    """)
    conn.commit()
    conn.close()

    return {"success": True, "message": "Update successful"}
