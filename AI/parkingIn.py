import cv2
import numpy as np
import vehicles
import time
cnt_up=0
cnt_down=0


#Firebase Setup
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
users_ref = db.collection(u'spaces').document(u"Txi6nwvuHdRSvIVGwDNQ")

"""Txi6nwvuHdRSvIVGwDNQ"""

"""rvdFPEAFjaHngpmTRmh3"""

"C:\\Users\\HARSH SHARMA\\Desktop\\team stackoverflow\\surveillance.m4v"
cap=cv2.VideoCapture("C:\\Users\\HARSH SHARMA\\Desktop\\team stackoverflow\\hars.mp4")

#Get width and height of video

w=cap.get(3)
h=cap.get(4)
frameArea=h*w
areaTH=frameArea/420

#Lines
line_up=int(2*(h/5))
line_down=int(3*(h/5))

up_limit=int(1*(h/5))
down_limit=int(4*(h/5))

print("Red line y:",str(line_down))
print("Blue line y:",str(line_up))
line_down_color=(255,0,0)
line_up_color=(255,0,255)
pt1 =  [0, line_down]
pt2 =  [w, line_down]
pts_L1 = np.array([pt1,pt2], np.int32)
pts_L1 = pts_L1.reshape((-1,1,2))
pt3 =  [0, line_up]
pt4 =  [w, line_up]
pts_L2 = np.array([pt3,pt4], np.int32)
pts_L2 = pts_L2.reshape((-1,1,2))

pt5 =  [0, up_limit]
pt6 =  [w, up_limit]
pts_L3 = np.array([pt5,pt6], np.int32)
pts_L3 = pts_L3.reshape((-1,1,2))
pt7 =  [0, down_limit]
pt8 =  [w, down_limit]
pts_L4 = np.array([pt7,pt8], np.int32)
pts_L4 = pts_L4.reshape((-1,1,2))

#Background Subtractor
fgbg=cv2.createBackgroundSubtractorMOG2(detectShadows=True)

#Kernals
kernalOp = np.ones((3,3),np.uint8)
kernalOp2 = np.ones((5,5),np.uint8)
kernalCl = np.ones((11,11),np.uint8)


font = cv2.FONT_HERSHEY_SIMPLEX
cars = []
max_p_age = 5
pid = 1


while(cap.isOpened()):
    ret,frame=cap.read()
    for i in cars:
        i.age_one()
    fgmask=fgbg.apply(frame)
    fgmask2=fgbg.apply(frame)

    if ret==True:

        ret,imBin=cv2.threshold(fgmask,200,255,cv2.THRESH_BINARY)
        ret,imBin2=cv2.threshold(fgmask2,200,255,cv2.THRESH_BINARY)
        mask=cv2.morphologyEx(imBin,cv2.MORPH_OPEN,kernalOp)
        mask2=cv2.morphologyEx(imBin2,cv2.MORPH_CLOSE,kernalOp)

        mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernalCl)
        mask2=cv2.morphologyEx(mask2,cv2.MORPH_CLOSE,kernalCl)


        countours0,hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        for cnt in countours0:
            area=cv2.contourArea(cnt)
            print(area)
            if area>areaTH:
                m=cv2.moments(cnt)
                cx=int(m['m10']/m['m00'])
                cy=int(m['m01']/m['m00'])
                x,y,w,h=cv2.boundingRect(cnt)

                new=True
                if cy in range(up_limit,down_limit):
                    for i in cars:
                        if abs(x - i.getX()) <= w and abs(y - i.getY()) <= h:
                            new = False
                            i.updateCoords(cx, cy)

                            if i.going_UP(line_down,line_up)==True:
                                cnt_up+=1
                                
                            elif i.going_DOWN(line_down,line_up)==True:
                                doc = users_ref.get().to_dict()
                                if(doc['spotsFilled'] >= doc['numberOfSpots']):
                                    doc['filled'] = 1
                                else:                                        
                                    doc['spotsFilled'] = doc['spotsFilled'] + 1
                                    for i in range(0,len(doc['spots'])):
                                        if(doc['spots'][i]==""):
                                            doc['spots'][i]="1"
                                            break
                                users_ref.set(doc)
                                cnt_down+=1
                                
                            break
                        if i.getState()=='1':
                            if i.getDir()=='down'and i.getY()>down_limit:
                                i.setDone()
                            elif i.getDir()=='up'and i.getY()<up_limit:
                                i.setDone()
                        if i.timedOut():
                            index=cars.index(i)
                            cars.pop(index)
                            del i

                    if new==True: #If nothing is detected,create new
                        p=vehicles.Car(pid,cx,cy,max_p_age)
                        cars.append(p)
                        pid+=1

                cv2.circle(frame,(cx,cy),5,(0,0,255),-1)
                img=cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        for i in cars:
            cv2.putText(frame, str(i.getId()), (i.getX(), i.getY()), font, 0.3, i.getRGB(), 1, cv2.LINE_AA)




        str_up='UP: '+str(cnt_up)
        str_down='DOWN: '+str(cnt_down)
        frame=cv2.polylines(frame,[pts_L1],False,line_down_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L2],False,line_up_color,thickness=2)
        frame=cv2.polylines(frame,[pts_L3],False,(255,255,255),thickness=1)
        frame=cv2.polylines(frame,[pts_L4],False,(255,255,255),thickness=1)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, str_down, (10, 90), font, 0.5, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow('Frame',frame)

        if cv2.waitKey(1)&0xff==ord('q'):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()









