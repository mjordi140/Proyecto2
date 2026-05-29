import csv
import os
import threading
from datetime import datetime
from flask import Flask, jsonify, request
from flask_cors import CORS
import bd
import robot as rb

app = Flask(__name__)
CORS(app)

robot_lock = threading.Lock()

# ================= CONEXIÓN BD =================
conexion_bd = bd.conectar("TVERGUT", "tu_password")

# ================= CSV =================
CSV_PATH = "logs.csv"

def insertar_csv(mensaje, tipo):
    try:
        file_exists = os.path.exists(CSV_PATH)
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["fecha+hora", "mensaje", "tipo"])
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), mensaje, tipo])
    except Exception as e:
        print(f"Error escribiendo CSV: {e}")

def registrar(mensaje, tipo):
    bd.insertar_log(conexion_bd, mensaje, tipo)
    insertar_csv(mensaje, tipo)

# Conectar el logger de robot.py con el de Flask
rb.set_log_callback(registrar)

# ================= ESTADO GLOBAL =================
estado = {
    "running": False,
    "herramienta": "abierta",
    "velocidad_cinta": 0,
    "cinta": "parada",
    "sensor": False,
    "ip_robot": "172.16.190.28"
}

# ================= ROBOT =================
# ID de la cinta para uso manual (fuera del modo automático)
_conveyor_id_manual = None

def ejecutar_automatico():
    rb.Pickandplace(0)

def parar_robot():
    rb.stop()

def ir_home():
    rb.robot.move_pose(rb.POS_INICIAL)

def mover_pose(x, y, z, roll, pitch, yaw):
    rb.move_to_position(x, y, z, roll, pitch, yaw)

def mover_joints(j1, j2, j3, j4, j5, j6):
    rb.robot.move_joints(j1, j2, j3, j4, j5, j6)

def encender_cinta(velocidad):
    global _conveyor_id_manual
    if _conveyor_id_manual is None:
        _conveyor_id_manual = rb.robot.set_conveyor()
    rb.robot.run_conveyor(_conveyor_id_manual, speed=velocidad, direction=rb.ConveyorDirection.FORWARD)

def parar_cinta():
    global _conveyor_id_manual
    if _conveyor_id_manual is not None:
        rb.robot.stop_conveyor(_conveyor_id_manual)

def abrir_herramienta():
    rb.robot.open_gripper(speed=400)

def cerrar_herramienta():
    rb.robot.close_gripper(speed=400)

def get_posicion():
    return rb.get_posicion_robot()

def leer_sensor():
    return rb.robot.digital_read(rb.PIN_SENSOR_PIEZA_PEQUENYA) == rb.PinState.LOW


# ================= AUTOMÁTICO =================
@app.route("/run_main", methods=["POST"])
def run_main():
    def task():
        with robot_lock:
            estado["running"] = True
            registrar("Inicio modo automático", "robot")
            ejecutar_automatico()
            estado["running"] = False
            registrar("Fin modo automático", "robot")

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


