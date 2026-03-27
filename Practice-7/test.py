import psycopg2

conn = psycopg2.connect(
    host="localhost",
    dbname="phonebook_db",
    user="torekhan.danial",
    password="",
    port="5432"
)

print("Connected successfully!")
conn.close()