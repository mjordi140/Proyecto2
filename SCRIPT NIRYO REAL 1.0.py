#!/usr/bin/env python3
from pyniryo import NiryoRobot, ConveyorDirection, PinID, PoseObject, PinState

IP_ROBOT = "172.16.190.28"
robot = NiryoRobot(IP_ROBOT)

META_PIEZAS_PEQUENYAS = 3

POS_INICIAL = PoseObject(x=0.251, y=0.000, z=0.313, roll=0.239, pitch=1.421, yaw=0.350)
POS_STOP = PoseObject(x=0, y=0, z=0, roll=0, pitch=0, yaw=0)

POS_COJER_PIEZA = PoseObject(x=0.286, y=0.179, z=0.158, roll=0.476, pitch=1.540, yaw=0.492)
POS_PRE_COJER_PIEZA = PoseObject(x=0.279, y=0.179, z=0.204, roll=0.983, pitch=1.547, yaw=1.005)

POS_PRE_DEJAR_CONVEYOR = PoseObject(x=-0.037, y=0.204, z=0.205, roll=1.976, pitch=1.547, yaw=2.01)
POS_DEJAR_CONVEYOR = PoseObject(x=-0.036, y=0.203, z=0.145, roll=3.01, pitch=1.547, yaw=3.028)

POS_RECOGER = PoseObject(x=0.286, y=0.179, z=0.158, roll=0.476, pitch=1.540, yaw=0.492)
POS_PRE_RECOGER = PoseObject(x=0.279, y=0.179, z=0.204, roll=0.983, pitch=1.547, yaw=1.005)

POS_PRE_DEJAR_1 = PoseObject(x=0.106, y=0.212, z=0.201, roll=2.945, pitch=1.514, yaw=3.028)
POS_DEJAR_1     = PoseObject(x=0.106, y=0.209, z=0.144, roll=-2.596, pitch=1.482, yaw=-2.588)

POS_PRE_DEJAR_2 = PoseObject(x=0.037, y=0.204, z=0.205, roll=1.976, pitch=1.547, yaw=2.01)
POS_DEJAR_2     = PoseObject(x=0.036, y=0.203, z=0.145, roll=3.01, pitch=1.547, yaw=3.028)

POS_PRE_DEJAR_3 = PoseObject(x=-0.019, y=0.2, z=0.203, roll=2.968, pitch=1.522, yaw=3.041)
POS_DEJAR_3     = PoseObject(x=-0.021, y=0.202, z=0.143, roll=3.059, pitch=1.513, yaw=3.135)

def main():
    Pickandplace(num_obj)

def stop():
    robot = NiryoRobot(IP_ROBOT)
    robot.move_pose(POS_DEJAR_3)


num_obj = 0

def Pickandplace(num_obj):
    num_obj = 0
    robot.calibrate_auto()
    robot.update_tool()
    conveyor_id = robot.set_conveyor()
    robot.stop_conveyor(conveyor_id)
    robot.open_gripper(speed=100)

    while num_obj < 3:
        num_obj += 1
        if num_obj == 1:
            robot.move_pose(POS_PRE_COJER_PIEZA)
            robot.move_pose(POS_COJER_PIEZA)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_COJER_PIEZA)


            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
            robot.move_pose(POS_DEJAR_CONVEYOR)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
                        
            robot.move_pose(POS_INICIAL)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_RECOGER)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_PRE_DEJAR_1)
            robot.move_pose(POS_DEJAR_1)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_1)
            robot.move_pose(POS_INICIAL)
        elif num_obj == 2:
            robot.move_pose(POS_PRE_COJER_PIEZA)
            robot.move_pose(POS_COJER_PIEZA)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_COJER_PIEZA)


            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
            robot.move_pose(POS_DEJAR_CONVEYOR)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)

            robot.move_pose(POS_INICIAL)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_RECOGER)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_PRE_DEJAR_2)
            robot.move_pose(POS_DEJAR_2)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_2)
            robot.move_pose(POS_INICIAL)
        else:
            robot.move_pose(POS_PRE_COJER_PIEZA)
            robot.move_pose(POS_COJER_PIEZA)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_COJER_PIEZA)


            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
            robot.move_pose(POS_DEJAR_CONVEYOR)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_CONVEYOR)
                        
            robot.move_pose(POS_INICIAL)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_RECOGER)
            robot.close_gripper(speed=100)
            robot.move_pose(POS_PRE_RECOGER)
            robot.move_pose(POS_PRE_DEJAR_3)
            robot.move_pose(POS_DEJAR_3)
            robot.open_gripper(speed=100)
            robot.move_pose(POS_PRE_DEJAR_3)
            robot.move_pose(POS_INICIAL)

            robot.unset_conveyor(conveyor_id)
            robot.close_connection()
        
            
if __name__ == "__main__":
    Pickandplace(num_obj)

