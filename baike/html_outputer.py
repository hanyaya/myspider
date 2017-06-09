#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
class HtmlOutputer(object):

    def __init__(self):
        self.datas = []


    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = open('output.html', 'w',encoding='utf-8')
        fout.write("<html>")
        fout.write("<head>")
        fout.write("<meta http-equiv='Content-type' content='charset=UTF-8'>")
        fout.write("</head>")
        fout.write("<body>")
        fout.write("<table>")

        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'])#encode('utf-8'))
            fout.write("<td>%s</td>" % data['summary'])
            #此处不能用encode（utf-8）utf-8否则，会把汉字转换为其他符号
            print (data['title'].encode('utf-8'))
            fout.write("</tr>")
        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")
        fout.close()