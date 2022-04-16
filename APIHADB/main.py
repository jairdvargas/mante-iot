#Se importa las librerias a utilizar
from ast import And, Try
import functools
from threading import Thread
import time
import requests
import json
from tcping import Ping
from cliente_sqlite import seleccionar_servidor
from cliente_sqlite import cliente_sqlite

#constantes
TAGSIM="DESKTOP-3PEVOMB.Ramp"

#Funcion para poder solicitar al API del servidor Historian creado previamente
#Esta funcion recibira dos parametros:
def mifuncion(par_url, par_head):
    respuesta = requests.get(par_url, headers=par_head)
    dataHIST = respuesta.json()
    print(dataHIST)
	

if __name__== '__main__':
    #En aqui se configura la url del API del servidor historian
    id_tag = TAGSIM
    url="http://"
    historian_IP="0.0.0.0"
    historian_PORT=0
    #recuperamos la IP del servidor Historian desde la DB
    with cliente_sqlite:
        servidor=seleccionar_servidor(cliente_sqlite)
        historian_IP=servidor[0][2]
        historian_PORT=servidor[0][3]
        url = "http://" + historian_IP + ":" + str(historian_PORT) + "/ver-tags/" + id_tag
    headers = {'user-agent': 'my-app/0.0.1'}
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
            #Iniciamos el hilo para la solicitud del API historian
            req = hilo=Thread(target=functools.partial(mifuncion, url, headers))
            req.start()
        counter+=1
        #el numero dentro de sleep es el tiempo que espera
        time.sleep(10)

