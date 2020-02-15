var https = require('follow-redirects').https;
var fs = require('fs');
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
var number;
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

var postData = JSON.stringify({"outboundSMSMessageRequest":{"address":["tel:+91"+number],"outboundSMSTextMessage":{"message":otp},"senderAddress":"59840201"}});

req.write(postData);

req.end();