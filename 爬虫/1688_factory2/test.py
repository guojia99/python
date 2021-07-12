# coding:utf-8
import traceback
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv

import sys

reload(sys)
sys.setdefaultencoding('utf8')


class S1688(object):
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.pwd = password
    
    def init(self):
        self.csvfile = open('data.csv', 'wb')
        self.data = []
        self.driver = webdriver.Firefox()  # 打开一个浏览器
        time.sleep(5)  # 睡眠5秒，防止浏览器还没打开就进行了其他操作
        login_url = 'https://login.taobao.com/member/login.jhtml'  # 登录的url
        self.driver.get(login_url)  # 跳转到登录页面
        time.sleep(5)  # 睡眠5秒，防止网速较差打不开网页就进行了其他操作

        # 找到账号登录框的DOM节点，并且在该节点内输入账号
        self.driver.find_element_by_name("fm-login-id").send_keys(self.username)
        # 找到账号密码框的DOM节点，并且在该节点内输入密码
        self.driver.find_element_by_name("fm-login-password").send_keys(self.pwd)
        # 找到账号登录框的提交按钮，并且点击提交
        self.driver.find_element_by_name("fm-login-password").send_keys(Keys.ENTER)
        time.sleep(5)  # 睡眠5秒，防止未登录就进行了其他操作
        
        self.driver.get(self.url)  # 跳转到指定页面的url
        self.writer = csv.writer(self.csvfile)

        # 构建agents防止反爬虫
        self.user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;.NET CLR 1.1.4322; .NET CLR2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5(like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        ]

    @staticmethod
    def find_list_text(lt):
        if len(lt) >= 1:
            return lt[0].text
        return "-"

    @staticmethod
    def find_time_sleep():
        for item in range(10):
            time.sleep(10)
            print "time sleep: {}".format(item*10)

    def function(self):

        self.init()
        page_end = 50
        print "page is", page_end

        for page in range(1, page_end):
            self.driver.execute_script("window.scrollTo(0,1000);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,2000);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0,4000);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0,1000);")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0,10000);")
            time.sleep(5)
            try:
                product = self.driver.find_elements_by_class_name("company-offer-contain")
                for i in product:
                    title = i.find_elements_by_class_name("company-name")
                    self.data.append({
                        "title": self.find_list_text(title),
                        "href": (title[0].get_attribute("href") or "none link") + 'page/contactinfo.htm',
                        "year": self.find_list_text(i.find_elements_by_class_name("integrity-year")),
                        "position": self.find_list_text(i.find_elements_by_class_name("position-text")),
                        "info": self.find_list_text(i.find_elements_by_class_name("company-info")),
                        "craft_content": self.find_list_text(i.find_elements_by_class_name("main-craft-content")),
                    })
                page = self.driver.find_elements_by_css_selector("a[class=fui-next]")[0]
                page.click()
            except:
                print 'page_error:', page
                traceback.print_exc()
                continue
        self.driver.close()

        # 写入标题，采集企业名称，主页，产品，联系人，电话和地址信息
        self.writer.writerow((
            '企业名称',
            '主页链接',
            '年限',
            '地址',
            '其他信息',
            '主营业务'

        ))
        import json
        f = open("data.json", 'wb')
        f.write(json.dumps(self.data))
        f.close()

        for item in self.data:
            self.writer.writerow((
                str(item["title"]),
                str(item["href"]),
                str(item["year"]),
                str(item["position"]),
                str(item["info"]),
                str(item["craft_content"])
            ))
        self.csvfile.close()


if __name__ == "__main__":
    uri = "https://s.1688.com/company/company_search.htm?keywords=%B5%E7%C5%AF%C6%F7&spm=a26352.13672862.searchbox.input"
    t = S1688(url=uri, username="15089512105", password="linwanting123")
    t.function()
