#Se importa las librerias a utilizar
from ast import Try
import functools
from threading import Thread
import time
import requests
import json
from tcping import Ping

#constantes
IP_HISTORIAN="192.168.200.111"
PUERTO_HISTORIAN="5050"
HISTORIAN_TAG_URL="http://"+ IP_HISTORIAN+ ":"+PUERTO_HISTORIAN+"/ver-tags/"
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
    url = HISTORIAN_TAG_URL+id_tag
    headers = {'user-agent': 'my-app/0.0.1'}
    counter = 0
    #Este 1920 es simplemente las veces que va a ejecutar este bucle +1 
    #se podria modificar para que pasado estas veces vuelva a iniciar
    #Ahora solo funciona por un turno de 8 horas
    while counter < 1920:
        #Asumimos que existe error al principio
        existeError=False
        # Ping(host, port, timeout)
        ping = Ping(IP_HISTORIAN, PUERTO_HISTORIAN, 5)
        try:
            ping.ping(1)
        except:
            print("Error de conexion a Historian ", IP_HISTORIAN)
            existeError=True
        if existeError == False:
            #Iniciamos el hilo para la solicitud del API historian
            req = hilo=Thread(target=functools.partial(mifuncion, url, headers))
            req.start()
        counter+=1
        #el numero dentro de sleep es el tiempo que espera
        time.sleep(10)

