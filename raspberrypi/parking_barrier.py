from picamera import PiCamera
from gpiozero import Servo
import os,io
from time import sleep
import RPi.GPIO as GPIO
import time
camera = PiCamera()

# Import database module.
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials,firestore
import datetime
from datetime import timedelta
cred = credentials.Certificate("cred.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sjce-hack.firebaseio.com'
})
db = firestore.client()
refMatchplateCollection = db.collection(u'matchplates')
refUserCollection = db.collection(u'users')
refParkingCollection = db.collection(u'parkingLots')
refPaymentCollection = db.collection(u'payments')


#Vision
from google.cloud import vision
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"cred.json"
client = vision.ImageAnnotatorClient()
image_path = 'image.jpg'


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


    # annotate Image Response
    response = client.text_detection(image=image)  # returns TextAnnotation
    # df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    print(texts)
    # for text in texts:
    text = texts[0].description
    print(text)
    text = text.replace("\n",'').replace(' ','')
    length = len(text) - 4
    text1 = text[length:]
    return text1[:4].splitlines()[0]

def Entry():
    if not GPIO.input(irEntry):
       
        #camera.start_preview();
        sleep(1)
        print("Capturing")
        camera.capture(image_path)
        text = ocr()
        print("OCR Result Entry")
        print(text)
       
       
        matchPlateObj = refMatchplateCollection.document(text).get().to_dict()
        print(matchPlateObj)
        if(matchPlateObj!=None):
            s1.ChangeDutyCycle(6)
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            time1 = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            print(date)
            print(time1)
            refUserCollection.document(matchPlateObj['phone']).set({
                u'isParkedAt':u'Parking model'
            }, merge=True)
            spotsFilled = refParkingCollection.document("F86vVn7OQnZTYak9zFcH").get().to_dict()['spotsFilled']
            refParkingCollection.document("F86vVn7OQnZTYak9zFcH").set({
                u'spotsFilled':spotsFilled + 1,
            },merge=True)
        while True:
            if not GPIO.input(irExit):
                s1.ChangeDutyCycle(2.5)
                sleep(5)
                return 1
    else:
        return 0
               
def Exit():
    if not GPIO.input(irExit):
        s1.ChangeDutyCycle(6)
        while True:
            if not GPIO.input(irEntry):
                s1.ChangeDutyCycle(2.5)
                sleep(5)
                datetimeFormat = '%H:%M:%S'
                print("Capturing")
                camera.capture(image_path)
                text = "1234"
                print("OCR Result Exit")
                print(text)
                matchPlateObj = refMatchplateCollection.document(text).get().to_dict()
                print(matchPlateObj)
                if(matchPlateObj!=None):
                    ts = time.time()
                    userObj = refUserCollection.document(matchPlateObj['phone']).get().to_dict()
                    refPaymentCollection.document(userObj['phone']).set({
                        u"phone":userObj['phone'],
                        u"cost":50
                    })
                    refUserCollection.document(matchPlateObj['phone']).set({
                        u"isParkedAt":u""
                    },merge=True)
                    spotsFilled = refParkingCollection.document("F86vVn7OQnZTYak9zFcH").get().to_dict()['spotsFilled']
                    refParkingCollection.document("F86vVn7OQnZTYak9zFcH").set({
                        u'spotsFilled':spotsFilled - 1,
                    },merge=True)
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
       
        if not GPIO.input(irSelfPark):
            s2.ChangeDutyCycle(2.5)
        else:
            if(db.collection(u'vip').document(u'parkingspace').get().to_dict()['unlocked']):
                s2.ChangeDutyCycle(6)
            else:
                s2.ChangeDutyCycle(2.5)
       
        if GPIO.input(ir1):
            GPIO.output(led1,True)
           
        else:
            print("Spot 1 Filled");
            GPIO.output(led1,False)
           
         
         
        if GPIO.input(ir2):
            GPIO.output(led2,True)
           
        else:
            print("Spot 2 Filled");
            GPIO.output(led2,False)
         
           
        if GPIO.input(ir3):
            GPIO.output(led3,True)
            finalStatus[2] = 0
        else:
            print("Spot 3 Filled");
            GPIO.output(led3,False)
           
         
         
        if GPIO.input(ir4):
            GPIO.output(led4,True)
           
        else:
            print("Spot 4 Filled");
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