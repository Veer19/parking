var https = require('follow-redirects').https;
var fs = require('fs');
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
var number=9822003837;
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
    console.log(body.toString());
  });

  res.on("error", function (error) {
    console.error(error);
  });
});

req.end();