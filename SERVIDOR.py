from flask import Flask, jsonify
from prova import main
from prova import stop

app = Flask(__name__) # Crear instancia de la aplicación Flask

@app.route("/") #El endpoint “/” muestra este mensaje
def home():
    return "API funcionando"

@app.route("/run_main", methods=["POST"]) #Endpoint “/run_main” que ejecuta main()
def run_main():
    main() #Llama al método “main”
    return jsonify({"status": "finished"}) #Lo devuelve al finalizar

@app.route("/run_stop", methods=["POST"]) #Endpoint “/run_stop” que ejecuta stop()
def run_stop():
    stop() #Llama al método “stop”
    return jsonify({"status": "finished"}) #Lo devuelve al finalizar   

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False) #IP y puerto donde corre la app