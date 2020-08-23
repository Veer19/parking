# Import database module.
from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sjce-hack.firebaseio.com'
})
ref = db.reference('matchplates/12')
print(ref.get())
"""
all_users = db.child("matchplate").get()
for user in all_users.each():
    userid = user.key()
    inventorydb = db.child("matchplate").child(userid).child("phone")
    print(inventorydb)"""
