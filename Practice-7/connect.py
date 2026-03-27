import psycopg2
from config import host, dbname, user, password, port

def connect():
    return psycopg2.connect(
        host=host,
        dbname=dbname,
        user=user,
        password=password,
        port=port
    )