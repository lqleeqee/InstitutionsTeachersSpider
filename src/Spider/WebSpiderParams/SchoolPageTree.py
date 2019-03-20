#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/24 16:48
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : SchoolPageTree.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import re
import requests
import hashlib
import urllib3
import socket
import sys
import os
import inspect
import importlib
import time
from selenium.common import exceptions as selenium_error
pre_folder = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], "..")))
if pre_folder not in sys.path:
    sys.path.insert(0, pre_folder)
importlib.reload(sys)
from src.Spider.WebSpiderParams.WebSpiderDriver import SpiderDriver
from src.Spider.WebSpiderParams.MultiBranchesTree import MultiWayTree
from src.Spider.WebSpiderParams.PageNode import PageNode
from src.get_conf.log_conf import LoggingConfigure
sys.setrecursionlimit(1000000)


class SchoolWebPageTree(object):

    def __init__(self, url=None, school_name=None, abbreviation_cn=None, abbreviation_en=None):
        self.home_url = url.strip()
        self.logger = LoggingConfigure()
        self.school_name = school_name.strip()
        self.dn = self.get_domain_name().strip()
        self.abbreviation_cn = abbreviation_cn.strip()
        self.abbreviation_en = abbreviation_en.strip()
        self.tree = MultiWayTree(url=self.home_url, school_name=self.school_name,
                                 abbreviation_cn=self.abbreviation_cn, abbreviation_en=self.abbreviation_en)
        self.driver = SpiderDriver()
        self.driver.get(self.home_url)
        self.leaves_nodes = []
        #self.leaves_nodes = self.tree.leaf_nodes(self.tree.root_node, []).remove(self.tree.root_node)
        self.access_histories = set()
        #self.access_histories.add(self.home_url)
        self.access_histories.add(hashlib.md5(self.home_url.encode("utf-8")).hexdigest())
        self.access_histories.add(hashlib.md5("javascript:;".encode("utf-8")).hexdigest())
        self.access_histories.add(hashlib.md5("javascript:".encode("utf-8")).hexdigest())
        requests.adapters.DEFAULT_RETRIES = 5
        s = requests.session()
        s.keep_alive = False
        pass

    def get_domain_name(self):
        re_matcher = re.compile(r"""(?xi)\A
        [a-z][a-z0-9+\-.]*://                                # Scheme
        ([a-z0-9\-._~%!$&'()*+,;=]+@)?                       # User
        ([a-z0-9\-._~%]+                                     # Named or IPv4 host
        |\[[a-z0-9\-._~%!$&'()*+,;=:]+\])                    # IPv6+ host
        """)
        match = re_matcher.search(self.home_url)
        if match:
            dn = match.group(2)
            return dn[dn.index('.'):]

    def is_school_web_page(self, page_node):
        node_url = page_node.url
        node_title = page_node.title
        threshold = 0.0
        if self.dn is not None:
            if self.dn in node_url:
                threshold += 1.01
            elif self.dn[1:] in node_url:
                threshold += 0.81
            else:
                threshold -= 0.41
        if self.abbreviation_cn in node_title \
                or self.school_name in node_title:
            threshold += 0.81
        else:
            threshold -= 0.31
        if self.abbreviation_en.lower() in node_title.lower() \
                or self.abbreviation_en.lower() in node_url:
            threshold += 0.51
        else:
            threshold -= 0.21
        if '图书馆' in node_title:
            threshold -= 3.05
        if '就业' in node_title or '就业信息'in node_title or '招聘' in node_title:
            threshold -= 3.05
        if '有限公司' in node_title or '集团' in node_title:
            threshold -= 3.05

        if threshold >= 1:
            return True
        else:
            return False
        pass

    def is_school_web_url(self, url, title):
        pn = PageNode(url=url, title=title)
        return self.is_school_web_page(pn)
        pass

    def open_all_url(self, par_link):
        self.driver.get(par_link)
        time.sleep(5)
        parent_url = self.driver.current_url()
        links = [link.get_attribute('href').strip() for link in self.driver.driver.find_elements_by_xpath("//*[@href]")]
        links = set(links)
        # 先从访问历史过滤第一次，url跳转之后，过滤第二次
        new_links = []
        for url in links:
            url_md5 = hashlib.md5(url.encode("utf-8")).hexdigest()
            if url_md5 not in self.access_histories:
                new_links.append(url)
            else:
                continue
        del links
        links = new_links
        for link in links:
            # 首先，跳过已经访问过的url
            link_md5 = hashlib.md5(link.encode("utf-8")).hexdigest()
            if link_md5 in self.access_histories:
                self.logger.log_debug("Creat Tree", ('Have visited: ', link))
                # print("Have visited: ", link)
                continue
            # 去除视频，图片，email，等
            # 要去除两次，跳转后，去除第二次，这是第一次
            if not self.driver.is_url(link) or self.driver.is_css(link) \
                    or self.driver.is_img(link) or self.driver.is_email(link) \
                    or self.driver.is_video(link) or self.driver.is_doc(link):
                # print('Invalid URL: ', link)
                self.logger.log_debug("Creat Tree", ('Invalid URL: ', link))
                self.access_histories.add(link_md5)
                continue
            try:
                self.driver.get(link)
                #time.sleep(5)
                title = self.driver.title()
                old_link = link
                link = self.driver.current_url()
                if link != old_link:
                    self.access_histories.add(link_md5)
                link_md5 = hashlib.md5(link.encode("utf-8")).hexdigest()
                # 如果已经访问过，则跳过
                if link_md5 in self.access_histories:
                    self.logger.log_debug("Creat Tree", ('Have visited: ', link))
                    # print("Have visited: ", link)
                    continue
                else:
                    self.access_histories.add(link_md5)
                # 去除视频，图片，email，等
                if not self.driver.is_url(link) or self.driver.is_css(link) \
                        or self.driver.is_img(link) or self.driver.is_email(link) \
                        or self.driver.is_video(link) or self.driver.is_doc(link):
                    # print('Invalid URL: ', link)
                    self.logger.log_debug("Creat Tree", ('Invalid URL: ', link))
                    self.access_histories.add(hashlib.md5(link.encode("utf-8")).hexdigest())
                    continue
                # 根据状态码判断是否跳过
                r = requests.get(link, timeout=5)
                status_code = r.status_code
                if status_code < 200 or status_code > 400:
                    # print('Unreachable url: %s, status_code: %s', (link, str(status_code)))
                    self.logger.log_debug("Creat Tree",
                                          ('Unreachable url: %s, status_code: %s', (link, str(status_code))))
                    continue
                # 如果是新页面，且被判断为学校站点的页面，则添加到树中
                if self.is_school_web_url(link, title):
                    msg = 'new node:  status_code: %d, url : %s , title: %s' % (status_code, link, title)
                    # print(msg)
                    self.logger.log_debug('Creat Tree',  msg)
                    page_html = self.driver.get_source()
                    yield PageNode(url=link, title=title, html=page_html), parent_url
                else:
                    # print("It's not an internal school page: ", link)
                    self.logger.log_debug("Creat Tree", ("It's not an internal school page: ", link))
            except requests.exceptions.ConnectionError as requestsError:
                print(requestsError)
                continue
            except urllib3.exceptions.MaxRetryError as urllibError:
                print(urllibError)
                continue
            except urllib3.exceptions.NewConnectionError as urllibNewError:
                print(urllibNewError)
                continue
            except socket.gaierror as socketError:
                print(socketError)
                continue
            except selenium_error.TimeoutException as s:
                print(s)
                continue
            except Exception as e:
                print(e)
                continue
        pass

    def building_tree(self):
        if self.whether_break():
            # print("School Tree has been created!")
            self.logger.log_debug("Creat Tree", 'School Tree has been created!')
            return True
        self.tree.root_node.display()
        if not self.leaves_nodes:
            self.leaves_nodes.clear()
        self.leaves_nodes.extend(self.tree.leaf_nodes(self.tree.root_node, []))
        for pre_node in self.leaves_nodes:
            pre_link = pre_node.url
            try:
                for new_node, parent_url in self.open_all_url(pre_link):
                    self.tree.__add__(new_node, parent_node_url=parent_url)
            except selenium_error.StaleElementReferenceException as e:
                # print("StaleElementReferenceException: ", e)
                self.logger.log_debug("Creat Tree",("StaleElementReferenceException: ", e))
                continue
                pass
            except selenium_error.NoSuchWindowException as noWindows:
                # print('selenium.common.exceptions.NoSuchWindowException:', noWindows)
                self.logger.log_debug('Creat Tree', ('selenium.common.exceptions.NoSuchWindowException:', noWindows))
                continue
                pass
        return self.building_tree()
        pass

    def whether_break(self):
        leaves_node_round_n = self.tree.leaf_nodes(self.tree.root_node, [])
        if not self.leaves_nodes:
            return False
        # for turl in [node.url for node in leaves_node_round_n]:
        #     if (hashlib.md5(link.encode("utf-8")).hexdigest() not in self.access_histories
        for node in leaves_node_round_n:
            if node not in self.leaves_nodes:
                self.leaves_nodes.clear()
                self.leaves_nodes.extend(leaves_node_round_n)
                return False
        return True


if __name__ == "__main__":
    ruc = SchoolWebPageTree(url='https://www.ruc.edu.cn/',
                            school_name='中国人民大学', abbreviation_cn='人大', abbreviation_en='ruc')
    # ruc = SchoolWebPageTree(url='http://www.tjghxy.com/',
    #                         school_name='天津市工会管理干部学院', abbreviation_cn='天津市工会管理干部学院', abbreviation_en='tjghxy')
    # ruc = SchoolWebPageTree(url='http://www.hust.edu.cn/',
    #                         school_name='华中科技大学', abbreviation_cn='华科', abbreviation_en='HUST')
    ruc.building_tree()
    ruc.tree.root_node.display()
    print('\n\n')
    leaves_nodes = ruc.tree.leaf_nodes(ruc.tree.root_node)
    for node in leaves_nodes:
        node.display()
    ruc.driver.quit()
# https://www.ruc.edu.cn/
# http://alumni.ruc.edu.cn/
