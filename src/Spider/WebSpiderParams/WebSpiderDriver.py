#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/22 14:34
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : WebSpiderDriver.py
# @license : Copyright(C), Lee
# @Software: PyCharm
from selenium.common import exceptions
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from src.configure.conf import Conf
from selenium.common import exceptions as selenium_error
import time
import re
import zlib
import traceback
import requests
from src.Spider.WebSpiderParams.PageNode import PageNode


class SpiderDriver(object):

    def __init__(self):
        config = Conf()
        chrome_options = webdriver.ChromeOptions()
        prefs = {
            'profile.default_content_setting_values': {
                'images': 2,  # 禁用图片的加载
                # 'javascript': 2  ##禁用js，可能会导致通过js加载的互动数抓取失效
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        chromedriver_path = config.get_conf().get('driver', 'chromedriver')
        #chrome_options.add_argument()

        self.driver = webdriver.Chrome(executable_path=chromedriver_path, chrome_options=chrome_options)
        self.driver.maximize_window()
        self.driver.implicitly_wait(50)
        self.driver.set_page_load_timeout(50)
        self.driver.set_script_timeout(10)
        pass

    def get(self, url):
        print("get url: ", url)
        main_win = self.driver.current_window_handle  # 记录当前窗口的句柄
        all_win = self.driver.window_handles
        # self.driver.switch_to.alert().accept()
        # alert = self.driver.switch_to.alert
        # alert.dismiss()
        try:
            if len(all_win) == 1:
                print('弹出保护罩')
                js = 'window.open("https://www.baidu.com");'
                self.driver.execute_script(js)
                # 还是定位在main_win上的
                for win in all_win:
                    if main_win != win:
                        print('保护罩WIN', win, 'Main', main_win)
                        self.driver.switch_to.window(main_win)
            self.driver.get(url)
            #time.sleep(10)
        except selenium_error.TimeoutException as s:
            # 超时
            print('Time out: ', s)
            # 切换新的浏览器窗口
            for win in all_win:
                if main_win != win:
                    print('WIN', win, 'Main', main_win)
                    print('切换到保护罩')
                    self.driver.close()
                    self.driver.switch_to.window(win)
                    main_win = win

            js = 'window.open("https://www.baidu.com");'
            self.driver.execute_script(js)
            if 'time' in str(traceback.format_exc()):
                print('页面访问超时')

        # except selenium_error.UnexpectedAlertPresentException as s:
        #     print('NoAlertPresentException: ', s)
        #     self.driver.close()
        #     win = self.driver.window_handles[0]
        #     self.driver.switch_to.window(win)
        #     main_win = win
        pass

    def reflush(self):
        self.driver.refresh()
        pass

    def quit(self):
        self.driver.quit()
        pass

    def page_source(self):
        #return self.driver.page_source
        try:
            page_source = self.driver.page_source
            return page_source
        except selenium_error.UnexpectedAlertPresentException as s:
            print('UnexpectedAlertPresentException: ', s)
            alert_title = self.driver.switch_to.alert
            alert_title.accept()
        finally:
            time.sleep(10)
            page_source = self.driver.page_source
        return page_source
        pass

    def current_url(self):
        try:
            url = self.driver.current_url
            return url
        except selenium_error.UnexpectedAlertPresentException as s:
            print('UnexpectedAlertPresentException: ', s)
            alert_title = self.driver.switch_to.alert
            alert_title.accept()
            time.sleep(10)
        finally:
            url = self.driver.current_url
        return url
        pass

    def title(self):
        try:
            curr_title = self.driver.title.strip()
            return curr_title
        except selenium_error.UnexpectedAlertPresentException as s:
            print('UnexpectedAlertPresentException: ', s)
            alert_title = self.driver.switch_to.alert
            alert_title.accept()
            time.sleep(10)
        finally:
            curr_title = self.driver.title.strip()
        return curr_title

    @classmethod
    def is_url(cls, url):
        pattern = re.match(
            r'(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?',
            url, re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_email(cls, email):
        pattern = re.match(r'\w+@([0-9a-zA-Z]+[-0-9a-zA-Z]*)(\.[0-9a-zA-Z]+[-0-9a-zA-Z]*)+', email, re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_ip(cls, ip):
        pattern = re.match(
            r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', ip,
            re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_img(cls, img_url):
        pattern = re.match(
            r'(http|ftp|https):.*?\.(jpg|png|ico)', img_url,
            re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_doc(cls, doc_url):
        pattern = re.match(
            r'(http|ftp|https):.*?\.(doc|pdf|docx|ppt|pptx|txt|xls|xlsx|rar|enw|bib)', doc_url.strip(),
            re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_video(cls, video_url):
        pattern = re.match(
            r'(http|ftp|https):.*?\.(flv|mp4|mp3|wmv|rmvb|mpeg|rm|mov|swf)', video_url,
            re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    @classmethod
    def is_css(cls, css_url):
        pattern = re.match(
            r'(http|ftp|https):.*?\.css', css_url,
            re.IGNORECASE)
        if pattern:
            return True
        else:
            return False

    # def open_all_url(self):
    #     parent_url = self.driver.current_url
    #     links = [link.get_attribute('href').strip() for link in self.driver.find_elements_by_xpath("//*[@href]")]
    #     links = list(set(links))
    #     for link in links:
    #         if not self.is_url(link):
    #             print('Invalid URL: ', link)
    #             continue
    #         if self.is_css(link):
    #             #print("CSS address: ", link)
    #             continue
    #         if self.is_img(link):
    #             #print("Img URL: ", link)
    #             continue
    #         if self.is_email(link):
    #             #print("Email address: ", link)
    #             continue
    #         r = requests.get(link)
    #         status_code = r.status_code
    #         if status_code < 200 or status_code > 400:
    #             print('Unreachable url: %s, status_code: %s', (link, str(status_code)))
    #             continue
    #         self.get(link)
    #         #time.sleep(10)
    #         title = self.title()
    #         print(status_code, link, title)
    #         yield PageNode(url=link, title=title), parent_url
    #         # #link.send_keys(Keys.COMMAND, "t")
    #     pass

    def get_source(self):
        page = self.driver.page_source
        #return zlib.compress(page)
        return page
        pass


if __name__ == "__main__":
    driver = SpiderDriver()
    driver.get("https://www.ruc.edu.cn/")
    driver.get("http://io.ruc.edu.cn/hmt/more.php?cid=101")
    print('url: ', driver.current_url())
    print("source: ", driver.page_source())
    print("title: ", driver.title())
    # try:
    #     print("title: ", driver.title())
    # except selenium_error.UnexpectedAlertPresentException as s:
    #     print('NoAlertPresentException: ', s)
    #     alert = driver.driver.switch_to.alert
    #     alert.accept()
    #     time.sleep(10)
    # finally:
    #     time.sleep(10)
    #     print("title: ", driver.title())


    # for node, parent_url in driver.open_all_url():
    #     node.display()
    #driver.open_all_url()
    #driver.quit()
    pass

