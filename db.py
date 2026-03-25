import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import Error

load_dotenv()

def get_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        return conn
    except Error as e:
        print(f"Ошибка подключения к БД: {e}")
        return None
    
def login_user(username: str, password: str):
    conn = get_connection()
    if not conn:
        return None, "Ошибка подключения к БД"
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                        SELECT "ID", username, password
                        FROM users
                        WHERE username = %s""", (username,))
            
            user = cur.fetchone()

            if not user:
                return None, "Вы ввели неверный логин или пароль. Пожалуйста проверьте еще раз введенные данные."
            
            user_id, username_db, stored_password = user

            if stored_password == password:
                print("Пароли совпали")
                return (user_id, username_db, None, None, "users"), None
            elif password != password:
                return None, "Вы ввели неверный логин или пароль. Пожалуйста проверьте еще раз введенные данные."

    except Exception as e: 
        print(f"[ОШИБКА в login_user] {type(e).__name__}: {e}")
        return None, f"Ошибка базы данных: {str(e)}"
    finally:
        if conn:
            conn.close()