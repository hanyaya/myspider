import ftplib

FTP_SERVER_URL = 'ftp.kernel.org'#ftp服务器的地址

def test_ftp_connection(path,username,email):
    ftp = ftplib.FTP(path,username,email)#创建一个会话，
    ftp.cwd("/pub")#切换工作目录。
    print("file list at %s :"%path)
    files = ftp.dir()#返回目录的文件结构，
    print(files)

    ftp.quit()#终止会话。
if __name__=='__main__':
    test_ftp_connection(path=FTP_SERVER_URL,username='anonymous',email='hobody@nourl.com')