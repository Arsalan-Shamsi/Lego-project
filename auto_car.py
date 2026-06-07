"""
Auto-Drive Lego Car for LEGO SPIKE (Prime / Education)
======================================================

What it does:
    The car drives forward on its own. When the Distance Sensor sees
    something too close in front, it stops, backs up a little, and turns
    away. Then it keeps driving forward again. No word blocks needed!

How to use:
    1. Open the LEGO SPIKE app.
    2. Make a NEW project and choose "Python" (not the word blocks).
    3. Delete whatever code is in there.
    4. Copy and paste ALL of this code in.
    5. Press the big "Play" button.

Wiring (change the letters below if your ports are different):
    - Left drive motor   -> port A
    - Right drive motor  -> port B
    - Distance Sensor    -> port F
"""

from spike import PrimeHub, MotorPair, DistanceSensor
from spike.control import wait_for_seconds

# ---- Setup: tell the program what is plugged in where ----
hub = PrimeHub()

# A MotorPair lets the two wheel motors steer together like a real car.
# If your car drives backwards, swap 'A' and 'B' here.
wheels = MotorPair('A', 'B')

# The eyes of the car. Change 'F' if your sensor is on another port.
eyes = DistanceSensor('F')

# ---- Settings you can play with ----
DRIVE_SPEED = 40        # how fast it drives forward (0 to 100)
STOP_DISTANCE_CM = 20   # how close something can get before we turn away
BACKUP_TIME = 0.6       # seconds to reverse before turning
TURN_DEGREES = 200      # how far to spin away (bigger = bigger turn)


def something_is_too_close():
    """Return True if there is an obstacle closer than STOP_DISTANCE_CM."""
    distance = eyes.get_distance_cm()
    # The sensor returns None when nothing is in range, so check for that.
    if distance is None:
        return False
    return distance < STOP_DISTANCE_CM


def flash_red_and_yellow(times=4):
    """Blink the hub's button light red and yellow as a warning."""
    for _ in range(times):
        hub.status_light.on('red')
        wait_for_seconds(0.15)
        hub.status_light.on('yellow')
        wait_for_seconds(0.15)
    hub.status_light.on('white')   # back to normal when done


# ---- Main program: this runs over and over until you press Stop ----
hub.light_matrix.show_image('HAPPY')   # little smiley so you know it started

while True:
    if something_is_too_close():
        # Obstacle ahead! React.
        hub.light_matrix.show_image('NO')   # frowny face
        wheels.stop()
        flash_red_and_yellow()              # warning lights!

        # Back up a bit so we have room to turn.
        wheels.start(0, -DRIVE_SPEED)
        wait_for_seconds(BACKUP_TIME)
        wheels.stop()

        # Spin away from the obstacle (turn in place).
        wheels.move_tank(TURN_DEGREES, 'degrees', DRIVE_SPEED, -DRIVE_SPEED)

        hub.light_matrix.show_image('HAPPY')
    else:
        # Path is clear, keep cruising forward.
        # start(steering, speed): steering 0 means go straight.
        wheels.start(0, DRIVE_SPEED)

    # Small pause so the sensor gets checked many times per second.
    wait_for_seconds(0.05)
