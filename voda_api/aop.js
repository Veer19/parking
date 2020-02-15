var https = require('follow-redirects').https;
var fs = require('fs');
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
var options = {
  'method': 'POST',
  'hostname': 'partner.vodafone.in',
  'path': '/services2/adviceofprivacy/3/rest/sms?address=tel%253A%252B919822003837&callbackUrl=http%253A%252F%252Fpartner.vodafone.in%253A9999%252FrestServer&operation=requestConsent',
  'headers': {
    'Content-Type': 'application/x-www-form-urlencoded',
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

req.end();