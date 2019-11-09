const firebaseConfig = {
    "apiKey": "AIzaSyAxZj2_365R_O6o82f4vwY6M8ir6ykN8tw",
    "authDomain": "sjce-hack.firebaseapp.com",
    "databaseURL": "https://sjce-hack.firebaseio.com",
    "projectId": "sjce-hack",
    "storageBucket": "sjce-hack.appspot.com",
    "messagingSenderId": "100927717855",
    "appId": "1:100927717855:web:8058b4ef832ce5634a446a",
    "measurementId": "G-SE3ESM9E6X"
};
import firebase from 'firebase'
import 'firebase/firestore'
firebase.initializeApp(firebaseConfig)
const db = firebase.firestore();
const auth = firebase.auth();
export default {db,auth}