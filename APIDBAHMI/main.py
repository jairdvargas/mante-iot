from flask import Flask, request, jsonify
from flask_cors import CORS
from cliente_sqlite import devolver_tag_historizados, leer_valores_PDB,leer_historicos_PDB, leer_historicos, SQLITE_ARCHIVO
import json

app = Flask(__name__)
# aqui se habilita cors
CORS(app)

@app.route("/leervaloresPDB", methods=["GET"])
def leervaloresPDB():
    if request.method == "GET":
        # leer tags de la base de datos
        valoresInstantaneos = leer_valores_PDB(SQLITE_ARCHIVO)
        # la funcion find retorna "cursor" y se tiene que convertir a json con jsonify
        print(valoresInstantaneos)
        return jsonify(valoresInstantaneos)
#[
#    {
#        "calidad": "GOOD",
#        "descripcion": "flujo de algo",
#        "egu_max": "1000",
#        "egu_min": "0",
#        "egu_unidad": "Kg/h",
#        "fechalectura": "16-04-2022 02:26:27",
#        "id": 4,
#        "idhistorian": 0,
#        "nombre": "DESKTOP-3PEVOMB.Tan",
#        "tiemposcan": 10,
#        "tipo": "AI",
#        "valor": "900.0"
#    }
#]

@app.route("/leerhistoricosPDB", methods=["GET"])
def leerhistoricosPDB():
    if request.method == "GET":
        #Leemos cuales tags estan siendo historizados o no desde la base de datos
        TagsHistorizados=devolver_tag_historizados(SQLITE_ARCHIVO)
        #Lista donde se alarmacenara en cada indice un valor true o false segun tenga o no tenga historicos
        listaHist=[]
        hist_i=0
        while hist_i < len(TagsHistorizados):
            if TagsHistorizados[hist_i]:
                valoreshistoricos = leer_historicos(SQLITE_ARCHIVO, hist_i)
                #NOTA: Primero llega una <list> con un elemento que adentro tiene un solo <tuple> y su unico elemento es un <str>
                estuple=valoreshistoricos[0]
                esStr=estuple[0]
                listaHist.append(esStr)
            hist_i+=1
        #print("----------")
        #Se arma un json de cada una de las respuesta de los tags que si estan siendo historizados
        return jsonify([hist for hist in listaHist])

        
if __name__ == "__main__":
    app.run("0.0.0.0", port=5051)