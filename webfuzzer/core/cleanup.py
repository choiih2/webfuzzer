# core/cleanup.py
import pymysql
from core.config import DB_CONFIG

def db_connect():
    return pymysql.connect(
        host=DB_CONFIG["host"],
        port=DB_CONFIG["port"],
        user=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        db=DB_CONFIG["db"],
        charset=DB_CONFIG["charset"],
        autocommit=DB_CONFIG["autocommit"]
    )

def get_last_post_id():
    conn = db_connect()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT IFNULL(MAX(id), 0) FROM posts")
            maxid = cur.fetchone()[0]
    finally:
        conn.close()
    return maxid

def delete_new_posts_after(base_id):
    conn = db_connect()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM posts WHERE id > %s", (base_id,))
            deleted = cur.rowcount
    finally:
        conn.close()
    print(f"[CLEANUP] Deleted {deleted} fuzz-generated posts.")
