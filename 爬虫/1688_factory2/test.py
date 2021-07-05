# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import urllib
import urllib2
import sys
import os
import re
import csv
import numpy as np


class S1688(object):
    def __init__(self, url):
        self.url = url
    
    def init(self):
        self.driver = webdriver.Firefox()  # 打开一个浏览器
        time.sleep(5)  # 睡眠5秒，防止浏览器还没打开就进行了其他操作
        login_url = 'https://login.taobao.com/member/login.jhtml'  # 登录的url
        self.driver.get(login_url)  # 跳转到登录页面
        time.sleep(5)  # 睡眠5秒，防止网速较差打不开网页就进行了其他操作

        # 找到账号登录框的DOM节点，并且在该节点内输入账号
        self.driver.find_element_by_name("TPL_username").send_keys('梦似空月')
        # 找到账号密码框的DOM节点，并且在该节点内输入密码
        self.driver.find_element_by_name("TPL_password").send_keys('linwanting123')
        # 找到账号登录框的提交按钮，并且点击提交
        self.driver.find_element_by_name("TPL_password").send_keys(Keys.ENTER)
        time.sleep(5)  # 睡眠5秒，防止未登录就进行了其他操作
        
        self.driver.get(self.url)  # 跳转到指定页面的url
        csvfile = open('data.csv', 'web')
        writer = csv.writer(csvfile)

        # 写入标题，我们采集企业名称，主页，产品，联系人，电话和地址信息
        writer.writerow((
            u'企业名称'.encode('gbk'),
            u'主页'.encode('gbk'),
            u'产品'.encode('gbk'),
            u'联系人'.encode('gbk'),
            u'电话'.encode('gbk'),
            u'地址'.encode('gbk'),
            u'年限'.encode('gbk')
        ))

        # 构建agents防止反爬虫
        user_agents = [
            'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
            'Opera/9.25 (Windows NT 5.1; U; en)',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1;.NET CLR 1.1.4322; .NET CLR2.0.50727)',
            'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5(like Gecko) (Kubuntu)',
            'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
            'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
            "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
            "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
        ]

    def function(self, page_s, page_end):
        self.init()
        for page in range(page_s, page_end):
            time.sleep(5)
            try:
                title = self.driver.find_elements_by_css_selector("a[class=list-item-title-text]")
                product = self.driver.find_elements_by_xpath("//div[@class=\"list-item-detail\"]/div[1]/div[1]/a[1]")
                print len(title), title, product
            except:
                print 'page_error:', page
                continue

if __name__ == "__main__":
    uri = "https://s.1688.com/company/company_search.htm?keywords=%C5%AF%C6%F8&button_click=top&n=y&netType=1%2C11"
    t = S1688(uri)
    t.function(1, 2)

    

    

