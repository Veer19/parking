import * as functions from 'firebase-function';
var https = require('follow-redirects').https;
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';

var fs = require('fs');
exports.createUser = functions.firestore
    .document('users/{userId}')
    .onCreate((snap, context) => {
      // Get an object representing the document
      // e.g. {'name': 'Marie', 'age': 66}
      const newValue = snap.data();
      var number = newValue.phone;
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
          let revenue = body.toString();
          console.log(revenue)
        });
      
        res.on("error", function (error) {
          console.error(error);
        });
      });
      
      req.end();

    });
