#!/usr/bin/env python
# -*- coding: utf-8 -*-
import traceback
import django
import os
import jieba
from jieba import analyse
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lagou_new_web.settings")
django.setup()
from myapp.models import *

import os
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from bs4 import BeautifulSoup
from collections import Counter
import sys
import time
import re
import requests


class Spider(object):
    """
    爬取类
    """
    def __init__(self, ):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
        # self.browser = webdriver.PhantomJS(executable_path=self._getdriverpath())
        self.browser = webdriver.Chrome(self._getdriverpath(), chrome_options=options)
        self.browser.implicitly_wait(60) # 隐性等待，最长等30秒
        self.browser.maximize_window()
        self.skill_type ={0: {0: 'java', 1: 'c++', 2:'php', 3: 'python'},
                          1: {4: 'HTML5', 5: 'android', 6:'ios', 7: 'wp'},
                          2: {8: 'web前端', 9: 'Flash', 10:'html5', 11: 'javascript'},
                          3: {12: '深度学习', 13: '机器学习', 14:'图像处理', 15: '图像识别'},
                          4: {16: '测试工程师', 17: '自动化测试', 18:'功能测试', 19: '性能测试'},
                          5: {20: '运维工程师', 21: '运维开发工程师', 22:'网络工程师', 23: '系统工程师'},
                          6: {24: 'mysql', 25: 'sqlserver', 26:'oracle', 27: 'DB2'},
                          }

    def get_data(self):
        for key, skill in self.skill_type.items():
            for key_child, skill_child in skill.items():
                url = "https://www.lagou.com/jobs/list_{0}?px=default&city=%E5%85%A8%E5%9B%BD#filterBox".format(skill_child)
                self.browser.get(url)
                time.sleep(2)
                page_index = 1
                while page_index <= 30:
                    bs = BeautifulSoup(self.browser.page_source, "html.parser")
                    div_list = bs.select("ul li.con_list_item")
                    for item in div_list:
                        try:
                            data = DataModel()
                            position = item.select("div.position")[0]
                            data.zhiwei = position.select("a.position_link h3")[0].text
                            data.position = position.select("span em")[0].text
                            company = item.select("div.company")[0]
                            data.company_name = company.select("div.company_name a")[0].text
                            data.industry = item.select("div.industry")[0].text.replace("\n", "").strip()
                            data.rongzi = data.industry.split("/")[1]
                            data.industry = data.industry.split("/")[0]
                            data.money = position.select("span.money")[0].text
                            data.exp = position.select("div.li_b_l")[0].text.split("\n")[2]
                            data.xueli = data.exp.split("/")[1].strip()
                            data.exp = data.exp.split("/")[0].strip()
                            data.sort = key_child
                            data.skill_type = key
                            data.save()
                        except Exception as e:
                            print(traceback.format_exc())
                            print(e)
                            continue
                    try:
                        page = self.browser.find_element_by_css_selector("span.pager_next")
                        page.click()
                        page_index += 1
                        time.sleep(2)
                    except Exception as e:
                        break
        self.browser.close()

    def quit(self):
        self.browser.close()

    def analyze(self, description):
        jieba.analyse.set_stop_words('stop_words.txt')
        stop_dict = {}
        content = open("stop_words.txt", "rb").read().decode('utf-8')
        for wd in content.split('\n'):
            stop_dict[wd] = 1
        tk = jieba.cut(description, cut_all=True)
        data = dict(Counter(tk))

        pat = re.compile(r'\d')
        keywords = {}
        for key, value in data.items():
            if key and not pat.search(key) and key not in stop_dict and len(key)>=2:
                if key in keywords:
                    keywords[key] += value
                else:
                    keywords[key] = value
        return keywords

    def _getdriverpath(self):
        path = "C://chromedriver.exe"
        return path

if __name__ == '__main__':
    Spider().get_data()

