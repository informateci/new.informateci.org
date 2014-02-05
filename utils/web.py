# -*- coding: UTF-8 -*-
__author__ = 'mandrake'

import urllib2


def url2html(url):
    req = urllib2.Request(url)
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 \
        (KHTML, like Gecko) Chrome/24.0.1312.52 Safari/537.17")
    opener = urllib2.build_opener()
    return opener.open(req).read()


def unescape(s):
    r = s.replace('&#224;', 'à')
    return r