#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import urllib


class HtmlDownloader(object):

    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        if response.getcode() != 200:
            return None
        return response.read()#返回下载好的内容