#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lizujun
# @email: lizujun2008@gmail.com
# @crate time : 1/30/2019 11:05 AM
from selenium.common import exceptions
from selenium import webdriver
from src.configure.conf import Conf
import time


class GetBaidu(object):
    # 打开baidu搜索，处理搜索结果，查找官网
    def __init__(self, school_names):
        config = Conf()
        chromedriver_path = config.get_conf().get('driver', 'chromedriver')
        self.driver = webdriver.Chrome(executable_path=chromedriver_path)
        self.driver.get("https://www.baidu.com")
        self.names = school_names
        self.name_urls = []
        self.faild_records = []
        self.get_office_website()
        self.driver.quit()
        pass

    def search(self, school_name):
        self.driver.get("https://www.baidu.com")
        self.driver.find_element_by_id("kw").clear()
        self.driver.find_element_by_id("kw").send_keys(school_name)
        self.driver.find_element_by_id("su").click()
        self.driver.implicitly_wait(10)
        time.sleep(5)
        for i in range(3):
            mark = False
            try:
                self.driver.find_element_by_xpath('//*[@id="%s"]/h3/a[2]' % (i + 1)).click()
                num = self.driver.window_handles
                self.driver.switch_to.window(num[-1])
                self.driver.implicitly_wait(30)
                if "信誉V认证" in self.driver.title:
                    mark = True
                self.driver.close()
                num = self.driver.window_handles
                self.driver.switch_to.window(num[-1])
                self.driver.find_element_by_xpath('//*[@id="%s"]/h3/a[1]' % (i+1)).click()
                num = self.driver.window_handles
                self.driver.switch_to.window(num[-1])
                try:
                    self.driver.refresh()
                except exceptions.TimeoutException:
                    time.sleep(3)
                    #self.driver.refresh()
                time.sleep(3)
                current_url = self.driver.current_url

                print("title: ", self.driver.title)
                if mark or school_name == self.driver.title:
                    print(current_url)
                    self.driver.close()
                    num = self.driver.window_handles
                    self.driver.switch_to.window(num[-1])
                    return current_url
                else:
                    self.driver.close()
                    num = self.driver.window_handles
                    self.driver.switch_to.window(num[-1])
                    continue
            except exceptions.NoSuchElementException:
                continue
        #self.driver.quit()
        raise AssertionError("The first five unmatched!")
        pass

    def get_office_website(self):
        for s in self.names:
            print(s)
            try:
                url = self.search(s)
                self.name_urls.append((s,url))
            except AssertionError:
                self.faild_records.append(s)
                continue
            time.sleep(5)

    def display_succesd(self):
        print("office website")
        for t in self.name_urls:
            print(t)

    def display_faild(self):
        print("faild")
        for t in self.faild_records:
            print(t)
    pass


if __name__=="__main__":
    universities_names = ['北京大学', '清华大学','中国人民大学','北京航空航天大学','北京理工大学',
                            '中央民族大学','南开大学','天津大学','中国农业大学','北京师范大学',''
                            '大连理工大学','同济大学','吉林大学','哈尔滨工业大学','复旦大学','上海交通大学',
                          '华东师范大学','南京大学','东南大学','浙江大学','山东大学','中国科学技术大学',
                          '厦门大学','武汉大学','华中科技大学','中南大学','中国海洋大学','中山大学',
                          '华南理工大学','四川大学','电子科技大学','西安交通大学','西北工业大学','兰州大学',
                          '重庆大学','国防科技大学','东北大学','郑州大学','云南大学','西北农林科技大学',
                          '湖南大学','新疆大学']

    new_website = GetBaidu(universities_names)
    new_website.display_succesd()
    print()
    new_website.display_faild()

