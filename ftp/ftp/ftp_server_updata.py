import os
import argparse
import ftplib
import getpass
#因为无本地ftp服务器，所以脚本执行后不会上传
LOCAL_FTP_SERVER = 'localhost'
LOCAL_FILE = 'readme.txt'

def ftp_upload(ftp_server,username,password,file_name):
    print("connecting to ftp server:%s"%ftp_server)
    ftp = ftplib.FTP(ftp_server)#构造一个会话 ，返回一个句柄。
    print("login to ftp server: user=%s"%username)
    ftp.login(username,password)#用于连接的用户名，密码
    ext = os.path.splitext(file_name)[1]#分离文件名与扩展名；默认返回(fname,fextension)元组，可做分片操作。勇索引读取。
    if ext in (".txt",".htm",".html"):
        ftp.storlines("STOR"+file_name,open(file_name))
    else:
        ftp.storbinary("STOR"+file_name,open(file_name,"rb"),1024)#上传目标文件，指令处理二进制文件，要给定文件对象。
    print("uploaded file ：%s"%file_name)
if __name__=='__main__':
    parser = argparse.ArgumentParser(description="ftp server upload example")
    parser.add_argument('--ftp-server',action="store",dest="ftp_server",default=LOCAL_FTP_SERVER)
    parser.add_argument('--file-name',action="store",dest="file_name",default=LOCAL_FILE)
    parser.add_argument('--username',action="store",dest="username",default=getpass.getuser())
    given_args = parser.parse_args()
    ftp_server,file_name,username = given_args.ftp_server,given_args.file_name,given_args.username
    password = getpass.getpass(prompt="enter your password:")
    ftp_upload(ftp_server,username,password,file_name)
