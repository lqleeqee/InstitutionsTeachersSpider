#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lizujun
# @email: lizujun2008@gmail.com
# @crate time : 1/28/2019 03:07 PM
import os
import sys
import xlrd
import xlwt
import openpyxl
from openpyxl import Workbook
from openpyxl import load_workbook


class OrdinaryInstitutions(object):

    def __init__(self, excel_fn):
        self.fn = excel_fn
        self.names = []
        self.read_excel()
        pass

    def read_excel(self):
        wb = load_workbook(filename=self.fn, read_only=True)
        ws = wb["sheet1"]
        for row in ws.rows:
            uid = str(row[0].value).replace("\n", "").strip()
            uname = str(row[1].value).replace("\n", "").strip()
            ucode = str(row[2].value).replace("\n", "").strip()
            udept = str(row[3].value).replace("\n", "").strip()
            uaddr = str(row[4].value).replace("\n", "").strip()
            urank = str(row[5].value).replace("\n", "").strip()
            tp_names = (uid, uname, ucode, udept, uaddr, urank)
            if "None" in tp_names:
                continue
            if not uid.isnumeric() or not ucode.isnumeric():
                continue
            self.names.append(tp_names)
        pass

    pass

