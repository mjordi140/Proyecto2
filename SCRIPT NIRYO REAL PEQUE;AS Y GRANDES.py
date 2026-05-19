#!/usr/bin/env python3
from pyniryo import NiryoRobot, ConveyorDirection, PinID, PoseObject, PinState

IP_ROBOT = "158.42.132.206"

PIN_SENSOR_PIEZA_PEQUENYA = PinID.DI5
PIN_SENSOR_PIEZA_GRANDE  = PinID.DI1

META_PIEZAS_PEQUENYAS = 3

POS_INICIAL = PoseObject(x=0.251, y=0.000, z=0.313, roll=0.239, pitch=1.421, yaw=0.350)

POS_RECOGER = PoseObject(x=0.286, y=0.179, z=0.158, roll=0.476, pitch=1.540, yaw=0.492)
POS_PRE_RECOGER = PoseObject(x=0.279, y=0.179, z=0.204, roll=0.983, pitch=1.547, yaw=1.005)

POS_PRE_DEJAR_1 = PoseObject(x=0.106, y=0.212, z=0.201, roll=2.945, pitch=1.514, yaw=3.028)
POS_DEJAR_1     = PoseObject(x=0.106, y=0.209, z=0.144, roll=-2.596, pitch=1.482, yaw=-2.588)

POS_PRE_DEJAR_2 = PoseObject(x=0.037, y=0.204, z=0.205, roll=1.976, pitch=1.547, yaw=2.01)
POS_DEJAR_2     = PoseObject(x=0.036, y=0.203, z=0.145, roll=3.01, pitch=1.547, yaw=3.028)

POS_PRE_DEJAR_3 = PoseObject(x=-0.019, y=0.2, z=0.203, roll=2.968, pitch=1.522, yaw=3.041)
POS_DEJAR_3     = PoseObject(x=-0.021, y=0.202, z=0.143, roll=3.059, pitch=1.513, yaw=3.135)

contador_piezas_pequenyas = 0
contador_piezas_grandes = 0


def registrar_pieza_pequenya():
    global contador_piezas_pequenyas
    contador_piezas_pequenyas += 1
    print("Piezas pequeñas:", contador_piezas_pequenyas)


def registrar_pieza_grande():
    global contador_piezas_grandes
    contador_piezas_grandes += 1
    print("Piezas grandes:", contador_piezas_grandes)


def ejecutar_clasificacion():
    global contador_piezas_pequenyas, contador_piezas_grandes

    robot = NiryoRobot(IP_ROBOT)

    try:
        robot.calibrate_auto()
        robot.update_tool()
        robot.open_gripper(speed=400)
        robot.move_pose(POS_INICIAL)

        cinta_transportadora = robot.set_conveyor()

        while contador_piezas_pequenyas < META_PIEZAS_PEQUENYAS or contador_piezas_grandes < META_PIEZAS_GRANDES:
            robot.run_conveyor(cinta_transportadora, speed=100, direction=ConveyorDirection.FORWARD)

            while True:
                estado_sensor_grande = robot.digital_read(PIN_SENSOR_PIEZA_GRANDE)
                estado_sensor_pequenyo = robot.digital_read(PIN_SENSOR_PIEZA_PEQUENYA)

                # Detección pieza grande
                if estado_sensor_grande == PinState.LOW:
                    robot.stop_conveyor(cinta_transportadora)
                    robot.run_conveyor(cinta_transportadora, speed=100, direction=ConveyorDirection.BACKWARD)
                    robot.wait(12.0)
                    robot.stop_conveyor(cinta_transportadora)
                    registrar_pieza_grande()
                    break

                # Detección pieza pequeña
                if estado_sensor_pequenyo == PinState.LOW:
                    robot.stop_conveyor(cinta_transportadora)

                    # Elegir posición de depósito según cuántas pequeñas llevamos
                    if contador_piezas_pequenyas == 0:
                        pos_pre_dejar = POS_PRE_DEJAR_1
                        pos_dejar = POS_DEJAR_1
                    elif contador_piezas_pequenyas == 1:
                        pos_pre_dejar = POS_PRE_DEJAR_2
                        pos_dejar = POS_DEJAR_2
                    else:
                        pos_pre_dejar = POS_PRE_DEJAR_3
                        pos_dejar = POS_DEJAR_3

                    # Recoger pieza
                    robot.move_pose(POS_PRE_RECOGER)
                    robot.open_gripper(speed=400)
                    robot.move_pose(POS_RECOGER)
                    robot.close_gripper(speed=400)
                    robot.move_pose(POS_PRE_RECOGER)

                    # Dejar pieza
                    robot.move_pose(pos_pre_dejar)
                    robot.move_pose(pos_dejar)
                    robot.open_gripper(speed=400)
                    robot.move_pose(pos_pre_dejar)

                    # Volver a inicial
                    robot.move_pose(POS_INICIAL)

                    registrar_pieza_pequenya()
                    break

                robot.wait(0.05)

        robot.stop_conveyor(cinta_transportadora)
        robot.unset_conveyor(cinta_transportadora)
        robot.move_pose(POS_INICIAL)

    finally:
        robot.close_connection()


if __name__ == "__main__":
    ejecutar_clasificacion()