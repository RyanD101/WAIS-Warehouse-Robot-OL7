MAX_SPEED = 6.28 

leftMotor = None
rightMotor = None
ps = []  

OBSTACLE_THRESHOLD = 80.0

FRONT_SENSORS = [0, 7]
FRONT_SIDE_SENSORS = [1, 6]
ALL_OBSTACLE_SENSORS = [0, 1, 6, 7]


def setup(robot, timestep):
    global leftMotor, rightMotor, ps

    leftMotor = robot.getDevice("left wheel motor")
    rightMotor = robot.getDevice("right wheel motor")

    leftMotor.setPosition(float("inf"))
    rightMotor.setPosition(float("inf"))

    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)
    
    ps = []
    for i in range(8):
        sensor = robot.getDevice(f"ps{i}")
        sensor.enable(timestep)
        ps.append(sensor)

    print("[NAV] Motors and proximity sensors initialised")


def read_sensors():
    return [ps[i].getValue() for i in range(8)]


def obstacle_detected():
    values = read_sensors()
    for i in ALL_OBSTACLE_SENSORS:
        if values[i] > OBSTACLE_THRESHOLD:
            return True
    return False


def move_forward():
    leftMotor.setVelocity(MAX_SPEED)
    rightMotor.setVelocity(MAX_SPEED)


def avoid_obstacle():
    values = read_sensors()

    right_threat = values[0] + values[1]
    left_threat = values[6] + values[7]

    if right_threat > left_threat:
        leftMotor.setVelocity(-MAX_SPEED * 0.5)
        rightMotor.setVelocity(MAX_SPEED * 0.5)
    else:
        leftMotor.setVelocity(MAX_SPEED * 0.5)
        rightMotor.setVelocity(-MAX_SPEED * 0.5)


def reverse():
    leftMotor.setVelocity(-MAX_SPEED * 0.5)
    rightMotor.setVelocity(-MAX_SPEED * 0.5)


def turn_right():
    leftMotor.setVelocity(MAX_SPEED * 0.5)
    rightMotor.setVelocity(-MAX_SPEED * 0.5)


def turn_left():
    leftMotor.setVelocity(-MAX_SPEED * 0.5)
    rightMotor.setVelocity(MAX_SPEED * 0.5)


def stop_robot():
    leftMotor.setVelocity(0.0)
    rightMotor.setVelocity(0.0)