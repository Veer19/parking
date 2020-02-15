const functions = require('firebase-functions');
var https = require('follow-redirects').https;
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
const admin = require('firebase-admin');
admin.initializeApp();

const db = admin.firestore();

var fs = require('fs');
exports.createUser = functions.firestore
    .document('tempUsers/{userId}')
    .onCreate((snap, context) => {

    
      
      let userData = snap.data()
      var number = userData.phone;
      var options = {
        'method': 'GET',
        'hostname': 'partner.vodafone.in',
        'path': '/services2/subrev/1/revenue/tel%3A%2B91'+number,
        'headers': {
          'Content-Type': 'application/json',
          'X-Forwarded-For': '192.168.56.1',
          'Authorization': 'Basic NmViNzcwYThjMGUxMGIzYjc4ZThmOTU1Y2FjZDRkM2I6QSMrUFE2WGM='
        },
        'maxRedirects': 20
      };
      
      var req = https.request(options, function (res) {
        var chunks = [];
      
        res.on("data", function (chunk) {
          chunks.push(chunk);
        });
      
        res.on("end", function (chunk) {
          var body = Buffer.concat(chunks);
          userData.revenue = body.toString().revenue.arpu;

        });
      
        res.on("error", function (error) {
          console.error(error);
        });
      });
      
      req.end();


      var options = {
        'method': 'GET',
        'hostname': 'partner.vodafone.in',
        'path': '/services2/subage/1/subscriber/age/tel%3A%2B91'+number,
        'headers': {
          'Content-Type': 'application/json',
          'X-Forwarded-For': '192.168.56.1',
          'Authorization': 'Basic NmViNzcwYThjMGUxMGIzYjc4ZThmOTU1Y2FjZDRkM2I6QSMrUFE2WGM='
        },
        'maxRedirects': 20
      };
      
      var req = https.request(options, function (res) {
        var chunks = [];
      
        res.on("data", function (chunk) {
          chunks.push(chunk);
        });
      
        res.on("end", function (chunk) {
          var body = Buffer.concat(chunks);
          userData.dob = body.toString().subscriber.age.dob;
          userData.gender = body.toString().subscriber.age.gender;
          userData.age = body.toString().subscriber.age.age;
        });
      
        res.on("error", function (error) {
          console.error(error);
        });
      });
      
      req.end();


      var options = {
        'method': 'GET',
        'hostname': 'partner.vodafone.in',
        'path': '/services2/devicedetails/1/deviceDetails/tel:+91'+number,
        'headers': {
          'Content-Type': 'application/json',
          'X-Forwarded-For': '192.168.56.1',
          'Authorization': 'Basic NmViNzcwYThjMGUxMGIzYjc4ZThmOTU1Y2FjZDRkM2I6QSMrUFE2WGM='
        },
        'maxRedirects': 20
      };
      
      var req = https.request(options, function (res) {
        var chunks = [];
      
        res.on("data", function (chunk) {
          chunks.push(chunk);
        });
      
        res.on("end", function (chunk) {
          var body = Buffer.concat(chunks);
          userData.device = body.toString().deviceDetails.make + " : " + body.toString().deviceDetails.model;
          console.log("UserData")
          console.log(userData)
        });
        res.on("error", function (error) {
          console.error(error);
        });
      });
      
      req.end();
      console.log("Empty")

      console.log(userData)
      db.doc('users/'+userData.phone).set(userData);

    });
exports.sendOTP = functions.firestore
.document('users/{userId}')
.onCreate((snap, context) => {
    let phone = snap.data().phone
    var otp="123";
    var options = {
    'method': 'POST',
    'hostname': 'partner.vodafone.in',
    'path': '/services2/sendsms/2_0/smsmessaging/outbound/59840201/requests',
    'headers': {
        'Content-Type': 'application/json',
        'X-Forwarded-For': '192.168.56.1',
        'Authorization': 'Basic NmViNzcwYThjMGUxMGIzYjc4ZThmOTU1Y2FjZDRkM2I6QSMrUFE2WGM='
    },
    'maxRedirects': 20
    };

    var req = https.request(options, function (res) {
    var chunks = [];

    res.on("data", function (chunk) {
        chunks.push(chunk);
    });

    res.on("end", function (chunk) {
        var body = Buffer.concat(chunks);
        console.log(body.toString());
    });

    res.on("error", function (error) {
        console.error(error);
    });
    });

    var postData = JSON.stringify({"outboundSMSMessageRequest":{"address":["tel:+91"+phone],"outboundSMSTextMessage":{"message":otp},"senderAddress":"59840201"}});

    req.write(postData);

    req.end();
})