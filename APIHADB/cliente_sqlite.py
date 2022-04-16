import sqlite3
from sqlite3 import Error

SQLITE_ARCHIVO=r"../Processdata/manteDB.sqlite3"
SQLITE_TABLA_SERVIDOR="Servidor"

def crear_conexion(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def seleccionar_servidor(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+SQLITE_TABLA_SERVIDOR)
    rows = cur.fetchall()

    return rows

cliente_sqlite= crear_conexion(SQLITE_ARCHIVO)

def leerServidor():
    # create a database connection
    with cliente_sqlite:
        servidores=seleccionar_servidor(cliente_sqlite)
        print(servidores[0][2])
        for servidor in servidores:
            print(servidor)



if __name__ == '__main__':
    leerServidor()