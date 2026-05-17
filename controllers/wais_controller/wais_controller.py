from controller import Robot
import navigation
import perception

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

inventory_count = 0
recovery_counter = 0
last_print_time = 0

currently_detecting = False
no_detection_counter = 0
last_logged_colour = None

print("Controller started")

while robot.step(timestep) != -1:

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

        navigation.move_forward()
        recovery_counter = 0
        perception.reset_confirmation()

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