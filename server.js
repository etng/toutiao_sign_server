const express = require('express'),
    bodyParser = require('body-parser'),
    cors = require('cors'),
    listSigner = require('./list_signer'),
    detailSigner = require('./detail_signer'),
    port=3515,
    app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: true}));
app.use(cors());

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

app.listen(port, () => {
    console.log(`listening on:http://127.0.0.1:${port}`);
})