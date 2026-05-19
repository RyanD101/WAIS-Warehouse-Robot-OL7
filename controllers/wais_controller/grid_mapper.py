
 
from controller import Robot
import navigation
import perception
import grid_mapper
import math
 
robot   = Robot()
timestep = int(robot.getBasicTimeStep())
 
# FSM States
EXPLORE         = "EXPLORE"
AVOID_OBSTACLE  = "AVOID_OBSTACLE"
TARGET_DETECTED = "TARGET_DETECTED"
RECOVERY        = "RECOVERY"
 
state = EXPLORE
 

navigation.setup(robot, timestep)
perception.setup(robot, timestep)
 

START_X       = -1.92765
START_Y       = -0.00240742
START_HEADING =  0.0          
 
grid_mapper.setup(robot, timestep,
                  start_x=START_X,
                  start_y=START_Y,
                  start_heading=START_HEADING)
 

inventory_count      = 0
recovery_counter     = 0
last_print_time      = 0
last_grid_print_time = 0
no_detection_counter = 0
last_logged_colour   = None
currently_detecting  = False
 
print("[WAIS] Controller started")
 

while robot.step(timestep) != -1:
 
    
    colour   = perception.detect_inventory_marker()
    obstacle = navigation.obstacle_detected()
    grid_mapper.update()                        
 
    current_time = robot.getTime()
 
    
    if obstacle:
        colour = None
 
    
    if colour is None:
        no_detection_counter += 1
    else:
        no_detection_counter = 0
 
    if no_detection_counter > 30:
        currently_detecting  = False
        last_logged_colour   = None
 
    
    if recovery_counter > 40:
        state = RECOVERY
    elif obstacle:
        state = AVOID_OBSTACLE
    elif colour is not None:
        state = TARGET_DETECTED
    else:
        state = EXPLORE
 
    
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
            if current_time - last_print_time > 2.0:
                print("[WAIS] Exploration complete!")
                print(f"[WAIS] Total inventory items logged: {inventory_count}")
 
    elif state == AVOID_OBSTACLE:
        navigation.avoid_obstacle()
        recovery_counter += 1
        perception.reset_confirmation()
 
    elif state == TARGET_DETECTED:
        navigation.move_forward()
 
        
        if colour != last_logged_colour:
            inventory_count   += 1
            last_logged_colour = colour
            print(f"[WAIS] Item logged: {colour}  |  Total: {inventory_count}")
 
    elif state == RECOVERY:
        print("[WAIS] Recovery behaviour triggered")
        navigation.reverse()
        navigation.turn_right()
        recovery_counter = 0
        perception.reset_confirmation()
 
    
    if current_time - last_print_time > 0.5:
        x, y, hdg = grid_mapper.get_pose()
        print(f"[WAIS] State: {state}  |  "
              f"Pos: ({x:.2f}, {y:.2f})  |  "
              f"Heading: {math.degrees(hdg):.1f}°  |  "
              f"Coverage: {grid_mapper.coverage_percent():.1f}%")
        last_print_time = current_time
 
    
    if current_time - last_grid_print_time > 10.0:
        grid_mapper.print_grid()
        last_grid_print_time = current_time