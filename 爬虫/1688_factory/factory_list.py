"""
获取工厂列表
"""
import re
import time
import requests
import execjs
from urllib import parse
from urllib.request import quote
import json


class FactoryList(object):
    URI = "https://s.1688.com/company/company_search.htm?keywords={word}&charset=utf8"
    PARSE = "&spm=a52.1672862.searchbox.input&beginPage={page}#sm-filtbar"

    def __init__(self, cookie, word):
        self.head = {
            "cookie": cookie,
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        self.word = word

        self.url = self.URI.format(word=quote(word, encoding="gbk"))
        print(self.url)

    def get_html(self, url):
        req = requests.get(url, headers=self.head)
        # html = re.sub("\s", '', req.text)
        html = req.text
        return html

    def init_js(self, data):
        token = re.findall('_m_h5_tk=(.*?)_', self.head['cookie'], re.S)[0]
        s = '12574478'
        self.st = str(int(time.time() * 1000))
        parse = (token + "&" + self.st + "&" + s + "&" + data)
        with open('1688.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
        self.sign = ctx.call('u', parse)

    def get_word(self):
        req = self.get_html(self.url)
        print(req)
        self.factory_id = re.findall('"realUserId":"(.*?)"', req, re.S)[0]

    def check_html(self, html):
        if re.findall("令牌过期", html, re.S):
            print('令牌过期，更新cookie后重试')

    def run(self):
        self.get_word()


if __name__ == "__main__":
    word = "热水器"
    cookie = 'cna=zdKCGIYRiU0CATsqP8ujETtC; _m_h5_tk=647b34a666eb9e5904cfc4c690149ac4_1625464058763; _m_h5_tk_enc=fc95878ab783a8c6615bf38c2722b3e0; cookie2=12f78d7a19fb1f75a87e1f4027aeade0; hng=CN%7Czh-CN%7CCNY%7C156; t=49c43452c1a92ece42ac43ee387b7340; _tb_token_=de33633833d8; csg=1d4a26c2; lid=%E6%A2%A6%E4%BC%BC%E7%A9%BA%E6%9C%88; __cn_logon__=false; UM_distinctid=17a74b7a8a7425-0cc5e94a320999-34657601-1fa400-17a74b7a8a8b5a; xlly_s=1; taklid=a1d9f85298ab4584a77fb88c18cabee4; _csrf_token=1625455831736; alicnweb=touch_tb_at%3D1625455927702; ali_ab=59.42.60.101.1625456112472.8; tfstk=cPkfBpYKvVHrjcRN3mtP_PP3Pzyla2SQfIamcXxKY4PdbL3QysYOLyMBBfbOeWE5.; l=eBIVxgHnj5lJ5A2CBOfZlurza779vIRAguPzaNbMiOCPOf127ZkNW6t4mhYyCnGVh67JR3rE2hzkBeYBcf21b0IVzhxMULkmn; isg=BC8v4E0Gk0SMPpd4TU8aAkscvkU51IP2DmJOjkG8-B6qkE-SSaDyR-mKFoCu6Ftu'
    d = FactoryList(cookie=cookie, word=word)
    d.get_word()


