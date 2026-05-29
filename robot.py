#!/usr/bin/env python3
from pyniryo import NiryoRobot, ConveyorDirection, PinID, PoseObject, PinState

IP_ROBOT = "172.16.190.28"
robot = NiryoRobot(IP_ROBOT)

PIN_SENSOR_PIEZA_PEQUENYA = PinID.DI5
PIN_SENSOR_PIEZA_GRANDE  = PinID.DI1

META_PIEZAS_PEQUENYAS = 3

#0.2438,-0.0055,0.3474,-0.0779,0.6068,-0.0524
POS_INICIAL = PoseObject(x=0.2438, y=-0.0055, z=0.3474, roll=-0.0779, pitch=0.6068, yaw=-0.0524)

#0.2,-0.196,0.0878,3.0755,1.2281,3.1308
POS_COJER_PIEZA = PoseObject(x=0.2, y=-0.196, z=0.0878, roll=3.0755, pitch=1.2281, yaw=3.1308)
#0.1988,-0.1957,0.1529,-2.8363,1.4386,-2.9242
POS_PRE_COJER_PIEZA = PoseObject(x=0.1988, y=-0.1957, z=0.1529, roll=-2.8363, pitch=1.4386, yaw=-2.9242)

#0.2792,-0.2049,0.1188,1.0894,1.5394,1.0279
POS_PRE_DEJAR_CONVEYOR = PoseObject(x=0.2792, y=-0.2049, z=0.1188, roll=1.0894, pitch=1.5394, yaw=1.0279)
#0.2887,-0.2049,0.0757,0.1658,1.4893,0.1757
POS_DEJAR_CONVEYOR = PoseObject(x=0.2887, y=-0.2049, z=0.0757, roll=0.1658, pitch=1.4893, yaw=0.1757)

#0.2788,0.1758,0.0698,-1.3735,1.4922,-1.405
POS_RECOGER = PoseObject(x=0.2788, y=0.1758, z=0.0698, roll=-1.3735, pitch=1.4922, yaw=-1.405)
#0.2806,0.1764,0.1304,-0.4217,1.4018,-0.4012
POS_PRE_RECOGER = PoseObject(x=0.2806, y=0.1764, z=0.1304, roll=-0.4217, pitch=1.4018, yaw=-0.4012)

#0.0376,0.2095,0.1551,2.8083,1.4893,2.8565
POS_PRE_CENTRO = PoseObject(x=0.0376, y=0.2095, z=0.1551, roll=2.8083, pitch=1.4893, yaw=2.8565)
#0.0443,0.2049,0.0619,-2.4745,1.5295,-2.3983
POS_CENTRO = PoseObject(x=0.0443, y=0.2049, z=0.0619, roll=-2.4745, pitch=1.5295, yaw=-2.3983)

# ahora tengo qu eponer los offsets de las 6 piezas e intentar que si detecta una pieza pequeña la deje arriba de izquierda a derecha y si detecta una pieza grande la deje debajo de izquierda a derecha de la POS_CENTRO, es decir, la pieza pequeña 1 se dejará en la parte superior izquierda de la POS_CENTRO, la pieza pequeña 2 en la parte superior central y la pieza pequeña 3 en la parte superior derecha, mientras que la pieza grande 1 se dejará en la parte inferior izquierda de la POS_CENTRO.

offset_pequenyas = [
    PoseObject(x=0.0, y=0.05, z=0.0, roll=0, pitch=0, yaw=0),   # izquierda arriba
    PoseObject(x=0.0, y=0.0,  z=0.0, roll=0, pitch=0, yaw=0),   # centro arriba
    PoseObject(x=0.0, y=-0.05,z=0.0, roll=0, pitch=0, yaw=0)    # derecha arriba
]


def ejecutar_automatico():
    robot.Pickandplace(0)

def parar_robot():
    robot.stop()

def ir_home():
    robot.calibrate_auto()
    robot.update_tool()
    robot.move_pose(POS_INICIAL)

def mover_pose(x, y, z, roll, pitch, yaw):
    robot.calibrate_auto()
    robot.update_tool()
    robot.move_pose(x, y, z, roll, pitch, yaw)

def mover_joints(j1, j2, j3, j4, j5, j6):
    robot.calibrate_auto()
    robot.update_tool()
    robot.move_pose(j1, j2, j3, j4, j5, j6)

