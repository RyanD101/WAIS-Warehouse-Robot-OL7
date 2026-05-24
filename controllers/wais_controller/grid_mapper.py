gps = None

WAYPOINTS = [
    (1.88, 0.173, "left"),
    (1.88, 0.553, "left"),
    (-1.82, 0.553, "right"),
    (-1.82, 0.953, "right"),
    (1.83, 0.953, "left"),
    (1.83, 1.34, "left"),
    (-1.67, 1.34, "done")
]

current_target = 0
turn_steps = 0
turn_direction = None

TURN_STEPS = 22
TARGET_DISTANCE = 0.12

visited_points = set()


def setup(robot, timestep, start_x=0.0, start_y=0.0, start_heading=0.0):
    global gps

    gps = robot.getDevice("gps")
    gps.enable(timestep)

    print("[GRID] Waypoint mapper enabled")


def get_pose():
    values = gps.getValues()

    x = values[0]
    y = values[1]
    heading = 0.0

    return x, y, heading


def update():
    x, y, heading = get_pose()
    visited_points.add((round(x, 1), round(y, 1)))


def get_explore_direction():
    global current_target, turn_steps, turn_direction

    if current_target >= len(WAYPOINTS):
        return "done"

    if turn_steps > 0:
        turn_steps -= 1
        return turn_direction

    x, y, heading = get_pose()

    target_x, target_y, action = WAYPOINTS[current_target]

    dx = target_x - x
    dy = target_y - y

    distance = (dx * dx + dy * dy) ** 0.5

    if distance < TARGET_DISTANCE:
        visited_points.add((round(target_x, 1), round(target_y, 1)))

        if action == "done":
            return "done"

        turn_direction = action
        turn_steps = TURN_STEPS

        current_target += 1

        return turn_direction

    return "forward"


def coverage_percent():
    return (len(visited_points) / len(WAYPOINTS)) * 100


def print_grid():
    print("[GRID] Visited points:", visited_points)
    print("[GRID] Coverage:", round(coverage_percent(), 1), "%")