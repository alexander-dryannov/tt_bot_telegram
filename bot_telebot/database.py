from datetime import datetime
from uuid import uuid4
from os import getenv
import psycopg2


# Запись в базу данных.
def write_to_database(data):
    try:
        con = psycopg2.connect(f"dbname={getenv('DATABASE')} host={getenv('HOST')} port={getenv('PORT')} "
                               f"user={getenv('USER')} password={getenv('PASSWORD')}")
    except psycopg2.OperationalError:
        with open('err.log', 'a') as f:
            f.write(
                f"[Error] [{datetime.now()}] Ошибка подключения к базе данных. "
                f"Проверьте правильность введеных данных.\n"
            )
    cur = con.cursor()
    cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('pizza_bot_customer',))
    if cur.fetchone()[0] is False:
        cur.execute("CREATE TABLE pizza_bot_customer (id varchar PRIMARY KEY, date timestamp, messenger varchar, "
                    "size varchar, payment varchar, confirm bool);")
        con.commit()
    cur.execute("INSERT INTO pizza_bot_customer (id, date, messenger, size, payment, confirm) "
                "VALUES (%s, %s, %s, %s, %s, %s)", (uuid4().hex, data['date'], data['messenger'],
                                                    data['size'], data['payment'], data['confirm'])
                )
    con.commit()
    con.close()
