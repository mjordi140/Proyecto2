
# !/usr/bin/env python3
from pyniryo import NiryoRobot, JointsPosition, PoseObject, PinID, PinState, ConveyorDirection

robot = NiryoRobot("127.0.0.1")

initial_pose = JointsPosition(0.0,0.0,0.0,0.000,0.0000,0.0000)

atak_pieza1 = JointsPosition(-2.3496,-1.0715,0.5021,0,-1.0017,-2.3929)
pieza1_pick = JointsPosition(-2.3602,-1.1943,0.5854,0,-0.9618,-0.7638)

atak_pieza2 = JointsPosition(-2.5231,-0.8185,0.0537,0,-0.8054,-2.5294)
pieza2_pick = JointsPosition(-2.5474,-0.967,0.1158,0,-0.7195,2.166)


atak_pieza3 = JointsPosition(-2.7848,-0.6625,-0.2037,0,-0.7057,-2.5294)
pieza3_pick = JointsPosition(-2.7985,-0.8655,-0.1371,0,-0.5676,1.9145)


atak_conveyor = JointsPosition(-0.7622,0.2524,-0.2568,0.0691,-1.4082,-0.0198)
conveyor_place = JointsPosition(-0.7165,-0.4125,-0.4855,0.0215,-0.6873,2.5296)

observation_pose = JointsPosition(0.7809,0.3479,-0.6825,0.0522,-1.2917,2.5296)

atak_afterVision = JointsPosition(0.6653,-0.2247,-0.4916,0,-0.8545,-0.8988)
pick_afterVision = JointsPosition(0.7535,-0.4428,-0.4492,0,-0.6796,-0.8098)

atak_plataforma = JointsPosition(-1.6008,-0.055,0.1279,-0.0766,-1.9191,0.1504)
plataforma_pieza1 = JointsPosition(-1.339,-0.4186,-0.487,-0.0029,-0.7026,0.3805)
plataforma_pieza2 = JointsPosition(-1.5764,-0.3838,-0.5476,-0.0183,-0.675,0.1565)
plataforma_pieza3 = JointsPosition(-1.7758,-0.3928,-0.5325,-0.029,-0.6796,-0.0305)

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
            robot.move(atak_pieza1)
            robot.move(pieza1_pick)
            robot.close_gripper(speed=100)


            robot.move(atak_conveyor)
            robot.move(conveyor_place)
            robot.open_gripper(speed=100)
                        
            robot.move(observation_pose)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move(atak_afterVision)
            robot.move(pick_afterVision)
            robot.close_gripper(speed=100)
            robot.move(atak_plataforma)
            robot.move(plataforma_pieza1)
            robot.open_gripper(speed=100)
            robot.move(atak_plataforma)
        elif num_obj == 2:
            robot.move(atak_pieza2)
            robot.move(pieza2_pick)
            robot.close_gripper(speed=100)


            robot.move(atak_conveyor)
            robot.move(conveyor_place)
            robot.open_gripper(speed=100)
                        
            robot.move(observation_pose)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move(atak_afterVision)
            robot.move(pick_afterVision)
            robot.close_gripper(speed=100)
            robot.move(atak_plataforma)
            robot.move(plataforma_pieza2)
            robot.open_gripper(speed=100)
            robot.move(atak_plataforma)
        else:
            robot.move(atak_pieza3)
            robot.move(pieza3_pick)
            robot.close_gripper(speed=100)


            robot.move(atak_conveyor)
            robot.move(conveyor_place)
            robot.open_gripper(speed=100)
                        
            robot.move(observation_pose)
            robot.run_conveyor(conveyor_id, speed=50, direction=ConveyorDirection.FORWARD)

            robot.wait(7)
            robot.stop_conveyor(conveyor_id)
            robot.wait(2)
            robot.move(atak_afterVision)
            robot.move(pick_afterVision)
            robot.close_gripper(speed=100)
            robot.move(atak_plataforma)
            robot.move(plataforma_pieza3)
            robot.open_gripper(speed=100)
            robot.move(atak_plataforma)

            robot.unset_conveyor(conveyor_id)
            robot.close_connection()
        
            
if __name__ == "__main__":
    Pickandplace(num_obj)

