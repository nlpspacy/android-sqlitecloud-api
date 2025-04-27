from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlitecloud
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = "sqlitecloud://cgdjyovjhk.g2.sqlite.cloud:8860/play_navigation.db?apikey=SFR0f2mYTxb3bbOiaALxEyatvEt2WDn5hYygAXiuE2o"

@app.post("/create_user")
async def create_user(request: Request):
    data = await request.json()
    username = data.get("username")

    if not username:
        return {"success": False, "message": "Username required"}

    conn = sqlitecloud.connect(DB_URL)
    cursor = conn.cursor()

    try:
        # Check if username already exists
        check_sql = "SELECT 1 FROM play_character_user WHERE username = ? LIMIT 1;"
        cursor.execute(check_sql, (username,))
        result = cursor.fetchone()

        if result:
            return {"success": False, "message": "Username already exists"}

        # Clone play_character into play_character_user for new user
        insert_sql = """
            INSERT INTO play_character_user (play_code, character_nr, character_full_name, character_short_name, character_description, is_a_group, username, is_user)
            SELECT play_code, character_nr, character_full_name, character_short_name, character_description, is_a_group, ?, 0
            FROM play_character;
        """
        cursor.execute(insert_sql, (username,))
        conn.commit()

        return {"success": True, "message": "User created successfully"}

    except Exception as e:
        return {"success": False, "message": str(e)}

    finally:
        conn.close()
