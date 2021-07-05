#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re
import time
import requests
import execjs
from urllib import parse

class S1688(object):
    def __init__(self, word):

        self.head = {
          'cookie': 'cna=zdKCGIYRiU0CATsqP8ujETtC; _m_h5_tk=647b34a666eb9e5904cfc4c690149ac4_1625464058763; _m_h5_tk_enc=fc95878ab783a8c6615bf38c2722b3e0; cookie2=12f78d7a19fb1f75a87e1f4027aeade0; hng=CN%7Czh-CN%7CCNY%7C156; t=49c43452c1a92ece42ac43ee387b7340; _tb_token_=de33633833d8; csg=1d4a26c2; lid=%E6%A2%A6%E4%BC%BC%E7%A9%BA%E6%9C%88; __cn_logon__=false; UM_distinctid=17a74b7a8a7425-0cc5e94a320999-34657601-1fa400-17a74b7a8a8b5a; xlly_s=1; taklid=a1d9f85298ab4584a77fb88c18cabee4; _csrf_token=1625455831736; alicnweb=touch_tb_at%3D1625455927702; ali_ab=59.42.60.101.1625456112472.8; tfstk=cPkfBpYKvVHrjcRN3mtP_PP3Pzyla2SQfIamcXxKY4PdbL3QysYOLyMBBfbOeWE5.; l=eBIVxgHnj5lJ5A2CBOfZlurza779vIRAguPzaNbMiOCPOf127ZkNW6t4mhYyCnGVh67JR3rE2hzkBeYBcf21b0IVzhxMULkmn; isg=BC8v4E0Gk0SMPpd4TU8aAkscvkU51IP2DmJOjkG8-B6qkE-SSaDyR-mKFoCu6Ftu',
          "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
        }
        self.word = word  # 工厂关键词
        self.api = 'https://h5api.m.1688.com/h5/mtop.taobao.widgetservice.getjsoncomponent/1.0/?'

    def Main(self):
        self.Get_word()  # 一、关键词处理-获取工厂ID
        self.Get_mtopjsonp1()  # 二、获取合作伙伴地址等信息
        self.Get_mtopjsonp2()  # 三、获取生产实力
        self.Get_mtopjsonp7()  # 四、获取粉丝数
        self.RE_html()  # 五、正则提取与整理

    def Get_html(self, url):
        '请求网页，返回文本'
        req = requests.get(url, headers=self.head) #网页请求
        html = re.sub('\s', '', req.text)   #去除多余空格
        return html

    def Init_js(self, data):
        token = re.findall('_m_h5_tk=(.*?)_', self.head['cookie'], re.S)[0]  # token值
        s = '12574478'                  #固定参数
        self.a = str(int(time.time() * 1000)) #时间戳

        p = (token + "&" + self.a + "&" + s + "&" + data)   #参数整理
        with open('1688.js', 'r', encoding='utf-8') as f:   #加载js
            ctx = execjs.compile(f.read())
        self.sign = ctx.call('u', p)                #执行sign生成函数获取sign值

    def Get_word(self):
        url = 'https://s.1688.com/company/company_search.htm?keywords={}&charset=utf8'.format(self.word)
        print(url)
        req = self.Get_html(url)
        print(req)
        self.factory_id = re.findall('"realUserId":"(.*?)"', req, re.S)[0]   #获取工厂ID

    def Get_mtopjsonp1(self):

        data = '{"cid":"TpFacCoreInfosService:TpFacCoreInfosService","methodName":"execute","params":"{\\"facAliId\\":\\"' + str(
            self.factory_id) + '\\"}"}'  # 参数更新

        url=self.Get_url(data,1)
        # print(url)
        self.html1 = self.Get_html(url) #请求网页返回的文本
        # print(self.html1)
        self.Check_html(self.html1) #检查cookie是否正常

    def Check_html(self, html):
        k = re.findall('令牌过期', html, re.S)
        if k:
            print('令牌过期，更新cookie后重试')

    def Get_url(self,data,n):
        self.Init_js(str(data))  # js获取
        parms = 'jsv=2.6.0&appKey=12574478&t={}&sign={}&api=mtop.taobao.widgetService.getJsonComponent&v=1.0&type=jsonp&timeout=5000&dataType=jsonp&callback=mtopjsonp{}&'.format(
            self.a, self.sign,n)
        sdata = parse.quote(str(data))  # quote()将字符串进行编码
        url = self.api + parms + 'data=' + sdata
        print(url)
        return url

    def Get_mtopjsonp2(self):
        data = {"cid": "FactoryStrengthServiceWidget:FactoryStrengthServiceWidget", "methodName": "execute"}
        k = "{\"extParam\":{\"factoryUserId\":\"%s\"}}" % (self.factory_id)#参数修改
        data.update(({'params': k}))#字典更新

        url=self.Get_url(data,2)

        self.html2 = self.Get_html(url)

        self.Check_html(self.html2)

    def Get_mtopjsonp7(self):

        data = {'cid': 'ShopFavouriteServiceWidget:ShopFavouriteServiceWidget', 'methodName': 'execute'}
        k = '{"extParams":{"method":"readFavourite","targetUserId":"%s"}}' % (self.factory_id)
        data.update(({'params': k}))

        url=self.Get_url(data,7)

        self.html7 = self.Get_html(url)

        self.Check_html(self.html7)

    def RE_html(self):
        facName = re.findall('"facName":"(.*?)"', self.html1, re.S)[0]  # 工厂名称
        data = re.findall('"data":"(.*?)"', self.html1, re.S)  # 数据

        comment = re.findall('"desc":"(.*?)"', self.html1, re.S)  # 备注

        factoryPv = re.findall('"factoryPv":"(.*?)"', self.html1, re.S)[0]  # 浏览数
        address = re.findall('"factoryDetailedAddress":"(.*?)"', self.html1, re.S)[0]  # 地址

        # favCount = re.findall('"favCount":"(.*?)"', self.html7, re.S)[0]  # 粉丝数

        k = re.findall('"value":"(.*?)"', self.html2, re.S)  # 生产实力
        s = ''
        for i, com in enumerate(comment):
            if i==0:
                t='\t'
            else:
                t='%\t'
            s += str(com) + ':' + str(data[i]) +t

        # s += '粉丝数:' + favCount + '\t' + '浏览数:' + factoryPv + '\t'

        h = '厂房面积' + k[0] + '平方' + '\t' + \
            '生产人数' + k[1] + '人' + '\t' + \
            '设备总数' + k[2] + '台' + '\t' + \
            '仓储类型' + k[3] + '\t' + \
            '加工方式' + k[4] + '\t' + \
            '代工模式' + k[5] + '\t' + \
            '质检类型' + k[6] + '\t' + \
            '售后服务' + k[7] + '\t'
        print(facName + '\n' + '*' * 50 + '\n' + s + '\n' + address + '\n' + '-' * 50 + '\n' + h)


if __name__ == '__main__':
    word = '深圳市杰之美时装有限公司'
    ex = S1688(word)
    ex.Main()