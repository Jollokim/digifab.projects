from gpiozero import Servo
from time import sleep

from gpiozero.pins.pigpio import PiGPIOFactory

factory = PiGPIOFactory()

servo = Servo(4, pin_factory=factory)

servo.mid()

angle = -1
go = True

while True:
    # servo.min()
    if go:
        angle = 0.7
        servo.value = angle
        go = not go
        sleep(2)

    else:
        angle = -1
        go = not go
        servo.value = angle
        sleep(2)