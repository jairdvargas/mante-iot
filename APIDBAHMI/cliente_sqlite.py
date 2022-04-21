from ast import Try
import sqlite3
from sqlite3 import Error

SQLITE_ARCHIVO=r"../Processdata/manteDB.sqlite3"
SQLITE_TABLA_SERVIDOR="Servidor"
SQLITE_TABLA_PDB="PDB"

def seleccionar_tag(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+SQLITE_TABLA_PDB)
    tags = cur.fetchall()
    return tags
    
def leer_valores_PDB(PDB):
    conn = None
    try:
        conn = sqlite3.connect(PDB)
    except Error as e:
        print(e)

    with conn:
        #---- Se va a recuperar los valores de todos los tags y filtrar si estan o no en scan, nos interesa solo los que estan en modo tiemposcan > 0
        #Iniciamos una lista vacia
        tags_en_scan=[]
        #Se lees todos los tags de la PDB
        tagslist=seleccionar_tag(conn)
        #Se analiza cada tag de la PDB devuelto
        for tag in tagslist:
            #Se analiza el valor cada propiedad del tag en ese instante tag
            #print("Variable en scan ", tag[1]) if int(tag[5]) > 0 else print("Variable no en scan ", tag[1])
            tags_en_scan.append(tag) if int(tag[5]) > 0 else print("Variable no se escaneará ", tag[1])
        #---- Se recupera los nombres de las propiedades de los valores previamente obtenidos
        cur = conn.cursor()
        Estructura_PDB= [fields[1] for fields in cur.execute(f"PRAGMA table_info({SQLITE_TABLA_PDB})")]
        #-------Se va a formatea ambos datos que se obtuvieron
        #Se crea una lista vacia
        TagsYProps=[]
        #se forma el datos con la estructura y su dato correspondiente de manera independiente para poder enviar
        for tagscan in tags_en_scan:
            TagBienFormado= dict()
            TagBienFormado={Estructura_PDB[i]:tagscan[i] for i in range(len(Estructura_PDB))}
            TagsYProps.append(TagBienFormado)
        return(TagsYProps)

def leer_historicos_PDB(PDB):
    conn = None
    try:
        conn= sqlite3.connect(PDB)
    except Error as e:
        print(e)
    with conn:
        sql = ''' SELECT data
              FROM HistData
              WHERE id = 0'''
        cur = conn.cursor()
        cur.execute(sql)
        tags = cur.fetchall()
        return tags

if __name__ == '__main__':
    #leerServidor()
    #leerTag()
    #escribeValor()
    print(leer_valores_PDB())