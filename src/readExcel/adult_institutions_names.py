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
from src.readExcel.ordinary_institutions_names import OrdinaryInstitutions


class AdultInstitutions(OrdinaryInstitutions):
    def read_excel(self):
        wb = load_workbook(filename=self.fn, read_only=True)
        ws = wb["sheet1"]
        for row in ws.rows:
            uid = str(row[0].value).replace("\n", "").strip()
            uname = str(row[1].value).replace("\n", "").strip()
            ucode = str(row[2].value).replace("\n", "").strip()
            udept = str(row[3].value).replace("\n", "").strip()
            tp_names = (uid, uname, ucode, udept)
            if "None" in tp_names:
                continue
            if not uid.isnumeric() or not ucode.isnumeric():
                continue
            self.names.append(tp_names)
        pass
    pass

