camera = None

red_seen = False
green_seen = False

RED_ON = 60
RED_OFF = 30

GREEN_ON = 60
GREEN_OFF = 40


def setup(robot, timestep):
    global camera

    camera = robot.getDevice("camera")
    camera.enable(timestep)

    print("[VISION] Camera enabled")


def detect_inventory_marker():
    global red_seen, green_seen

    image = camera.getImage()

    if image is None:
        return None

    width = camera.getWidth()
    height = camera.getHeight()

    red_pixels = 0
    green_pixels = 0

    y_start = height // 3
    y_end = 2 * height // 3

    for x in range(0, width):
        for y in range(y_start, y_end):

            r = camera.imageGetRed(image, width, x, y)
            g = camera.imageGetGreen(image, width, x, y)
            b = camera.imageGetBlue(image, width, x, y)

            if r > 80 and r > g + 40 and r > b + 40:
                red_pixels += 1

            if g > 80 and g > r + 40 and g > b + 40:
                green_pixels += 1

    detected_colour = None
    
    if not red_seen and red_pixels >= RED_ON:
        red_seen = True
        detected_colour = "red"

    if red_seen and red_pixels <= RED_OFF:
        red_seen = False


    if not green_seen and green_pixels >= GREEN_ON:
        green_seen = True
        detected_colour = "green"

    if green_seen and green_pixels <= GREEN_OFF:
        green_seen = False

    return detected_colour


def confirm_detection(colour):

    if colour is not None:
        return True

    return False


def reset_confirmation():
    pass