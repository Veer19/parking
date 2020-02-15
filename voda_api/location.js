var https = require('follow-redirects').https;
var fs = require('fs');
process.env['NODE_TLS_REJECT_UNAUTHORIZED'] = '0';
var number;
var options = {
  'method': 'GET',
  'hostname': 'partner.vodafone.in',
  'path': '/services2/asegetlocation/2_0/location/queries/location?address=tel:+91'+number+'&requestedAccuracy=5000',
  'headers': {
    'Content-Type': 'application/json',
    'X-forwarded-For': '192.168.56.1',
    'Authorization': 'Basic NmViNzcwYThjMGUxMGIzYjc4ZThmOTU1Y2FjZDRkM2I6QSMrUFE2WGM='
  },
  'maxRedirects': 20
};
// 9822003837
// code for payment DWAP_VCIJ0000_PPU
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