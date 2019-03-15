#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/19 11:48
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : conf.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import configparser
import os


class MyConf(configparser.ConfigParser):

    def __init__(self, defaults=None):
        configparser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


class Conf(object):

    def __init__(self, cfg='./config.txt'):
        self.cfg = os.path.abspath(os.path.join(os.path.dirname(__file__), cfg))
        self.config = MyConf()
        self.config.read(self.cfg)

    def get_conf(self):
        return self.config


if __name__ == "__main__":
    TestCfg = Conf()
    config = TestCfg.get_conf()
    chromedriver_path=config.get('driver', 'chromedriver')
    print(chromedriver_path)
    root_dir = config.get('roots', 'root_dir')
    print(root_dir)

