"""
Functions for moving the robot FORWARD and BACKWARD.
Authors: David Fisher, David Mutchler and mohammed ali.
"""  # done: 1. PUT YOUR NAME IN THE ABOVE LINE.

# TODO: 2. Implment forward_seconds, then the relevant part of the test function.
#          Test and correct as needed.
#   Then repeat for forward_by_time.
#   Then repeat for forward_by_encoders.
#   Then repeat for the backward functions.

import ev3dev.ev3 as ev3
import time

def test_forward_backward():
    """
    Tests the forward and backward functions, as follows:
      1. Repeatedly:
          -- Prompts for and gets input from the console for:
             -- Seconds to travel
                  -- If this is 0, BREAK out of the loop.
             -- Speed at which to travel (-100 to 100)
             -- Stop action ("brake", "coast" or "hold")
          -- Makes the robot run per the above.
      2. Same as #1, but gets inches and runs forward_by_time.
      3. Same as #2, but runs forward_by_encoders.
      4. Same as #1, 2, 3, but tests the BACKWARD functions.
    """
    forward_seconds(15, 200, 'brake')

def forward_seconds(seconds, speed, stop_action):
    """
    Makes the robot move forward for the given number of seconds at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the given stop_action.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    left_motor.time_sp = seconds
    right_motor.time_sp = seconds
    left_motor.run_forever(speed_sp=speed, stop_action=stop_action)
    right_motor.run_forever(speed_sp=speed, stop_action=stop_action)
    time.sleep(seconds)
    left_motor.stop()
    right_motor.stop()

    ev3.Sound.beep().wait()


def forward_by_time(inches, speed, stop_action):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      0. Compute the number of seconds to move to achieve the desired distance.
      1. Start moving.
      2. Sleep for the computed number of seconds.
      3. Stop moving.
    """
    # Connect two large motors on output ports B and C
    left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
    right_motor = ev3.LargeMotor(ev3.OUTPUT_C)

    # Check that the motors are actually connected
    assert left_motor.connected
    assert right_motor.connected

    deg = 90 * inches
    time = deg / speed

    left_motor.run_timed(speed_sp=speed, time_sp=time, stop_action = 'brake')
    right_motor.run_timed(speed_sp=speed, time_sp=time, stop_action='brake')
    time.sleep(time)

    left_motor.stop()
    right_motor.stop()

    ev3.Sound.beep().wait()

def forward_by_encoders(inches, speed, stop_action):
    """
    Makes the robot move forward the given number of inches at the given speed,
    where speed is between -100 (full speed backward) and 100 (full speed forward).
    Uses the algorithm:
      1. Computea the number of degrees the wheels should spin to achieve the desired distance.
      2. Move until the computed number of degrees is reached.
    """


def backward_seconds(seconds, speed, stop_action):
    """ Calls forward_seconds with negative speeds to achieve backward motion. """


def backward_by_time(inches, speed, stop_action):
    """ Calls forward_by_time with negative speeds to achieve backward motion. """


def backward_by_encoders(inches, speed, stop_action):
    """ Calls forward_by_encoders with negative speeds to achieve backward motion. """


test_forward_backward()