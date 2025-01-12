from robodk.robolink import *  # Import the RoboDK API
from robodk.robomath import transl, rotz
from math import radians, cos, sin, atan2  # Use the standard math module
import time
import math

# Establishing the connection with RoboDK Robot
RDK = Robolink()  # Correctly instantiate the RoboDK connection

# Configuring two different robots as RoboDK items
robot_1 = RDK.Item('Epson VT6')  # Select the robot by name
station_1_frame = RDK.Item('station_1_frame')    # Initial frame of the object
outlet_frame = RDK.Item('outlet_frame')# Final frame for the object


if not robot_1.Valid():
    print("Error: Robot not found or invalid item")
    quit()

# Select the home target
home = RDK.Item('home')
#Feed frame Section
cone_approach = RDK.Item('approach')
cone_target = RDK.Item('cone_target')  

cone1App_pos = RDK.Item("cone_approach")
secondApp_target =  cone1App_pos.Pose()*transl(0, -120, 0)
thirdApp_target =  cone1App_pos.Pose()*transl(0, -240, 0)
fourthApp_target =  cone1App_pos.Pose()*transl(0, 0, 120)
fifthApp_target =  cone1App_pos.Pose()*transl(0, -120, 120)
sixthApp_target =  cone1App_pos.Pose()*transl(0, -240, 120)

approachPoints = [cone_approach, secondApp_target, thirdApp_target, fourthApp_target, fifthApp_target, sixthApp_target]

cone1_pos = RDK.Item("cone_target")
second_target =  cone1_pos.Pose()*transl(0, -120, 0)
third_target =  cone1_pos.Pose()*transl(0, -240, 0)
fourth_target =  cone1_pos.Pose()*transl(0, 0, 120)
fifth_target =  cone1_pos.Pose()*transl(0, -120, 120)
sixth_target =  cone1_pos.Pose()*transl(0, -240, 120)

targetPoints = [cone_target, second_target, third_target, fourth_target, fifth_target, sixth_target]

cone_names = [
    'cone_1','cone_2','cone_3','cone_4','cone_5','cone_6',
]

#Filling frame Section

filling_start = RDK.Item('cone_1_fill')
filling_cone_start = RDK.Item('cone_start')
filling_station_1 = RDK.Item('filling')
filling_cone_station_1 = RDK.Item('cone_station')
filling_middle = RDK.Item('middle_fill')
filling_cone_middle = RDK.Item('cone_middle')
filling_station_2 = RDK.Item('middle_2_fill')
filling_cone_station_2 = RDK.Item('filling_station')
filling_end = RDK.Item('end_filling')

hexagonCenter = RDK.Item('centerOfOutlet_')  #hexagon center

#Outlet frame Section
cone1_filling_retract = RDK.Item('cone_1_retract')
cone2_RetractPoint = RDK.Item("cone2DropPoint").Pose()*transl(325.027, 0, 0)
cone3_RetractPoint = RDK.Item("cone3DropPoint").Pose()*transl(325.027, 0, 0)
cone4_RetractPoint = RDK.Item("cone4DropPoint").Pose()*transl(325.027, 0, 0)
cone5_RetractPoint = RDK.Item("cone5DropPoint").Pose()*transl(325.027, 0, 0)
cone6_RetractPoint = RDK.Item("cone6DropPoint").Pose()*transl(325.027, 0, 0)

cone_1_place = RDK.Item('cone_1_place') 
cone2DropPoint = RDK.Item('cone_2_drop')
cone3DropPoint = RDK.Item('cone_3_drop')
cone4DropPoint = RDK.Item('cone_4_drop')
cone5DropPoint = RDK.Item('cone_5_drop')
cone6DropPoint = RDK.Item('cone_6_drop')

stopPoint = RDK.Item('stopping') 

outlet_retractPoint = [cone_1_place, cone2_RetractPoint, cone3_RetractPoint, cone4_RetractPoint, cone5_RetractPoint, cone6_RetractPoint]
outlet_targetPoint = [cone_1_place, cone2DropPoint, cone3DropPoint, cone4DropPoint, cone5DropPoint, cone6DropPoint]


# Run a Python script program
gripper_open = RDK.Item('gripper_open', ITEM_TYPE_PROGRAM)  # For gripper open
gripper_close = RDK.Item('gripper_close', ITEM_TYPE_PROGRAM)  # For gripper close
Replace = RDK.Item('Replace_Corns', ITEM_TYPE_PROGRAM)  # For Cones back to feed frame


# Find the object to attach
object_to_attach = RDK.Item('cone_1')  # Replace 'Cone' with the name of your object

# Attach the object to the robot's tool
tool = robot_1.Childs()[0]  # Get the robot's tool (or specify the tool name directly)

if object_to_attach.Valid() and tool.Valid():
    print("Object and Tool set successfully.")
else:
    print("Error: Object and/or Tool is not valid.")

def TCP_On(object_to_attach):
    object_to_attach = RDK.Item(object_to_attach)
    current_pose = object_to_attach.PoseAbs() 
    object_to_attach.setParent(tool)
    object_to_attach.setPoseAbs(current_pose)
    print("Object attached to the tool.")

def TCP_Off(object_to_attach):
    object_to_attach = RDK.Item(object_to_attach)
    current_pose = object_to_attach.PoseAbs()
    object_to_attach.setParent(outlet_frame)   
    object_to_attach.setPoseAbs(current_pose)
    print("Object detached from the tool and reattached to Outlet Frame.")

def main():
    Replace.RunCode()
    robot_1.MoveJ(home)

    for n in range(6):
        # n = 1
        # Set the speed of the robot
        robot_1.setSpeed(100)  # Use the method on the robot item

        robot_1.MoveJ(approachPoints[n])
        gripper_open.RunCode()
        time.sleep(0.5)
        robot_1.MoveL(targetPoints[n])
        gripper_close.RunCode()
        time.sleep(1)
        TCP_On(cone_names[n])
        time.sleep(1)
        robot_1.MoveL(approachPoints[n])
        robot_1.MoveJ(filling_start)
        robot_1.MoveC(filling_cone_start, filling_station_1)
        time.sleep(1)
        robot_1.MoveC(filling_cone_station_1, filling_middle)
        robot_1.MoveC(filling_cone_middle, filling_station_2)
        time.sleep(1)
        robot_1.MoveC(filling_cone_station_2, filling_end)
        robot_1.MoveJ(outlet_retractPoint[n])
        robot_1.MoveL(outlet_targetPoint[n])
        gripper_open.RunCode()
        time.sleep(0.5)
        TCP_Off(cone_names[n])
        time.sleep(0.5)
        robot_1.MoveL(outlet_retractPoint[n])
        robot_1.MoveJ(home)

    robot_1.MoveJ(stopPoint)

main()
