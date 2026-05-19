#!/usr/bin/env python3
from pyniryo import NiryoRobot, ConveyorDirection, PinID, PoseObject, PinState

IP_ROBOT = "172.16.190.28"
robot = NiryoRobot(IP_ROBOT)

PIN_SENSOR_PIEZA_PEQUENYA = PinID.DI5
PIN_SENSOR_PIEZA_GRANDE  = PinID.DI1

META_PIEZAS_PEQUENYAS = 3

POS_INICIAL = PoseObject(x=0.251, y=0.000, z=0.313, roll=0.239, pitch=1.421, yaw=0.350)
POS_STOP = PoseObject(x=0, y=0, z=0, roll=0, pitch=0, yaw=0)

POS_COJER_PIEZA = PoseObject(x=0.286, y=0.179, z=0.158, roll=0.476, pitch=1.540, yaw=0.492)
POS_PRE_COJER_PIEZA = PoseObject(x=0.279, y=0.179, z=0.204, roll=0.983, pitch=1.547, yaw=1.005)

POS_PRE_DEJAR_CONVEYOR = PoseObject(x=-0.037, y=0.204, z=0.205, roll=1.976, pitch=1.547, yaw=2.01)
POS_DEJAR_CONVEYOR = PoseObject(x=-0.036, y=0.203, z=0.145, roll=3.01, pitch=1.547, yaw=3.028)

POS_RECOGER = PoseObject(x=0.286, y=0.179, z=0.158, roll=0.476, pitch=1.540, yaw=0.492)
POS_PRE_RECOGER = PoseObject(x=0.279, y=0.179, z=0.204, roll=0.983, pitch=1.547, yaw=1.005)

POS_PRE_CENTRO = PoseObject(x=0.106, y=0.212, z=0.201, roll=2.945, pitch=1.514, yaw=3.028)
POS_CENTRO = PoseObject(x=0.106, y=0.212, z=0.201, roll=2.945, pitch=1.514, yaw=3.028)

# ahora tengo qu eponer los offsets de las 6 piezas e intentar que si detecta una pieza pequeña la deje arriba de izquierda a derecha y si detecta una pieza grande la deje debajo de izquierda a derecha de la POS_CENTRO, es decir, la pieza pequeña 1 se dejará en la parte superior izquierda de la POS_CENTRO, la pieza pequeña 2 en la parte superior central y la pieza pequeña 3 en la parte superior derecha, mientras que la pieza grande 1 se dejará en la parte inferior izquierda de la POS_CENTRO.
offset_pequenyas = [PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0),
                    PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0),
                    PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0)]
offset_grandes = [PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0),
                    PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0),
                    PoseObject(x=0.0, y=0.0, z=0.0, roll=0.0, pitch=0.0, yaw=0.0)]


def main():
    Pickandplace(num_obj)

def stop():
    robot.stop()
    robot.stop_conveyor()

    

def registrar_pieza_pequenya():
    global contador_piezas_pequenyas
    contador_piezas_pequenyas += 1
    print("Piezas pequeñas:", contador_piezas_pequenyas)


def registrar_pieza_grande():
    global contador_piezas_grandes
    contador_piezas_grandes += 1
    print("Piezas grandes:", contador_piezas_grandes)


num_obj = 0
es_grande = false

def Pickandplace(num_obj):
    num_obj = 0
    robot.calibrate_auto()
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
    robot.stop_conveyor(conveyor_id)
    robot.open_gripper(speed=100)

    while num_obj < 6:

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
                es_grande = true
                break

            # Detección pieza pequeña, en este caso solo el sensor pequeño detectará la pieza.
            if estado_sensor_pequenyo == PinState.LOW:
                robot.stop_conveyor(conveyor_id)
                registrar_pieza_pequenya()
                es_grande = false
                break
        
        robot.wait(1)
        robot.move_pose(POS_PRE_RECOGER)
        robot.move_pose(POS_RECOGER)
        robot.close_gripper(speed=100)
        robot.move_pose(POS_PRE_RECOGER)
        robot.move_pose(POS_PRE_CENTRO)
        if es_grande:
            robot.move_pose(POS_PRE_CENTRO + offset_grandes[contador_piezas_grandes-1])
            robot.move_pose(POS_CENTRO + offset_grandes[contador_piezas_grandes-1])

        else:
            robot.move_pose(POS_PRE_CENTRO + offset_pequenyas[contador_piezas_pequenyas-1])
            robot.move_pose(POS_CENTRO + offset_pequenyas[contador_piezas_pequenyas-1])
        robot.open_gripper(speed=100)

        robot.move_pose(POS_PRE_CENTRO)
        robot.move_pose(POS_INICIAL)
        
    robot.unset_conveyor(conveyor_id)
    robot.close_connection()
        
            
if __name__ == "__main__":
    Pickandplace(num_obj)

