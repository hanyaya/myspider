import os
import cgi
import argparse
import BaseHTTPServer
import CGIHTTPServer
import cgitb
cgitb.enable()

def web_server(port):
    server = BaseHTTPServer.HTTPServer
    handler = CGIHTTPServer.CGIHTTPRequestHandler
    server_address = ("",port)
    handler.cgi_directories = ["/cgi-bin",]
    httpd = server(server_address,handler)
    print("starting web server with CGI support on port :%s"%port)
    httpd.server_forever()

if __name__ =='__main__':
    parser = argparse.ArgumentParser(description="CGI SERVER EXAMPLE")
    parser.add_argument('--port',action="store",dest="port",type=int,required=True)
    given_args = parser.parse_args()
    web_server(given_args.port)
