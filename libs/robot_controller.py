"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time




class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""
    def __init__(self):
        """Motors"""
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm = ev3.MediumMotor(ev3.OUTPUT_A)

        """Sensors"""
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")
        self.touch = ev3.TouchSensor()

        """Motor Asserts"""
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm.connected

        """Sensor Asserts"""
        assert self.color_sensor.connected
        assert self.ir_sensor.connected
        assert self.pixy.connected
        assert self.touch.connected

        """more constants"""
        self.MAX_SPEED = 600
    def forward_inches(self, inches, speed=100, stop_action='brake'):
        k = 360 / 4.2
        degrees = k * inches
        self.left_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=stop_action)
        self.right_motor.run_to_rel_pos(position_sp=degrees, speed_sp=speed, stop_action=stop_action)

    def backward(self, inches, speed=100, stop_action='brake'):
        self.forward(inches, -speed, stop_action)
    # done: Implement the Snatch3r class as needed when working the sandbox exercises //s
    # (and delete these comments)

    def front(self, left_speed, right_speed):
        #Drives forwards
        self.right_motor.run_forever(speed_sp=right_speed)
        self.left_motor.run_forever(speed_sp=left_speed)

    def back(self, left_speed, right_speed):
        #Drives Backwards
        self.left_motor.run_forever(speed_sp=-1*left_speed)
        self.right_motor.run_forever(speed_sp=-1 * right_speed)

    def right(self, left_speed):
        #rotates right
        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=-1*left_speed)

    def left(self, left_speed):
        #rotates left
        self.left_motor.run_forever(speed_sp=-1*left_speed)
        self.right_motor.run_forever(speed_sp=left_speed)

    def stop(self):
        """Stops both motors"""
        self.right_motor.stop(stop_action="brake")
        self.left_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.BLACK)
        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.BLACK)

    def arm_up(self):
        """moves the arm up"""
        self.arm.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch.is_pressed:
            time.sleep(0.01)
        self.arm.stop(stop_action="brake")

    def arm_down(self):
        """Repositions the arm to be in the down state"""
        self.arm.run_to_abs_pos(position_sp=0, speed_sp=self.MAX_SPEED)
        self.arm.wait_while(ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running

        ev3.Sound.beep().wait()

    def loop_forever(self):
        self.running = True
        while self.running:
            time.sleep(0.1)

    def shutdown(self):
        self.running = False


