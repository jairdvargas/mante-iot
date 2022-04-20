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
    #se ecribe a la DB el valor que corresponde seguido de la id de la variable
    hiloRespuestaaSQL = crear_conexion(SQLITE_ARCHIVO)
    actualiza= actualizar_valor(hiloRespuestaaSQL,(dataHIST["valor"],dataHIST["tiempo"],idtag))
    print(dataHIST)
	

if __name__== '__main__':
    #En aqui se configura la url del API del servidor historian
    url="http://"
    historian_IP=""
    historian_PORT=0
    ####Esta variable se utiliza para almacenar el nombre de lso tags de la base de datos
    variables=[]
    ##Este es el indice de tag actual de la lista de tags de la base de datos
    var_index=0
    ####
    #recuperamos la IP del servidor Historian desde la DB y lista de tags
    with cliente_sqlite:
        #Se lee servidor historian configurado de la base de datos
        servidor=seleccionar_servidor(cliente_sqlite)
        #Se lee la ip y puerto
        historian_IP=servidor[0][2]
        historian_PORT=servidor[0][3]
        #leemos todos los tags de la base de datos
        tag=seleccionar_tag(cliente_sqlite)
        #tamano de tags encontrados
        #print(len(tag))
        #Se van agregando a una lista los tags recuperados de la base de datos
        #Aqui faltaria discriminar los tags que no estan siendo monitoreados
        for varhist in tag:
            #("id","nombre","tipo","descripcion","idhistorian","tiemposcan","valor","fechalectura","calidad","egu_min","egu_max", "egu_unidad")
            #(0, 'DESKTOP-3PEVOMB.Ramp', 'AI', 'Flujo 1', 0, 10, '400.0', '20-04-2022 08:50:12', 'GOOD', '0', '1000', 'Kg/h')
            if varhist[5] > 0:
                #Si el tag esta en modo monitoreo se agrega a la lista
                variables.append(varhist[1])
            else:
                #Si el tag su tiempo de scan es cero, se deja un espacio vacio en su lugar de monitoreo, asi no se scaneara ese tag
                variables.append("")

    
    #Este 1920 es simplemente las veces que va a ejecutar este bucle +1 
    #se podria modificar para que pasado estas veces vuelva a iniciar
    #Ahora solo funciona por un turno de 8 horas
    counter = 0
    while counter < 1920:
        #Asumimos que existe error al principio
        existeError=False
        # Ping(host, port, timeout) esto sirve para saber si esta online el servidor historian
        ping = Ping(historian_IP, historian_PORT, 5)
        try:
            #Se prueba hacer el ping una vez
            ping.ping(1)
        except:
            print("Error de conexion a Historian ", historian_IP)
            existeError=True
        if existeError == False and historian_PORT!=0:
            #Verificamos si el tag sera monitoreado o no para saltar al siguiente
            j=var_index
            scanning=True
            #Pone en modo scan de tags para monitorear mientras se cumplan las condiciones
            while scanning and j<len(variables):
                #Verificamos si existe una variable en la lista de tags a monitorear
                if variables[j]== "":
                        j+=1
                else:
                        #Si encontramos un tag a monitorear desactivamos el modo de scaneo
                        #print("Encontro indice bueno en ",j)
                        scanning=False
            #Esto sirve para que en caso de que se llego al final de la busqueda, vuelva al principio para volver a buscar el siguiente ciclo
            if j>=len(variables):
                var_index=0
            else:
                var_index=j
            #Solo va a enviar una solicitud al servidor historian si es que se encontro un tag a monitorear en este ciclo
            if variables[var_index] != "":
                #Configuramos la url del endpoint ccorrecto
                #Notar que utilizando var_index con cada instancia se va a ir leyendo progresivamente cada tag.
                #Internvamente en la funcion mifuncion cada vez que lee el tag se actualizara en la DB
                url = "http://" + historian_IP + ":" + str(historian_PORT) + "/ver-tags/" + variables[var_index]
                headers = {'user-agent': 'my-app/0.0.1'}
                #Iniciamos el hilo para la solicitud del API historian
                req = hilo=Thread(target=functools.partial(mifuncion, url, headers,var_index))
                req.start()
        counter+=1
        #Aumentamos el siguiente indice de busqueda
        var_index+=1
        #En caso de llegar al final de la lista de tags, volvemos al principio.
        if var_index >= len(variables):
            var_index=0
        #el numero dentro de sleep es el tiempo que espera
        time.sleep(5)

