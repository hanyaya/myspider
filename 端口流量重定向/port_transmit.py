import argparse
import asyncore
import socket

LOCAL_SERVER_HOST = 'localhost'
REMOTE_SERVER_HOST ='www.python.com'
BUFSIZE = 4096
#实现将一个端口接受到的数据，定向发送到目标地址跟端口，首先，要获取指定端口上收到的数据。然后将收到的数据发送到指定地址跟端口，
#receiver类，实现接受数据的功能，放入buffer中，sender类实现再次发送数据的功能，
class PortForwarder(asyncore.dispatcher):
    def __init__(self,ip,port,remoteip,remoteport,backlog=5):
        asyncore.dispatcher.__init__(self)#重载了asyncore.dispatcher。接着创建了一个socket。
        self.remoteip = remoteip
        self.remoteport = remoteport
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)#是类成员函数
        self.set_reuse_addr()
        self.bind((ip,port))
        self.listen(backlog)#backlog指定在拒绝连接之前，可以挂起的最大连接数量。

      #backlog等于5，表示内核已经接到了连接请求，但服务器还没有调用accept进行处理的连接个数最大为5
      #这个值不能无限大，因为要在内核中维护连接队列
    def handle_accept(self):#重写了accept函数。handle_accept: a new incoming connection can be accept()ed. Call the accept() method really accept the connection. To create a server socket,
                            # call the bind() and listen() methods on it first.
        conn,addr = self.handle_accept()
        print("connected to",addr)
        Sender(Receiver(conn),self.remoteip,self.remoteport)#发送receiver接受到的消息到指定的地址跟端口。
class Receiver(asyncore.dispatcher):
    def __init__(self,conn):
        asyncore.dispatcher.__init__(self,conn)
        self.from_remote_buffer = ''
        self.to_remote_buffer = ''
        self.sender = None
    def handle_connect(self):# connection to remote endpoint has been made. To initiate the connection, first call the connect() method on it.
        pass
    def handle_read(self):     #writable和readable在检测到一个socket可以写入或者检测到数据到达的时候，
                                         # 被调用，并返回一个bool来决定是否handle_read或者handle_write
        read = self.recv(BUFSIZE) #读取到的东西是recv收到的数据，
        self.from_remote_buffer +=read
    def writable(self):
        return (len(self.to_remote_buffer)>0)
    def handle_write(self):
        sent = self.send(self.to_remote_buffer)
        self.to_remote_buffer = self.to_remote_buffer[sent:]
    def handle_close(self):
        self.close()
        if self.sender:
            self.sender.close()
class Sender(asyncore.dispatcher):
    def __init__(self,receiver,remoteaddr,remoteport):
        asyncore.dispatcher.__init__(self)
        self.receiver = receiver
        receiver.sender = self
        self.create_socket(socket.AF_INET,socket.SOCK_STREAM)
        self.connect((remoteaddr,remoteport))
    def handle_connect(self):
        pass
    def handle_read(self):
        read = self.recv(BUFSIZE)#将读取到的数据放入一个变量中。
        self.receiver.to_remote_buffer += read
    def writable(self):
        return (len(self.receiver.from_remote_buffer)>0)
    def handle_write(self):
        sent =self.send(self.receiver.from_remote_buffer)#实现发送数据（从那个端口上接收到的）的功能，
        self.receiver.from_remote_buffer = self.receiver.from_remote_buffer[sent:]
    def handle_close(self):
        self.close()
        self.receiver.close()
if __name__=='__main__':
    parser = argparse.ArgumentParser(description='stackless socket server example')
    parser.add_argument('--local-host',action="store",dest="local_host",default=LOCAL_SERVER_HOST)
    parser.add_argument('--local-port',action="store",dest="local_port",type = int,required = True)
    parser.add_argument('--remote-host',action="store",dest="remote_host",default=REMOTE_SERVER_HOST)
    parser.add_argument('--remote-port',action="store",dest="remote_port",default=80,type=int)
    given_args = parser.parse_args()
    local_host,remote_host = given_args.local_host,given_args.remote_host
    local_port,remote_port = given_args.local_port,given_args.remote_port
    print("starting port forwarding local %s:%d => remote %s:%d "%(local_host,local_port,remote_host,remote_port))
    PortForwarder(local_host,local_port,remote_host,remote_port)
    asyncore.loop()#loop()函数检测到一个空的channel，将退出循环，程序完成任务，exit。loop实现轮询，在时间片中轮询。

