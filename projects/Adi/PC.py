import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import ev3dev.ev3 as ev3
import time
import traceback
import math

class MyDelegate(object):
    def __init__(self, main_frame):
        self.running = True
        self.main_frame = main_frame
        label = ttk.Label(self.main_frame, text="Points: 0")
        label.grid(columnspan=2)
        self.arm = ev3.MediumMotor(ev3.OUTPUT_A)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.touch = ev3.TouchSensor()
        self.MAX_SPEED = 600
        self.sound = ev3.Sound()

    def gameover(self):
        label = ttk.Label(self.main_frame, text="Game Over!")
        label.grid(columnspan=2)

    def arm_up_ev3(self):
        """moves the arm up"""
        self.arm.run_forever(speed_sp=self.MAX_SPEED)
        while not self.touch.is_pressed:
            time.sleep(0.01)
        self.arm.stop(stop_action="brake")

    def shot(self):
        print('recieved')
        """robot was shot!!"""
        arm_up_ev3()
        self.sound.speak("Shot Down, Game Over")


def main():




    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=0, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=1, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=0, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=1, column=2)

    '''Lambda Functions'''

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=2, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: forward_pc(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: forward_pc(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=3, column=0)
    # left_button and '<Left>' key
    left_button['command'] = lambda: left_pc(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Left>', lambda event: left_pc(mqtt_client, left_speed_entry, right_speed_entry))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=3, column=1)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: space_pc(mqtt_client)
    root.bind('<space>', lambda event: space_pc(mqtt_client))

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=3, column=2)
    # right_button and '<Right>' key
    right_button['command'] = lambda: right_pc(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Right>', lambda event: right_pc(mqtt_client, left_speed_entry, right_speed_entry))

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=4, column=1)
    # back_button and '<Down>' key
    back_button['command'] = lambda: back_pc(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: back_pc(mqtt_client, left_speed_entry, right_speed_entry))

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=5, column=0)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=6, column=0)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    # Buttons for quit and exit
    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(main_frame, text="Exit")
    e_button.grid(row=6, column=2)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))

    myDelegate = MyDelegate(main_frame)
    mqtt_client = com.MqttClient(myDelegate)
    mqtt_client.connect_to_ev3()


    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------

def forward_pc(mqtt_client, left_speed_entry, right_speed_entry):
    print("forward")
    mqtt_client.send_message('front_ev3', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def back_pc(mqtt_client, left_speed_entry, right_speed_entry):
    print("backwards")
    mqtt_client.send_message('back_ev3', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def right_pc(mqtt_client, left_speed_entry, right_speed_entry):
    print("turning right")
    mqtt_client.send_message('right_ev3', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def left_pc(mqtt_client, left_speed_entry, right_speed_entry):
    print('turning left')
    mqtt_client.send_message('left_ev3', [int(left_speed_entry.get()), int(right_speed_entry.get())])


def space_pc(mqtt_client):
    print('stopping')
    mqtt_client.send_message('stop_ev3')


def send_up(mqtt_client):
    print("raising")
    mqtt_client.send_message("arm_up_ev3")


def send_down(mqtt_client):
    print("lowering")
    mqtt_client.send_message("arm_down_ev3")


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
