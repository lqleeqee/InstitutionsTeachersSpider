#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/19 15:47
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : SpiderParams.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import hashlib


class SpiderParams(object):

    def __init__(self):
        self.data_root_dir = None
        self.filterUrlList = set()
        self.short_name = None
        self.name_cn = None
        self.name_en = None

    pass


class PageParams(object):
    def __init__(self, url, curr_level):
        self.url = url.strip()
        self.curr_level = curr_level
        self.md5String_url = hashlib.md5(self.url.encode("utf-8")).hexdigest()
        self.is_writer_link = False
        self.url_path = ''
        self.children = []
        pass
    pass
