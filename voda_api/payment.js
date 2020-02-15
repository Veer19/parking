var https = require('follow-redirects').https;
var fs = require('fs');

var options = {
  'method': 'POST',
  'hostname': 'partner.vodafone.in',
  'path': '/services2/asepay/2_1/payment/tel:+919923405494/transactions/amount',
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

var postData = JSON.stringify({"amountTransaction":{"endUserId":"tel:+919923405494","paymentAmount":{"chargingInformation":{"code":"DWAP_VCU0000_PPU_DES06885001","description":["NOKIA WALLPAPER 7"]},"chargingMetaData":{"onBehalfOf":"IBM SDP","purchaseCategoryCode":"WALLPAPER","channel":"USSD"}},"referenceCode":"kannin-33333-0","transactionOperationStatus":"Charged"}});

req.write(postData);

req.end();