def encender_cinta(velocidad):
    conveyor_id = robot.set_conveyor()
    if conveyor_id is None:
        conveyor_id = robot.set_conveyor()
    robot.run_conveyor(conveyor_id, speed=velocidad, direction=robot.ConveyorDirection.FORWARD)

def parar_cinta():
    conveyor_id = robot.set_conveyor()
    if conveyor_id is not None:
        robot.stop_conveyor(conveyor_id)

def abrir_herramienta():
    robot.calibrate_auto()
    robot.update_tool()
    robot.open_gripper(speed=100)

def cerrar_herramienta():
    robot.calibrate_auto()
    robot.update_tool()
    robot.close_gripper(speed=100)

def get_posicion():
    return robot.get_posicion_robot()

def leer_sensor():
    return robot.digital_read(robot.PIN_SENSOR_PIEZA_PEQUENYA) == robot.PinState.LOW

    

def registrar_pieza_pequenya():
    global contador_piezas_pequenyas
    contador_piezas_pequenyas += 1
    print("Piezas pequeñas:", contador_piezas_pequenyas)


def registrar_pieza_grande():
    global contador_piezas_grandes
    contador_piezas_grandes += 1
    print("Piezas grandes:", contador_piezas_grandes)

def sumar_pose(p1, p2):
    return PoseObject(
        x=p1.x + p2.x,
        y=p1.y + p2.y,
        z=p1.z + p2.z,
        roll=p1.roll + p2.roll,
        pitch=p1.pitch + p2.pitch,
        yaw=p1.yaw + p2.yaw
    )

contador_piezas_grandes = 0
contador_piezas_pequenyas = 0
num_obj = 0
es_grande = False

def Pickandplace(num_obj):
    num_obj = 0
    robot.calibrate_auto()
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
    robot.stop_conveyor(conveyor_id)
    robot.open_gripper(speed=100)

    while num_obj < 6:

        es_grande = False
        num_obj += 1

        robot.move_pose(POS_INICIAL)
        robot.move_pose(POS_PRE_COJER_PIEZA)
        robot.move_pose(POS_COJER_PIEZA)
        robot.close_gripper(speed=100)
        robot.move_pose(POS_PRE_COJER_PIEZA)
        robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
        robot.move_pose(POS_DEJAR_CONVEYOR)
        robot.open_gripper(speed=100)
        robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
        robot.move_pose(POS_INICIAL)
        robot.run_conveyor(conveyor_id, speed=100, direction=ConveyorDirection.FORWARD)
        while True:
            estado_sensor_grande = robot.digital_read(PIN_SENSOR_PIEZA_GRANDE)
            estado_sensor_pequenyo = robot.digital_read(PIN_SENSOR_PIEZA_PEQUENYA)

            # Detección pieza grande, los sensores estan uno encima del ortro, por lo que si el grande detecta, el pequeño también lo hará
            if estado_sensor_grande == PinState.LOW and estado_sensor_pequenyo == PinState.LOW:
                robot.stop_conveyor(conveyor_id)
                registrar_pieza_grande()
                es_grande = True
                robot.run_conveyor(conveyor_id, speed=100, direction=ConveyorDirection.BACKWARD)
                robot.wait(9.0)
                robot.stop_conveyor(conveyor_id)
                break
            robot.wait(0.1)    
            # Detección pieza pequeña, en este caso solo el sensor pequeño detectará la pieza.
            if estado_sensor_pequenyo == PinState.LOW and estado_sensor_grande == PinState.HIGH:
                robot.stop_conveyor(conveyor_id)
                registrar_pieza_pequenya()
                es_grande = False
                break
        


        if es_grande == False:
            robot.wait(1)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_RECOGER)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_PRE_CENTRO)

            if contador_piezas_pequenyas <= 3:
                offset = offset_pequenyas[contador_piezas_pequenyas - 1]

                robot.move_pose(sumar_pose(POS_PRE_CENTRO, offset))
                robot.move_pose(sumar_pose(POS_CENTRO, offset))
                robot.open_gripper(speed=100)
                robot.move_pose(sumar_pose(POS_PRE_CENTRO, offset))

        robot.move_pose(POS_INICIAL)

        
    robot.stop_conveyor(conveyor_id)
    robot.unset_conveyor(conveyor_id)
    robot.close_connection()
        
            
if __name__ == "__main__":
    Pickandplace(num_obj)

