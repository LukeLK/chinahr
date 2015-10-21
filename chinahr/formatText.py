# -*- coding: utf-8 -*-
__author__ = 'bitfeng'


import re


class FormatText(object):

    # 抽取复杂html中>和<之间的text内容，删除多余空格后拼接,list or str
    def extract_text(self, str_sel):
        if type(str_sel) == list:
            str_re = []
            for var in str_sel:
                str_re.append(self.extract_text_str(var))
            return str_re
        elif type(str_sel) == str:
            return self.extract_text_str(str_sel)
        else:
            return str_sel

    # 去除list中空格或换行符
    def strip_blankchr(self, str_sel):
        str_re = []
        for var in str_sel:
            if not re.compile(u'^\s+$').match(var):
                str_re.append(var.strip())
        return str_re

    # 抽取>和<之间的text内容并拼接,string
    def extract_text_str(self, str_sel):
        pattern = re.compile(u'(?<=>)[\s\S]*?(?=<)')
        str_re = re.sub(u'\r?\n', '', ''.join(pattern.findall(str_sel))).replace(' ', '')
        return str_re

    # # 删除 <.+> 样式的html标签，string
    # def delete_html_str(self, str_sel):
    #     pattern = re.compile(u'<.+>')

    def strip_list(self, str_sel):
        str_re = []
        for var in str_sel:
            str_re.append(var.strip())
        return str_re



