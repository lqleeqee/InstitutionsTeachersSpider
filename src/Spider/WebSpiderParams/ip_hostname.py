#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/2/25 10:15
# @Author  : lee
# @Contact : lqleeqee@gmail.com 
# @Site    : 
# @File    : ip_hostname.py
# @license : Copyright(C), Lee
# @Software: PyCharm
import re

subjects = ['https://blog.csdn.net/guaguastd/article/details/40373455',
            'https://www.rgexcook.com']

reobj = re.compile(r"""(?xi)\A
[a-z][a-z0-9+\-.]*://                                # Scheme
([a-z0-9\-._~%!$&'()*+,;=]+@)?                       # User
([a-z0-9\-._~%]+                                     # Named or IPv4 host
|\[[a-z0-9\-._~%!$&'()*+,;=:]+\])                    # IPv6+ host
""")
for subject in subjects:
    match = reobj.search(subject)
    #print(dir(match))
    if match:
        print(match.group(2)[match.group(2).index('.')+1:])
