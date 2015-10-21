# -*- coding: utf-8 -*-
__author__ = 'bitfeng'

import re


class TakeFirstL(object):

    def __call__(self, values):
        for value in values:
            if value is not None and value.strip() != '':
                return value.strip()
        return ''


class TakeLastL(object):

    def __call__(self, values):
        for value in values[::-1]:
            if value is not None and value.strip() != '':
                return value.strip()
        return ''


class TakeNumL(object):

    def __init__(self, num=0):
        self.num = num

    def __call__(self, values):
        if len(values) > self.num:
            return values[self.num].strip()
        else:
            return ''


class StripBlankL(object):

    def __call__(self, values):
        vlist = []
        for value in values:
            vlist.append(value.strip())
        return vlist


class ExtractTextL(object):

    def __call__(self, values):
        vlist = []
        for value in values:
            pattern = re.compile(u'(?<=>)[\s\S]*?(?=<)')
            vlist.append(''.join(pattern.findall(value.strip())))
        return vlist


class RemoveTagsL(object):
    def __call__(self, values):
        vlist = []
        for value in values:
            vlist.append(re.sub(u'<[^<>]+?>', '', value))
        return vlist


class JoinL(object):

    def __init__(self, separator=u' '):
        self.separator = separator

    def __call__(self, values):
        return self.separator.join(values)


class HeadTag(object):

    def __init__(self, tag='head:'):
        self.tag = tag

    def __call__(self, values):
        for value in values:
            if value is not None and value.strip() != '':
                return self.tag+value.strip()
        return ''


class ReplaceBlank(object):

    def __init__(self, sep='|'):
        self.sep = sep

    def __call__(self, values):
        vlist =[]
        for value in values:
            if value is not None and value.strip() != '':
                vlist.append(re.sub(u'\s+', '|', ''.join(value.strip())))
        return vlist