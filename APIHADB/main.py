#Se importa las librerias a utilizar
from ast import And, Try
import functools
from threading import Thread
import time
import requests
import json
from tcping import Ping
from cliente_sqlite import seleccionar_servidor, seleccionar_tag, actualizar_valor, crear_conexion
from cliente_sqlite import cliente_sqlite, SQLITE_ARCHIVO


#Funcion para poder solicitar al API del servidor Historian creado previamente
#Esta funcion recibira dos parametros:
def mifuncion(par_url, par_head,idtag):
    respuesta = requests.get(par_url, headers=par_head)
    dataHIST = respuesta.json()
    #secribe el valor que corresponde seguido de la id de la variable
    hiloRespuestaaSQL = crear_conexion(SQLITE_ARCHIVO)
    actualiza= actualizar_valor(hiloRespuestaaSQL,(dataHIST["valor"],dataHIST["tiempo"],idtag))
    print(dataHIST)
	

if __name__== '__main__':
    #En aqui se configura la url del API del servidor historian
    url="http://"
    historian_IP=""
    historian_PORT=0
    #####
    variables=[]
    var_index=0
    ####
    #recuperamos la IP del servidor Historian desde la DB
    with cliente_sqlite:
        servidor=seleccionar_servidor(cliente_sqlite)
        historian_IP=servidor[0][2]
        historian_PORT=servidor[0][3]
        tag=seleccionar_tag(cliente_sqlite)
        #tamano de tags encontrados
        #print(len(tag))
        for varhist in tag:
            variables.append(varhist[1])

    counter = 0
    #Este 1920 es simplemente las veces que va a ejecutar este bucle +1 
    #se podria modificar para que pasado estas veces vuelva a iniciar
    #Ahora solo funciona por un turno de 8 horas
    while counter < 1920:
        #Asumimos que existe error al principio
        existeError=False
        # Ping(host, port, timeout)
        ping = Ping(historian_IP, historian_PORT, 5)
        try:
            ping.ping(1)
        except:
            print("Error de conexion a Historian ", historian_IP)
            existeError=True
        if existeError == False and historian_PORT!=0:
            #Configuramos la url correcta
            url = "http://" + historian_IP + ":" + str(historian_PORT) + "/ver-tags/" + variables[var_index]
            headers = {'user-agent': 'my-app/0.0.1'}
            #Iniciamos el hilo para la solicitud del API historian
            req = hilo=Thread(target=functools.partial(mifuncion, url, headers,var_index))
            req.start()
        counter+=1
        var_index+=1
        if var_index >= len(variables):
            var_index=0
        #el numero dentro de sleep es el tiempo que espera
        time.sleep(4)

