from gpiozero import DistanceSensor, LED, Button
from picamera import PiCamera
from time import sleep

import time

led = LED (21)
button = Button(2)
sensor = DistanceSensor(echo=24, trigger=18)
camera = PiCamera()

distance_to_door = 100
sens_on = False

def switch_sens():
    global sens_on
    sens_on = not sens_on
    

def button_pressed():
    if sens_on:
        switch_sens()
        print("sensor off")
        for i in range(3):
            led.on()
            sleep(1)
            led.off()
            sleep(1)
    else:
        led.on()
        sleep(5)
        
        switch_sens()
        led.off()
        print("sensor on")



def look_for_abnormal():
    distance = sensor.distance*100
    if distance < 100:
        print(f"ABNORMAL DISTANCE: {distance}")
        camera.rotation = 180
        
        moment = time.asctime(time.localtime(time.time()))
        camera.start_recording(f"/home/pi/Desktop/picamvideos/PiSpy - {moment}.h264")
        sleep(15)

        camera.stop_recording()
        
    else:
        print(f"distance: {distance}")



button.when_released = button_pressed       

while True:
    
    if sens_on:
        look_for_abnormal()
        sleep(0.05)
    
