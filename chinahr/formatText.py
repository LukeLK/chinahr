# -*- coding: utf-8 -*-
__author__ = 'bitfeng'


import re


class FormatText(object):

    #抽取复杂html的text内容并拼接
    def extract_text(self, str_sel):
        str_re = []
        pattern = re.compile(u'(?<=>)[\s\S]*?(?=<)')
        for var in str_sel:
            str_re.append(re.sub(u'\r?\n', '/', ''.join(pattern.findall(var))).replace(' ', ''))
        return str_re

    #去除list中空格或换行符
    def strip_blankchr(self, str_sel):
        str_re = []
        for var in str_sel:
            if not re.compile(u'^\s+$').match(var):
                str_re.append(var.strip())
            else:
                pass
        return str_re

