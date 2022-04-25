import cv2
import time

import numpy as np

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep


DEVICE_CENTERX = 240
DEVICE_CENTERY = 320

SHOOT_MARGX = 50
SHOOT_MARGY = 50

cap = cv2.VideoCapture(0)

classes = ['person']

wht = 120

modelConfig = 'yolov3-tiny.cfg'
modelWeights = 'yolov3-tiny.weights'

net = cv2.dnn.readNetFromDarknet(modelConfig, modelWeights)
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

confidence_threshold = 0.5
nms_treshold = 0.3

servox_speed = 0.1
servoy_speed = 0.1


factory = PiGPIOFactory()
servox = Servo(17, pin_factory=factory)
servoy = Servo(27, pin_factory=factory)
servoshoot = Servo(4, pin_factory=factory)

servox.mid()
#servoy.mid()
servoshoot.value = 0.7



def findObjects(outputs, img):
    h_img, w_img, c_img = img.shape

    bbox = []
    classIds = []
    confs = []

    for output in outputs:
        for det in output:
            scores = det[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]

            if confidence > confidence_threshold:
                w, h = int(det[2]*w_img), int(det[3]*h_img)
                x, y = int((det[0]*w_img) - w/2), int((det[1]*h_img) - h/2)

                bbox.append([x, y, w, h])
                classIds.append(classId)
                confs.append(float(confidence))

    indices = cv2.dnn.NMSBoxes(bbox, confs, confidence_threshold, nms_treshold)

    for i in indices:
        i = i[0]
        box = bbox[i]
        x,y,w,h = box[0], box[1], box[2], box[3]

        centerx = x + (w//2)
        centery = y + (h//2)
        print(f'x: {x} y:{y} w:{w} h:{h}')
        print(f'cx: {centerx} cy: {centery}')
        
        if centerx < DEVICE_CENTERX:
            if servox.value+servox_speed < 1:
                servox.value += servox_speed
        elif centerx > DEVICE_CENTERX:
            if servox.value-servox_speed > -1:
                servox.value -= servox_speed
                
        if centery < DEVICE_CENTERY:
            if servoy.value+servoy_speed < 1:
                servoy.value += servoy_speed
        elif centery > DEVICE_CENTERY:
            if servoy.value-servoy_speed > -1:
                servoy.value -= servoy_speed
                
        if centerx < DEVICE_CENTERX+(SHOOT_MARGX/2) and centerx > DEVICE_CENTERX-(SHOOT_MARGX/2):
            print('SHOOOT')
            servoshoot.value = -1
            sleep(2)
            servoshoot.value = 0.7
            


        if classIds[i] == 0:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.putText(img, f'{classes[classId]} {int(confs[i]*100)}%', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
    return indices






fps_start = 0
fps = 0

checkEvery = 10
frameCounter = 0
while True:
    success, img = cap.read()

    """
    
    """
    
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    
    if frameCounter == checkEvery:
        
        fps_end = time.time()
        time_diff = fps_end - fps_start
        fps = int(1/(time_diff))
        fps_start = fps_end

        cv2.putText(img, 'proces', (5, 30), cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 255, 0), 2)
        
        blob = cv2.dnn.blobFromImage(img, 1/255, (wht, wht), [0, 0, 0], 1, crop=False)
        net.setInput(blob)

        layerNames = net.getLayerNames()

        outputNames = [layerNames[i[0]-1] for i in net.getUnconnectedOutLayers()]

        outputs = net.forward(outputNames)

        findObjects(outputs, img)
        
        frameCounter = 0
        
    frameCounter += 1
    
    cv2.rectangle(img, (DEVICE_CENTERX-SHOOT_MARGX, DEVICE_CENTERY-SHOOT_MARGY), (DEVICE_CENTERX+SHOOT_MARGX, DEVICE_CENTERY+SHOOT_MARGY), (0, 0, 255), 2)
    
    
    cv2.imshow("Cam", img)
    cv2.waitKey(1)
