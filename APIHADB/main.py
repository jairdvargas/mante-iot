#Se importa las librerias a utilizar
from ast import And, Try
import functools
from threading import Thread
import time
from xmlrpc.client import SafeTransport
import requests
import json
from tcping import Ping
from cliente_sqlite import actualizar_hist, seleccionar_servidor, seleccionar_tag, seleccionar_hist, actualizar_valor, crear_conexion
from cliente_sqlite import cliente_sqlite, SQLITE_ARCHIVO


#Funcion para poder solicitar al API del servidor Historian creado previamente
#Esta funcion recibira dos parametros:
def mifuncion(par_url, par_head,idtag,hist_url):
    respuesta = requests.get(par_url, headers=par_head)
    dataHIST = respuesta.json()
    #se ecribe a la DB el valor que corresponde seguido de la id de la variable
    hiloRespuestaaSQL = crear_conexion(SQLITE_ARCHIVO)
    actualiza= actualizar_valor(hiloRespuestaaSQL,(dataHIST["valor"],dataHIST["tiempo"],idtag))
    #solicita informacion de historico si corresponde
    if hist_url!="":
        #hiloRespuestaaSQL = crear_conexion(SQLITE_ARCHIVO)
        print("Solicitando historco...")
        histrespuesta = requests.get(hist_url, headers=par_head)
        Historicos = histrespuesta.json()
        jsonEnTexto=json.dumps(Historicos,separators=(',', ':'))
        historiza= actualizar_hist(hiloRespuestaaSQL,(jsonEnTexto,idtag))
        print(jsonEnTexto)
    #print(dataHIST)
	

if __name__== '__main__':
    #En aqui se configura la url del API del servidor historian
    url="http://"
    historian_IP=""
    historian_PORT=0
    ####Esta variable se utiliza para almacenar el nombre de lso tags de la base de datos
    variables=[]
    #Esta variable es para saber si tiene o no historico
    historicos=[]
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
        #leemos config historica de los tags en base de datos
        hist=seleccionar_hist(cliente_sqlite)
        #tamano de tags encontrados
        #print(len(tag))
        #Se van agregando a una lista los tags recuperados de la base de datos
        #Aqui faltaria discriminar los tags que no estan siendo monitoreados
        for varhist in tag:
            #("id","nombre","tipo","descripcion","idhistorian","tiemposcan","valor","fechalectura","calidad","egu_min","egu_max", "egu_unidad", verhistoricos)
            #(0, 'DESKTOP-3PEVOMB.Ramp', 'AI', 'Flujo 1', 0, 10, '400.0', '20-04-2022 08:50:12', 'GOOD', '0', '1000', 'Kg/h',0)
            #Si el tag esta en modo monitoreo se agrega a la lista, Si el tag su tiempo de scan es cero, se deja un espacio vacio en su lugar de monitoreo, asi no se scaneara ese tag
            variables.append(varhist[1]) if varhist[5] > 0 else variables.append("")
            #Para ver si se lee o no historico
            if varhist[12] ==1:
                historicos.append(True)
            else:
                historicos.append(False)
    
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
                #Verificamos si existe una variable en la lista de tags a monitorear,si encontramos un tag a monitorear desactivamos el modo de scaneo
                if variables[j]== "":
                    j+=1
                else:
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
                #Preguntar si se lee historicos o no
                if historicos[var_index]:
                    leehistorico=True
                    histconfig=hist[var_index]
                    #(0, 260, '10m', 'Now-2h', 'Now', '0')
                    urlhist="http://" + historian_IP + ":" + str(historian_PORT) + "/ver-historico?nombre=" + variables[var_index]
                    urlhist=urlhist+"&npuntos="+ str(histconfig[1])
                    urlhist=urlhist+"&intervalo="+ histconfig[2]
                    urlhist=urlhist+"&fechainicio="+ histconfig[3]
                    urlhist=urlhist+"&fechafin="+ histconfig[4]
                else:
                    leehistorico=False
                    urlhist=""
                #Iniciamos el hilo para la solicitud del API historian
                req = hilo=Thread(target=functools.partial(mifuncion, url, headers,var_index,urlhist))
                req.start()
        counter+=1
        #Aumentamos el siguiente indice de busqueda
        var_index+=1
        #En caso de llegar al final de la lista de tags, volvemos al principio.
        if var_index >= len(variables):
            var_index=0
        #el numero dentro de sleep es el tiempo que espera
        if leehistorico:
            time.sleep(10)
        else:
            time.sleep(4)

