import requests
import execjs
from urllib.parse import urlencode
from requests import Session

SESSION = Session()


class Toutiao:
    def __init__(self, user_token):
        # https://www.toutiao.com/c/user/token/MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM/
        # MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM
        self.user_token = user_token
        self.js_runtime_context_sign = Toutiao.init_js_runtime_context("sign_node.js")
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"
        }
        self.last_max_hot_time = "0"

    @classmethod
    def init_js_runtime_context(cls, js_filename):
        with open(js_filename, encoding="UTF-8") as f:
            content = f.read()
            return execjs.compile(content)

    def next_page(self):
        self.req()

    def req(self):
        url = "https://www.toutiao.com/api/pc/feed/?"
        params = {
            "category": "profile_all",
            "utm_source": "toutiao",
            "visit_user_token": self.user_token,
            "max_behot_time": self.last_max_hot_time,
        }
        # https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM&max_behot_time=1588854165000
        # https://www.toutiao.com/api/pc/feed/?category=profile_all&utm_source=toutiao&visit_user_token=MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM&max_behot_time=0

        # _signature: _02B4Z6wo00d01Y7KLgAAAIBAw4T8W6rUfX2OzyqAADwF64

        current_url = url + urlencode(params)
        signature = self.js_runtime_context_sign.call("sign", current_url, "")
        params.update({"_signature": signature})
        # print(signature)
        try:
            r = SESSION.get(url, params=params, headers=self.headers)
            print(r.url)
        except Exception as e:
            print(e)
        print(r.text[:100])
        data = r.json()
        # print(data)
        # print(data["message"])
        list_data = data["data"]
        # print(list_data)
        for lst in list_data:
            title = lst["title"]
            source_url = lst["source_url"]
            print(title, source_url)
        self.last_max_hot_time = data["next"]["max_behot_time"]
        if not data["has_more"]:
            #  没有了。
            print("done!!!")


# https://www.toutiao.com/c/user/token/MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM/
# 这里的token是用户的token
toutiao = Toutiao(
    "MS4wLjABAAAAeBjKNda8D5UNXcu07nCT0uIG9AUU8g38juNhhDcyrgZwzhk3Yn6LHDdTECWL6CeM"
)
toutiao.next_page()
toutiao.next_page()
for i in range(0, 10):
    toutiao.next_page()

