from gpiozero import Servo
from time import sleep

servo = Servo(17)

servo.mid()
sleep(3)
angle = -1
go = True

while True:
    # servo.min()
    if go:
        angle += 0.1

        if angle >= 0.7:
            go = not go
            continue
        
    else:
        angle -= 0.1
        
        if angle <= -1:
            go = not go
            continue
        
        
    servo.value = angle
        
    sleep(1)