@app.route("/stop", methods=["POST"])
def stop():
    def task():
        with robot_lock:
            parar_robot()
            estado["running"] = False
            registrar("Robot parado", "robot")

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= HOME =================
@app.route("/home", methods=["POST"])
def move_home():
    def task():
        with robot_lock:
            ir_home()
            registrar("Robot movido a home", "robot")

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= CINTA =================
@app.route("/cinta", methods=["POST"])
def cinta():
    data = request.json
    estado_cinta = data.get("estado")
    velocidad = data.get("velocidad", 50)

    def task():
        with robot_lock:
            if estado_cinta == "on":
                encender_cinta(velocidad)
                estado["cinta"] = "marcha"
                estado["velocidad_cinta"] = velocidad
                registrar(f"Cinta encendida al {velocidad}%", "cinta")
            else:
                parar_cinta()
                estado["cinta"] = "parada"
                estado["velocidad_cinta"] = 0
                registrar("Cinta parada", "cinta")

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= HERRAMIENTA =================
@app.route("/tool", methods=["POST"])
def tool():
    data = request.json
    accion = data.get("accion")

    def task():
        with robot_lock:
            if accion == "open":
                abrir_herramienta()
                estado["herramienta"] = "abierta"
                registrar("Herramienta abierta", "herramienta")
            else:
                cerrar_herramienta()
                estado["herramienta"] = "cerrada"
                registrar("Herramienta cerrada", "herramienta")

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= SENSOR =================
@app.route("/sensor", methods=["GET"])
def sensor():
    try:
        detectado = leer_sensor()
        estado_anterior = estado["sensor"]

        if detectado != estado_anterior:
            estado["sensor"] = detectado
            msg = "Objeto detectado" if detectado else "Sin detección"
            registrar(msg, "sensor")

        return jsonify({"detectado": detectado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= DASHBOARD =================
@app.route("/estado", methods=["GET"])
def get_estado():
    return jsonify({"running": estado["running"]})


@app.route("/herramienta", methods=["GET"])
def get_herramienta():
    return jsonify({"herramienta": estado["herramienta"]})


@app.route("/paletizadas", methods=["GET"])
def paletizadas():
    try:
        piezas = rb.get_paletizadas()
        return jsonify({"piezas": piezas})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/posicion", methods=["GET"])
def posicion():
    try:
        pos = get_posicion()
        return jsonify({
            "x":     round(pos[0], 4),
            "y":     round(pos[1], 4),
            "z":     round(pos[2], 4),
            "roll":  round(pos[3], 4),
            "pitch": round(pos[4], 4),
            "yaw":   round(pos[5], 4)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ================= MOVER POR POSICIÓN =================
@app.route("/move", methods=["POST"])
def move():
    data = request.json
    x     = data.get("x", 0)
    y     = data.get("y", 0)
    z     = data.get("z", 0)
    roll  = data.get("roll", 0)
    pitch = data.get("pitch", 0)
    yaw   = data.get("yaw", 0)

    def task():
        with robot_lock:
            mover_pose(x, y, z, roll, pitch, yaw)
            registrar(
                f"Move pose x={x} y={y} z={z} roll={roll} pitch={pitch} yaw={yaw}",
                "robot"
            )

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= MOVER POR JOINTS =================
@app.route("/move_joints", methods=["POST"])
def move_joints():
    data = request.json
    j1 = data.get("joint1", 0)
    j2 = data.get("joint2", 0)
    j3 = data.get("joint3", 0)
    j4 = data.get("joint4", 0)
    j5 = data.get("joint5", 0)
    j6 = data.get("joint6", 0)

    def task():
        with robot_lock:
            mover_joints(j1, j2, j3, j4, j5, j6)
            registrar(
                f"Move joints j1={j1} j2={j2} j3={j3} j4={j4} j5={j5} j6={j6}",
                "robot"
            )

    threading.Thread(target=task, daemon=True).start()
    return jsonify({"status": "ok"})


# ================= LOGS =================
@app.route("/log", methods=["GET"])
def ver_logs():
    elemento = request.args.get("elemento") or None

    logs = bd.obtener_logs(conexion_bd, elemento)

    html = """
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Logs</title>
        <style>
            body { font-family: Arial, sans-serif; padding: 20px; }
            h2 { margin-bottom: 10px; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }
            th { background-color: #f0f0f0; }
            tr:nth-child(even) { background-color: #f9f9f9; }
        </style>
    </head>
    <body>
        <h2>Logs del sistema</h2>
        <table>
            <tr>
                <th>Fecha</th>
                <th>Elemento</th>
                <th>Instrucción</th>
            </tr>
    """

    for log in logs:
        html += f"<tr><td>{log[0]}</td><td>{log[1]}</td><td>{log[2]}</td></tr>"

    html += """
        </table>
    </body>
    </html>
    """

    return html


# ================= CONFIGURACIÓN =================
@app.route("/config", methods=["POST"])
def config():
    data = request.json
    ip_robot = data.get("ip_robot")

    if ip_robot:
        estado["ip_robot"] = ip_robot
        registrar(f"IP robot actualizada a {ip_robot}", "robot")

    return jsonify({"status": "ok", "ip_robot": estado["ip_robot"]})


# ================= MAIN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)