#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import re

import urllib
from bs4 import BeautifulSoup


class HtmlParser(object):

    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return

        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        links = soup.find_all('a', href=re.compile(r"/view/\d+\.htm"))#传了正则表达式。\d 表示匹配数字，匹配的是/vies/.后面跟的是数字。
                                                                      #以/.htm结尾。+表示无数次匹配。
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)#newurl按照pageurl的格式连接成一个完整的
            new_urls.add(new_full_url)
        return new_urls


    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url

        res_data['url'] = page_url
        # <dd class="lemmaWgt-lemmaTitle-title"><h1>Python</h1>
        title_node = soup.find('dd', class_= "lemmaWgt-lemmaTitle-title").find("h1")
        res_data['title'] = title_node.get_text()

        summary_node = soup.find('div', class_="lemma-summary")
        res_data['summary'] = summary_node.get_text()
        return res_data
