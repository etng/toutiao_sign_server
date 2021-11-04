import requests
import execjs

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "cookie": "__ac_signature=_02B4Z6wo00f01ZilTmQAAIBBtQ-4ix4ihPWYtULAADntdf; __ac_referer=__ac_blank",
}


__ac_signature_context = execjs.compile(open("detail_content.js").read())


def get_content(url, first=False):
    print(headers)
    r = requests.get(url, headers=headers)
    # print(r.text)
    __ac_nonce = r.headers["set-cookie"].split("; ")[0].split("=")[1]
    # open("a.html", "w").write(r.text)
    if first:
        cookie = __ac_signature_context.call("getAsSignature", __ac_nonce)
        ac_signature = cookie.split("; ")[0].split("=")[1]
        # print(ac_signature, __ac_nonce)
        headers.update(
            {"cookie": f"__ac_nonce={__ac_nonce}; __ac_signature={ac_signature};"}
        )
        get_content(url)
        return
    print(r.text)


url = "https://www.toutiao.com/i6897758777978651143"
get_content(url, first=True)
