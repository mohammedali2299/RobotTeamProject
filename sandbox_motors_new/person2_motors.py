"""
Functions for SPINNING the robot LEFT and RIGHT.
Authors: David Fisher, David Mutchler and Adi Sethupathy.
"""  # done: 1. PUT YOUR NAME IN THE ABOVE LINE.

# done: 2. Implment spin_left_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for spin_left_by_time.
#   Then repeat for spin_left_by_encoders.
#   Then repeat for the spin_right functions.


import ev3dev.ev3 as ev3
import time


left = ev3.LargeMotor(ev3.OUTPUT_B)
right = ev3.LargeMotor(ev3.OUTPUT_C)


def test_spin_left_spin_right():
    """
    Tests the spin_left and spin_right functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets degrees and runs spin_left_by_time.
      3. Same as #2, but runs spin_left_by_encoders.
      4. Same as #1, 2, 3, but tests the spin_right functions.
    """
    while True:
        speed = int(input("-100 to 100"))
        time = int(input('how many seconds'))
        spin_left_seconds(time*100, speed, "brake")


def spin_left_seconds(seconds, speed, stop_action):
    """
    Makes the robot spin in place left for the given number of seconds at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the given stop_action.
    """
    left.run_forever(speed_sp = speed * 8)
    right.run_forever(speed_sp = -8 * speed)

    time.sleep(seconds)

    left.stop()
    right.stop()

    left.stop_action = stop_action
    right.stop_action = stop_action



def spin_left_by_time(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    time = degrees / speed

    left.run_forever(speed_sp = speed)
    right.run_forever(speed_sp=speed)

    time.sleep(time)

    left.stop()
    right.stop()

    left.stop_action = stop_action
    right.stop_action = stop_action


def spin_left_by_encoders(degrees, speed, stop_action):
    """
    Makes the robot spin in place left the given number of degrees at the given speed,
    where speed is between -100 (full speed spin_right) and 100 (full speed spin_left).
    Uses the algorithm:
      1. Compute the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """

    left.run_to_rel_pos(degrees, speed_sp = speed)
    right.run_to_rel_pos(degrees, speed_sp = speed)
    time.sleep(3.0)
    left.stop()
    right.stop()

    left.stop_action = stop_action
    right.stop_action = stop_action



def spin_right_seconds(seconds, speed, stop_action):
    """ Calls spin_left_seconds with negative speeds to achieve spin_right motion. """

    spin_left_seconds(seconds, -1 * speed, stop_action)


def spin_right_by_time(degrees, speed, stop_action):
    """ Calls spin_left_by_time with negative speeds to achieve spin_right motion. """

    spin_left_by_time(degrees, -1 * speed, stop_action)


def spin_right_by_encoders(degrees, speed, stop_action):
    """ Calls spin_left_by_encoders with negative speeds to achieve spin_right motion. """

    spin_left_by_encoders(degrees, -1 * speed, stop_action)


test_spin_left_spin_right()