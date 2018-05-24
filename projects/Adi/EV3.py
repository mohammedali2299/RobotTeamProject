#!/usr/bin/env python3


import mqtt_remote_method_calls as com
import controller as robot
import time


class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""
    def __init__(self):
        self.running = True



def main():
    robot1 = robot.Snatcher()
    mqtt_client = com.MqttClient(robot1)
    mqtt_client.connect_to_pc()
    dc = DataContainer()
    btn = robot1.button
    btn.on_enter = lambda state: btnpress(state, dc)
    remote = robot1.remote

    while dc.running:
        btn.process()
        time.sleep(0.1)

        if remote.red_up == 1:
            mqtt_client.send_message("shot", [])
            break

    robot1.Sound.speak("Game Over")
    robot1.right_motor.stop(stop_action='brake')
    robot1.left_motor.stop(stop_action='brake')

    robot1.arm_up_ev3()
    robot1.arm_down_ev3()

    for k in range(5):
        robot1.leds(robot1.leds.LEFT, robot1.leds.RED)
        robot1.leds(robot1.leds.RIGHT, robot1.leds.RED)
        time.sleep(0.1)
        robot1.leds(robot1.leds.LEFT, robot1.leds.BLACK)
        robot1.leds(robot1.leds.RIGHT, robot1.leds.BLACK)




def btnpress(button_state, dc):
    if button_state:
        dc.running = False

def game_over(mqtt_client):
    mqtt_client.send_message("gameover", [])




# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
