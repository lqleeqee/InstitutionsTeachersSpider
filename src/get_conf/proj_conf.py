#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lizujun
# @email: lizujun2008@gmail.com
# @crate time : 3/14/2019 02:01 PM
import configparser
from configparser import RawConfigParser
import os


class MyConf(configparser.RawConfigParser):

    def __init__(self, defaults=None):
        configparser.RawConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


class ProjectConfigure(MyConf):
    def __init__(self):
        MyConf.__init__(self)
        conf_file = os.path.abspath(__file__)
        conf_file = os.path.join(conf_file, '../../../config/proj.conf')
        conf_file = os.path.abspath(conf_file)
        self.read(conf_file, encoding='utf-8')


if __name__ == "__main__":
    conf = ProjectConfigure()
    print(conf.sections())
    print(conf.get('basic','proj_root'))
    print(conf.get('log_fmt', 'format'))
    pass
