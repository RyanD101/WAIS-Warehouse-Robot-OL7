from controller import Robot

TIME_STEP = 64
MAX_SPEED = 6.28

robot = Robot()

# Motors
left_motor = robot.getDevice("left wheel motor")
right_motor = robot.getDevice("right wheel motor")

left_motor.setPosition(float("inf"))
right_motor.setPosition(float("inf"))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Proximity sensors
ps_names = ["ps0", "ps1", "ps2", "ps3", "ps4", "ps5", "ps6", "ps7"]
ps = []

for name in ps_names:
    sensor = robot.getDevice(name)
    sensor.enable(TIME_STEP)
    ps.append(sensor)

def set_motor_speeds(left_speed, right_speed):
    left_motor.setVelocity(left_speed)
    right_motor.setVelocity(right_speed)

def read_proximity():
    return [sensor.getValue() for sensor in ps]

def detect_obstacle(values):
    right_obstacle = values[0] > 80 or values[1] > 80 or values[2] > 80
    left_obstacle = values[5] > 80 or values[6] > 80 or values[7] > 80
    return left_obstacle, right_obstacle

while robot.step(TIME_STEP) != -1:
    ps_values = read_proximity()
    left_obstacle, right_obstacle = detect_obstacle(ps_values)

    left_speed = 0.5 * MAX_SPEED
    right_speed = 0.5 * MAX_SPEED

    if left_obstacle:
        print("Obstacle left → turning right")
        left_speed = 0.5 * MAX_SPEED
        right_speed = -0.5 * MAX_SPEED

    elif right_obstacle:
        print("Obstacle right → turning left")
        left_speed = -0.5 * MAX_SPEED
        right_speed = 0.5 * MAX_SPEED

    else:
        print("EXPLORE")

    set_motor_speeds(left_speed, right_speed)