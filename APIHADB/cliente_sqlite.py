import sqlite3
from sqlite3 import Error

SQLITE_ARCHIVO=r"../Processdata/manteDB.sqlite3"
SQLITE_TABLA_SERVIDOR="Servidor"
SQLITE_TABLA_PDB="PDB"
SQLITE_TABLA_HIST="HistData"

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

def seleccionar_tag(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+SQLITE_TABLA_PDB)
    tags = cur.fetchall()
    return tags

def seleccionar_hist(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + SQLITE_TABLA_HIST)
    hists = cur.fetchall()
    return hists

def actualizar_valor(conn, tagyvalor):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE PDB
              SET valor = ?,
                  fechalectura = ?
              WHERE id = ?'''
    
    cur = conn.cursor()
    cur.execute(sql,tagyvalor)
    conn.commit()
def actualizar_hist(conn, tagyvalor):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE HistData
              SET data = ?
              WHERE id = ?'''
    
    cur = conn.cursor()
    cur.execute(sql,tagyvalor)
    conn.commit()

cliente_sqlite= crear_conexion(SQLITE_ARCHIVO)

def leerServidor():
    # create a database connection
    with cliente_sqlite:
        servidores=seleccionar_servidor(cliente_sqlite)
        print(servidores[0][2])
        for servidor in servidores:
            print(servidor)
def leerTag():
     # create a database connection
    with cliente_sqlite:
        tags=seleccionar_tag(cliente_sqlite)
        #nombre de tag
        print(tags[0][1])
        #id de historian
        print(tags[0][4])
        #scan en segundos
        print(tags[0][5])
        for tag in tags:
            print(tag)
def escribeValor():
    with cliente_sqlite:
        algo=actualizar_valor(cliente_sqlite,(888,0))


if __name__ == '__main__':
    #leerServidor()
    #leerTag()
    escribeValor()