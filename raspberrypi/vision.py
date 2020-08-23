# crr = credentials.Certificate("cred.json")
import random
import os, io
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore
from google.cloud import vision

image_path = f'capture.jpg'
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
    # df = pd.DataFrame(columns=['locale', 'description'])

    texts = response.text_annotations
    # for text in texts:
    text = texts[0].description[:13]
    print(text)

# default_app = firebase_admin.initialize_app(crr)
# db = firestore.client()
# users_ref = db.collection(u'numberplate').document(u"TOHxHAzbXruzzxLNFjHM")

#document(u"TOHxHAzbXruzzxLNFjHM").
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"cred.json"

client = vision.ImageAnnotatorClient()
ocr()