const firebaseConfig = {
    apiKey: "XXXXXXXXXXXXXXXXXXXXXXXXX",
    authDomain: "vodapark-20.firebaseapp.com",
    databaseURL: "https://vodapark-20.firebaseio.com",
    projectId: "vodapark-20",
    storageBucket: "vodapark-20.appspot.com",
    messagingSenderId: "820475761120",
    appId: "1:820475761120:web:90bfb7f23ae1074dc9db85",
    measurementId: "G-4SYSJC697M"
};
import firebase from 'firebase'
import 'firebase/firestore'
firebase.initializeApp(firebaseConfig)
const db = firebase.firestore();
const auth = firebase.auth();
export default {db,auth}
