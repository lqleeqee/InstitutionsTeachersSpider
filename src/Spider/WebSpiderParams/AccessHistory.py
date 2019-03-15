#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/19 16:32
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : AccessHistory.py
# @license : Copyright(C), Lee
# @Software: PyCharm


def _init():
    global _access_history
    _access_history = set()


def add_value(value):
    _access_history.add(value)


def exists(value):
    if value in _access_history:
        return True
    else:
        return False

