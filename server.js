const express = require('express'),
    bodyParser = require('body-parser'),
    cors = require('cors'),
    fs = require("fs"),
path = require("path"),
    listSigner = require('./list_signer'),
    detailSigner = require('./detail_signer'),
    app = express();
let port=3515;
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(cors());

const configPath = path.join(process.execPath, "../","./config.json");
let isConfigExist = fs.existsSync(configPath);

let jsonConfig = null
if (isConfigExist) {
  jsonConfig = JSON.parse(fs.readFileSync(configPath, "utf8"));
}
if (jsonConfig.port) {
    port = jsonConfig.port
}

app.post('/api/v1/toutiao/list/sign', (req, res) => {
    let url=req.body.url,
        cookie = req.body.cookie || '';

    let signature = listSigner.sign(url, cookie)
    if (url) {
        url = url + '&_signature=' + signature;
    }
    res.json({
        url,
        ua:listSigner.userAgent
    });
})

app.post('/api/v1/toutiao/detail/sign', (req, res) => {
    let nonce = req.body.nonce,
        url = req.body.url || '';
    res.json({
        ua:detailSigner.userAgent,
        cookie:detailSigner.sign(url, nonce)
    });
})
app.get('/api/v1/version', (req, res) => {
    res.json({
        status: "0",
        message: "ok",
        data: {
            version: "1.0.0",
        }
    });
})

app.listen(port, () => {
    console.log(`listening on:http://127.0.0.1:${port}`);
})