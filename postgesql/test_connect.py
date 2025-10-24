from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import os

load_dotenv()
password = os.getenv('POSTGREPASS')


conn = psycopg2.connect(
    host="localhost",
    database="postgres",  
    user="postgres",
    password=password  
)
conn.autocommit = True  
cursor = conn.cursor()


db_name = "my_blog"
try:
    cursor.execute(sql.SQL("CREATE DATABASE {}").format(
        sql.Identifier(db_name))
    )
    print(f"База данных '{db_name}' успешно создана!")
except psycopg2.Error as e:
    print(f"Ошибка при создании базы данных: {e}")
finally:
    cursor.close()
    conn.close()