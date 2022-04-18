from flask import Flask, request, jsonify
from flask_cors import CORS
from cliente_sqlite import leer_valores_PDB, SQLITE_ARCHIVO

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

if __name__ == "__main__":
    app.run("0.0.0.0", port=5051)