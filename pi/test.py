from picamera import PiCamera
from gpiozero import Servo

from time import sleep
import RPi.GPIO as GPIO
import time
import os, io
from google.cloud import vision
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
camera = PiCamera()

#Pin Configuration
servo1 = 26
servo2 = 20
irEntry = 19
irExit = 12
irSelfPark = 21
led1 = 3
led2 = 27
led3 = 9
led4 = 5
ir1 = 2
ir2 = 17
ir3 = 10
ir4 = 0
currentStatus = [0,0,0,0]
finalStatus = [0,0,0,0]
c= 0
#Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo1,GPIO.OUT)
GPIO.setup(servo2,GPIO.OUT)
GPIO.setup(irEntry,GPIO.IN)
GPIO.setup(irExit,GPIO.IN)
GPIO.setup(irSelfPark,GPIO.IN)
GPIO.setup(ir1,GPIO.IN)
GPIO.setup(ir2,GPIO.IN)
GPIO.setup(ir3,GPIO.IN)
GPIO.setup(ir4,GPIO.IN)
GPIO.setup(led1,GPIO.OUT)
GPIO.setup(led2,GPIO.OUT)
GPIO.setup(led3,GPIO.OUT)
GPIO.setup(led4,GPIO.OUT)
def ocr():
    with io.open(image_path, 'rb') as image_file:
            content = image_file.read()

    # construct an iamge instance
    image = vision.types.Image(content=content)

    """
    # or we can pass the image url
    image = vision.types.Image()
    image.source.image_uri = 'https://edu.pngfacts.com/uploads/1/1/3/2/11320972/grade-10-english_orig.png'
    """

    # annotate Image Response
    response = client.text_detection(image=image)  # returns TextAnnotation
    df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    for text in texts:
        df = df.append(
            dict(
                locale=text.locale,
                description=text.description
            ),
            ignore_index=True
        )

    ll=list(df['description'][0])
    stri = " "
    i=0
    while i<8:
        stri = stri+ll[i]
        i=i+1
    # users_ref.set({
    #     u"TOHxHAzbXruzzxLNFjHM": {
    #         'plate': stri,'time':firestore.SERVER_TIMESTAMP
        
    # }})   
    print(stri)

def Entry():
    if not GPIO.input(irEntry):
        s1.ChangeDutyCycle(6)
        #camera.start_preview();
        sleep(1)
        print("Capturing")
        camera.capture("capture.png")
        ocr()
        while True:
            if not GPIO.input(irExit):
                s1.ChangeDutyCycle(2.5)
                sleep(2)
                #camera.stop_preview();
                return 1
    else:
        return 0
                
def Exit():
    if not GPIO.input(irExit):
        s1.ChangeDutyCycle(6)
        while True:
            if not GPIO.input(irEntry):
                s1.ChangeDutyCycle(2.5)
                sleep(3)
                return
 
#Init      
    
s1=GPIO.PWM(servo1,50)
s2=GPIO.PWM(servo2,50)
s1.start(2.5)
s2.start(2.5)
GPIO.output(led1,False)
GPIO.output(led2,False)
GPIO.output(led3,False)
GPIO.output(led4,False)
print("IR Sensor Ready.....")
print(" ")
DutyCycle = 6
entering = True
try:
    
    while True:
        if GPIO.input(ir1):
            GPIO.output(led1,True)
            
        else:
            print("Spot 1 Filled")
            GPIO.output(led1,False)
            
          
          
        if GPIO.input(ir2):
            GPIO.output(led2,True)
           
        else:
            print("Spot 2 Filled")
            GPIO.output(led2,False)
         
            
        if GPIO.input(ir3):
            GPIO.output(led3,True)
            finalStatus[2] = 0
        else:
            print("Spot 3 Filled")
            GPIO.output(led3,False)
            
          
          
        if GPIO.input(ir4):
            GPIO.output(led4,True)
            
        else:
            print("Spot 4 Filled")
            GPIO.output(led4,False)
            

        c=0
        if(Entry() == 1):
            c=1
        if(c==0):
            Exit()
            
except KeyboardInterrupt:
    GPIO.cleanup()
#camera.start_preview();
#sleep(10);
#camera.stop_preview();

