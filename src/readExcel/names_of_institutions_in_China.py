#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lizujun
# @email: lizujun2008@gmail.com
# @crate time : 1/28/2019 04:17 PM
import os
from src.readExcel.ordinary_institutions_names import OrdinaryInstitutions
from src.readExcel.adult_institutions_names import AdultInstitutions
from src.configure.conf import Conf


class NamesOfInstitutions(object):

    def __init__(self):
        conf = Conf()
        config = conf().get_conf()
        root_dir = config.get('roots', 'root_dir')
        ord_fn = config.get('xlsx', 'ord_institutions')
        adu_fn = config.get('xlsx', 'adu_institutions')
        #dircetory = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
        self.ord_fn = os.path.abspath(os.path.join(root_dir, ord_fn))
        self.adu_fn = os.path.abspath(os.path.join(root_dir, adu_fn))
        self.institutions_names = []
        self.extend_adu_names()
        self.extend_ord_names()
        pass

    def extend_ord_names(self):
        OIN = OrdinaryInstitutions(self.ord_fn)
        self.institutions_names.extend(OIN.names)
        pass

    def extend_adu_names(self):
        AIN = AdultInstitutions(self.adu_fn)
        self.institutions_names.extend(AIN.names)
        pass

    def get_names(self):
        self.institutions_names = list(set(self.institutions_names))
        return self.institutions_names
    pass


if __name__ == "__main__":
    InstitutionsNames = NamesOfInstitutions()
    names = InstitutionsNames.get_names()
    for t in names:
        print(t)
    print(len(names))
