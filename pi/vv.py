import os, io
from google.cloud import vision
import pandas as pd
import cv2
import time
import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
crr = credentials.Certificate("C:\\Users\\HARSH SHARMA\\Desktop\\team stackoverflow\\sjce-hack-firebase-adminsdk-2bt7a-05950e373c.json")
"""cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  "type": "service_account",
  "project_id": "parking-3a32b",
  "private_key_id": "5decc7a0812a712ed2466270cef61233be3e6057",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCp0mV8ZyNlzqtX\n+c6NdP9FssNVXG0Y2RaQLPoUV8EctWh0vLIXvaBGf9J5GWfZAHAJb7op4Poq+gb/\n6YJmx/Ut6Z1juwNIEe5dEsX6GN0hJbWr0IlHkPRTNZlwEqxQTcLKdclxL8HvnV6l\n8AF36PQP1zYUC3i4Q3U9uDDQ6myrtB1lbeu+6Lsupm/FiFMFF1WDkyxZL+S1LDjS\n/XVMocbuQvzc7s/rfneuaXu0deCvJcMx1JC2thv9jK/7qXglsDQ595qsCfmmH5wI\nbLXmC7HlO4Ub9Ea7WuyyDk9RL4AEWsxMTKt/XetVSQMVjXozst8RQqyA4/EnfeLV\nGuEN/eLnAgMBAAECggEAI2UeUOkASDpknRAMfJBLml/Rdauvc3Pfz4oIT5AgyFaJ\nIHep2OfljXwbxrDEY8bDEzxtvUfObIGzTsiBLOH1WK3t53j1jKJsH4sHp4JiKIP/\nEwICct+kBOnRgrnpn00t0dvt8gDlt4cB0K0u6SqtH9YXx+LCNQmeWJBY4FpT7w9i\n/HW4Nm+qxfHnRm/02EOQwpUNleILYWizgTH/YuAMd0ZFxAjFvjTZMQUya+Bto8tX\nTznARZUhAWGzkGwktwt85N+B8rNBsMAvcK6aI8OgUcdMOuDQjJ3njh4qwzSjBjUL\nEjKuY6TGIrIuVWHmt7ucSa7sfrSyWnw0ddpAJ/OVEQKBgQDRAqzXpIL3Izff2m+3\nB7mpxQ/EpdENsOIGOL74XBJ4nfYVXjRP4eFqORpsF2arhk8kvXLiaOg5VFfRIRTQ\nyhDDm+mdRnRzF2n3UFvpOM5bFJUwwoCi62M0achCg/l8Kgb/0tEo/UTObD5gOvTA\nK1ZkiKc6bnZyiYJ9TDfcgYZVUQKBgQDQAEXguGQTPCNIXbvXwv9AJXIAG6fCHu3s\n4s1JoxosnqUZ521pOFpo2pJJuGMrX002pN1iaccgnsqul5EBhRgSKaS407cCaSdh\n2girRb5t4z03qYYq0XyQ5YUzrIcTxtW6hABIVnb5hHpYMh/hH/9ezM2+mcG6MWur\nNvRHT8cGtwKBgCEJcjaXu1fDClbo2RWuM+ugyXBE4XlvhxqCp7TsIMNN/JK+FDi4\nNIAszH9fZ4wfK61cAKfG+0XsjgDxYK/r8KBqqY+BjnCOt+IuooiHwR5mb3qIk/qs\niD7FpbDV2X6FyhtvwD3hYpnaRDXDu+IQN5SmgQBca36JO8YAYSgKlSgxAoGBAI0u\n4j96aVM1Cq3gEdSOIzujLxIrs17sJ4sXF0jYULfgpyhCEd3NxnBNi+ZGJeoWsg5Z\nMXvPWL4nimOftWlWsdQCODDMY/ha78RXfnLi0DM+fxr9EniV4PtpD1TX0of1+rSz\nTI3NQsxyw6iBvWnNkkUCttSdAQYk7XQ1xPFykSFZAoGAdh+5haA9PbICjXe1L7jE\ni3Zlzl29LD8cTg8KFGQLqgBhAf2pZWyx+ifjg4JW4TgJ2csdMWkA22tn6oA837aw\n4xeZxuYdv87x2tFXALetsHt8o/wIaqmVjx/xmHwgSGR+a7j4ohlUdKFLgtca35Pf\nBOqyJB9GfX37I8kWT8jAD+c=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-5dz08@parking-3a32b.iam.gserviceaccount.com",
  "client_id": "111339240162551914465",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-5dz08%40parking-3a32b.iam.gserviceaccount.com"
}
)"""
default_app = firebase_admin.initialize_app(crr)
db = firestore.client()
users_ref = db.collection(u'numberplate').document(u"TOHxHAzbXruzzxLNFjHM")

#document(u"TOHxHAzbXruzzxLNFjHM").
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:\\Users\\HARSH SHARMA\\Videos\\snap\\myparking-266110-934b985df050.json"

client = vision.ImageAnnotatorClient()

#file_name = 'frame0.jpg'
vidcap = cv2.VideoCapture('C:\\Users\\HARSH SHARMA\\Desktop\\team stackoverflow\\car.mp4')
success,image = vidcap.read()
count = random.randint(1,100);
while vidcap.isOpened():
    
    
    success,image = vidcap.read()
    cv2.imshow("frame",image)
        

    k = cv2.waitKey(1)
    if k==ord("q"):
        cv2.imwrite("C:\\Users\\HARSH SHARMA\\Videos\\snap\\frame%d.jpg" % count, image)
        image_path = f'C:\\Users\\HARSH SHARMA\\Videos\\snap\\frame%d.jpg'%count

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
        users_ref.set({
            u"TOHxHAzbXruzzxLNFjHM": {
                'plate': stri,'time':firestore.SERVER_TIMESTAMP
           
        }})   
        print(stri)
        

    if k == ord("e"):
        break
cv2.waitKey(0)
vidcap.release()
cv2.destroyAllWindows()
    

