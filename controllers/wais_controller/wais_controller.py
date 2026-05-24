from controller import Robot
import navigation
import perception
import grid_mapper
import math

robot = Robot()
timestep = int(robot.getBasicTimeStep())

# FSM states
EXPLORE = "EXPLORE"
AVOID_OBSTACLE = "AVOID_OBSTACLE"
TARGET_DETECTED = "TARGET_DETECTED"
RECOVERY = "RECOVERY"

state = EXPLORE

navigation.setup(robot, timestep)
perception.setup(robot, timestep)
grid_mapper.setup(robot, timestep,
                  start_x=-1.92765,
                  start_y=0,
                  start_heading=0.0)

inventory_count = 0
recovery_counter = 0
last_print_time = 0

currently_detecting = False
no_detection_counter = 0
last_logged_colour = None

print("Controller started")

while robot.step(timestep) != -1:
    
    grid_mapper.update()
    
    colour = perception.detect_inventory_marker()
    obstacle = navigation.obstacle_detected()
    if obstacle:
        colour = None

    current_time = robot.getTime()

    if colour is None:
        no_detection_counter += 1
    else:
        no_detection_counter = 0

    if no_detection_counter > 30:
        currently_detecting = False
        last_logged_colour = None

    if recovery_counter > 40:
        state = RECOVERY

    elif obstacle:
        state = AVOID_OBSTACLE

    elif colour is not None:
        state = TARGET_DETECTED

    else:
        state = EXPLORE

    if current_time - last_print_time > 0.5:
        print("State:", state)
        last_print_time = current_time

    if state == EXPLORE:
        
        recovery_counter = 0
        perception.reset_confirmation()
    
        direction = grid_mapper.get_explore_direction()
    
        if direction == "forward":
            navigation.move_forward()
    
        elif direction == "left":
            navigation.turn_left()
    
        elif direction == "right":
            navigation.turn_right()
    
        elif direction == "done":
            navigation.stop_robot()
            print("[WAIS] Route complete")

    elif state == AVOID_OBSTACLE:

        navigation.avoid_obstacle()
        recovery_counter += 1
        perception.reset_confirmation()

    elif state == TARGET_DETECTED:

        navigation.move_forward()
    
        inventory_count += 1
    
        print("Logged item:", colour)
        print("Inventory count:", inventory_count)
    
    elif state == RECOVERY:

        print("Recovery behaviour")

        navigation.reverse()
        navigation.turn_right()

        recovery_counter = 0
        perception.reset_confirmation()