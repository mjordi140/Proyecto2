import oracledb


def conectar(usuario, password):
    try:
        conexion = oracledb.connect(
            user=usuario,
            password=password,
            dsn="oralabos.dsic.upv.es/labora.dsic.upv.es"
        )
        print("Conectado con éxito")
        return conexion
    except Exception as e:
        print("Error al conectar:", e)
        return None


def insertar_log(conexion, instruccion, elemento):
    try:
        cursor = conexion.cursor()
        sql = """
        INSERT INTO log (instruccion, elemento)
        VALUES (:1, :2)
        """
        cursor.execute(sql, [instruccion, elemento])
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al insertar log:", e)


def obtener_logs(conexion, elemento=None):
    try:
        cursor = conexion.cursor()

        if elemento:
            sql = """
            SELECT fecha, elemento, instruccion
            FROM log
            WHERE LOWER(elemento) = LOWER(:1)
            ORDER BY fecha DESC
            """
            cursor.execute(sql, [elemento])
        else:
            sql = """
            SELECT fecha, elemento, instruccion
            FROM log
            ORDER BY fecha DESC
            """
            cursor.execute(sql)

        resultados = cursor.fetchall()
        cursor.close()

        return resultados

    except Exception as e:
        print("Error al consultar logs:", e)
        return []


def borrar_logs(conexion):
    try:
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM log")
        conexion.commit()
        cursor.close()
    except Exception as e:
        print("Error al borrar logs:", e)


def desconectar(conexion):
    if conexion:
        conexion.close()