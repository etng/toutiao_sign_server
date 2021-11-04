# as: A1254F76D892626
# cp: 5F6832E692161E1

import execjs
import requests
# as: A1954FC6E822643
# cp: 5F68E24694135E1
ASCPContext = execjs.compile(open("ascp.js", "r", encoding="utf-8").read())
SIGNContext = execjs.compile(open("sign_node.js", "r",encoding="utf-8").read())
userAgent = "Mozilla/5.0 (win32) AppleWebKit/537.36 (KHTML, like Gecko) jsdom/16.4.0"

def get_sign(_as, _cp, cookie, max_behot_time="0", first=False):
    # cookie =  "ttcid=6cf3c9f384694a0689ed95c9989ea93c10; WEATHER_CITY=%E5%8C%97%E4%BA%AC; MONITOR_WEB_ID=5107b035-cdde-44d3-8f1a-0f3ac3f7c9d2; csrftoken=e816e8750952c88e17dff81d60866fc6; tt_webid=6874785795879011854; s_v_web_id=verify_kfc04dc0_Y8rwExIV_mqfh_4ktV_8WjJ_qyr93WmE37oF; tt_webid=6874785795879011854; tt_scid=BmW10XZi53Pp-2k7ksT7tZ.iX-kFDOgFwfBbVdmrMQ-RLXgMyoUSBBvDmDlwyZVB167c; __tasessionId=j18cptglc1600660816346",

    url = "https://www.toutiao.com/toutiao/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=%s&cp=%s"%(_as, _cp)
    if not first:
        url = "https://www.toutiao.com/toutiao/api/pc/feed/?max_behot_time=%s&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=%s&cp=%s"%(max_behot_time, _as, _cp)
    print("sign URL", url)
    # userAgent, cookie, url
    return SIGNContext.call("getSign", userAgent, cookie, url)
def get_content(max_behot_time="0", first=False):
    obj = ASCPContext.call("a")
    _as = obj["as"]
    _cp = obj["cp"]
    url = "https://www.toutiao.com/api/pc/feed/?"

    # sign = "_02B4Z6wo00f01PlZ20AAAIBBRni2-lEHnnz5XN.AAGFEc47N1u9NKwmHkf1cKgYj4FwbnsJSKAyupbkVa-V8SDC1MNZXbFBcc7p0uqHVVJyca5mPEbHZqLPDkYwh-RW8A0zIZr87cG9DXsU293"
    params = {
        "category": "__all__",
        "utm_source": "toutiao",
        "widen": "1",
        "tadrequire": "true",
        "as": _as,
        "cp": _cp,
    }

    请在此处写入你的cookie
    cookie = ""    
    if first:
        params.update({"min_behot_time": "0"})
        # max_behot_time, _as, _cp, cookie, first=False
        sign = get_sign( _as, _cp, cookie, "0", True)
    else:
        params.update({"max_behot_time": max_behot_time})
        sign = get_sign(_as, _cp, cookie, max_behot_time, False)
    params.update({"_signature": sign})
    # as: "A155EF262852897"
    # category: "__all__"
    # cp: "5F683278B9C7CE1"
    # tadrequire: true
    # utm_source: "toutiao"
    # widen: 1
    headers = {
        "referer": "https://www.toutiao.com/",
        "x-requested-with": "XMLHttpRequest",
        "cookie": cookie,
        "user-agent": userAgent
    }
    r = requests.get(url, params=params, headers=headers)
    data = r.json()["data"]
    # print(r.text)
    for i in data:
        title = i["title"]
        print(title)
    return r.json()["next"]["max_behot_time"]
def run():
    max_behot_time = get_content(first=True)
    
    for i in range(0, 50):
        print("max_behot_time", max_behot_time)
        max_behot_time = get_content(max_behot_time=max_behot_time, first=False)

run()