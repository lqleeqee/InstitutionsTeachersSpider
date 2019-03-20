#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @author: lizujun
# @email: lizujun2008@gmail.com
# @crate time : 3/14/2019 02:51 PM
import os
import logging
import sys
from src.get_conf.proj_conf import ProjectConfigure


class LoggingConfigure(object):
    def __init__(self):
        proj_conf = ProjectConfigure()
        proj_root = proj_conf.get('basic', 'proj_root')
        self.logging_fn = os.path.join(proj_root, proj_conf.get('logging', 'logging_log'))
        # info_fn = os.path.join(proj_root, proj_conf.get('logging', 'info_log'))
        # debug_fn = os.path.join(proj_root, proj_conf.get('logging', 'debug_log'))
        if not os.path.exists(os.path.dirname(self.logging_fn)):
            os.makedirs(os.path.dirname(self.logging_fn))
        self.fmt = proj_conf.get('log_fmt', 'format').strip()
        pass

    def log_debug(self, logger_name, message):
        self.log('DEBUG', logger_name, message)
        pass

    def log_info(self, logger_name, message):
        self.log('INFO', logger_name, message)
        pass

    def log_warning(self, logger_name, message):
        self.log('WARNING', logger_name, message)
        pass

    def log_error(self, logger_name, message):
        self.log('ERROR', logger_name, message)
        pass

    def log_critical(self, logger_name, message):
        self.log('CRITICAL', logger_name, message)
        pass

    def log(self, level, logger_name, message):
        levels = {'CRITICAL':logging.CRITICAL,'ERROR':logging.ERROR,
                  'WARNING':logging.WARNING,'INFO':logging.INFO,
                  'DEBUG':logging.DEBUG,'NOTSET':logging.NOTSET}
        level = level.upper().strip()
        message = message.__str__()
        logger = logging.getLogger(logger_name)
        logger.setLevel(levels.get(level))  # default log level
        fmt = logging.Formatter(self.fmt)  # output format
        sh = logging.StreamHandler(stream=sys.stdout)  # output to standard output
        sh.setFormatter(fmt)
        fh = logging.FileHandler(self.logging_fn, mode='a',
                                 encoding='utf-8', delay=False)
        fh.setLevel(levels.get(level))
        fh.setFormatter(fmt)
        logger.addHandler(sh)
        logger.addHandler(fh)
        if level == 'CRITICAL':
            logger.critical(message)
        elif level == 'ERROR':
            logger.error(message)
        elif level == 'WARNING':
            logger.warning(message)
        elif level == 'INFO':
            logger.info(message)
        else:
            logger.debug(message)
        logger.handlers = []
        pass

if __name__ == "__main__":
    mesg = 'this is a test message!'
    a = LoggingConfigure()
    a.log_debug('test', mesg) # 同时输出到文件与控制台


