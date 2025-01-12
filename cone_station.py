from robodk.robolink import *  # Import the RoboDK API
from robodk.robomath import *  # Import RoboDK math utilities
import time

# Establish the connection with RoboDK
RDK = Robolink()

# Configure the robot and frames
robot_1 = RDK.Item('Epson VT6')  # Select the robot by name
station_1_frame = RDK.Item('station_1_frame')  # Initial frame for the object
outlet_frame = RDK.Item('outlet_frame')  # Final frame for the object

# Validate robot
if not robot_1.Valid():
    print("Error: Robot not found or invalid item")
    quit()

# Configure targets
home = RDK.Item('home')
approach = RDK.Item('approach')
cone_target = RDK.Item('cone_target')

# Validate targets
if not all([home.Valid(), approach.Valid(), cone_target.Valid()]):
    print("Error: One or more targets (home, approach, cone_target) are not valid")
    quit()

# Filling frame targets
filling_start = RDK.Item('cone_1_fill')
filling_cone_start = RDK.Item('cone_start')
filling_station_1 = RDK.Item('filling')
filling_cone_station_1 = RDK.Item('cone_station')
filling_middle = RDK.Item('middle_fill')
filling_cone_middle = RDK.Item('cone_middle')
filling_station_2 = RDK.Item('middle_2_fill')
filling_cone_station_2 = RDK.Item('filling_station')
filling_end = RDK.Item('end_filling')

# Outlet frame targets
retract_point = RDK.Item('cone_1_retract')
place_point = RDK.Item('cone_1_place')

# Validate outlet targets
if not all([retract_point.Valid(), place_point.Valid()]):
    print("Error: One or more outlet targets (cone_1_retract, cone_1_place) are not valid")
    quit()

# Gripper programs
gripper_open = RDK.Item('gripper_open', ITEM_TYPE_PROGRAM)
gripper_close = RDK.Item('gripper_close', ITEM_TYPE_PROGRAM)

# Validate gripper programs
if not gripper_open.Valid() or not gripper_close.Valid():
    print("Error: Gripper programs not found or invalid")
    quit()

# Object to attach
object_to_attach = RDK.Item('cone_1')

# Tool attachment
tool = robot_1.Childs()[0] if robot_1.Childs() else None

# Validate the tool and object
if not object_to_attach.Valid() or not tool.Valid():
    print("Error: Object or tool is not valid")
    quit()

print("Object and Tool set successfully.")

# Function to attach object to the tool
def TCP_On():
    """Attach the object to the robot's tool."""
    current_pose = object_to_attach.PoseAbs()
    object_to_attach.setParent(tool)
    object_to_attach.setPoseAbs(current_pose)
    print("Object attached to the tool.")

# Function to detach object from the tool
def TCP_Off():
    """Detach the object from the robot's tool and reattach it to the outlet frame."""
    current_pose = object_to_attach.PoseAbs()
    object_to_attach.setParent(outlet_frame)
    object_to_attach.setPoseAbs(current_pose)
    print("Object detached from the tool and reattached to the outlet frame.")

# Main sequence
def main():
    # Set the robot speed
    robot_1.setSpeed(50)

    # Move to the home position
    robot_1.MoveJ(home)

    # Pick the cone
    robot_1.MoveJ(approach)
    gripper_open.RunCode()
    time.sleep(0.5)
    robot_1.MoveL(cone_target)
    gripper_close.RunCode()
    TCP_On()
    time.sleep(0.5)
    robot_1.MoveL(approach)

    # Filling process
    robot_1.MoveJ(filling_start)
    robot_1.MoveC(filling_cone_start, filling_station_1)
    time.sleep(1)
    robot_1.MoveC(filling_cone_station_1, filling_middle)
    robot_1.MoveC(filling_cone_middle, filling_station_2)
    time.sleep(1)
    robot_1.MoveC(filling_cone_station_2, filling_end)

    # Place the cone
    robot_1.MoveJ(cone_1_retract)
    robot_1.MoveL(cone_1_place)
    gripper_open.RunCode()
    time.sleep(0.5)
    TCP_Off()
    time.sleep(0.5)
    robot_1.MoveL(cone_1_retract)

    # Return to home position
    robot_1.MoveJ(home)
    print("Task completed successfully.")

# Run the main sequence
main()
