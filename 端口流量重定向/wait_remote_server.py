import argparse
import socket
import errno
from time import time as now
#等待远程网络服务上线。
DEFAULT_TIMEOUT = 120
DEFAULT_SERVER_HOST = 'localhost'
DEFAULT_SERVER_PORT = 80

class NETServiceCheckr(object):
    def __init__(self,host,port,timeout=DEFAULT_TIMEOUT):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    def end_wait(self):
        self.sock.close()
    def check(self):
        if self.timeout:
            end_time = now()+self.timeout#结束时间=当前时间+总共的剩余时间。这样组成一个总共的时间轴。
        while True:
            try:
                if self.timeout:
                    next_timeout = end_time - now()#now为当前时间戳，下次探测所剩下的时间=结束时间减去当前时间。
                    print(now())
                    if next_timeout < 0:
                        return False
                    else:
                        print("setting socket next timeout %ss"%round(next_timeout))
                        self.sock.settimeout(next_timeout)#重新设置socket的timeout时间属性。
                self.sock.connect((self.host,self.port))#一直链接，直到timeout
            except socket.error as e:
                print("exception:%s"%e)
            else:
                self.end_wait()
                return True
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='wait for network server')
    parser.add_argument('--host',action="store",dest="host",default=DEFAULT_SERVER_HOST)
    parser.add_argument('--port',action="store",dest="port",type=int,default=DEFAULT_SERVER_PORT)
    parser.add_argument('--timeout',action="store",dest="timeout",type=int,default=DEFAULT_TIMEOUT)
    given_args = parser.parse_args()
    host,port,timeout = given_args.host,given_args.port,given_args.timeout
    service_checker = NETServiceCheckr(host,port,timeout=timeout)
    print("checking for network service %s:%s..."%(host,port))
    if service_checker.check():
        print("service is available again")
