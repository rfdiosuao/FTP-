import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

def start_ftp():
    # 配置
    USER = "rfdiosuao"
    PASSWORD = "Z66666666" # 用户之前修改的密码
    PORT = 21
    # 共享当前目录
    SHARED_DIR = os.getcwd()
    SHARED_DIR = "D:\ "    
    authorizer = DummyAuthorizer()
    
    # 权限说明: "elradfmwMT"
    # e - 改变目录
    # l - 列出文件
    # r - 从服务器检索文件
    # a - 将数据追加到现有文件
    # d - 删除文件或目录
    # f - 重命名文件或目录
    # m - 创建目录
    # w - 将文件存储到服务器
    # M - 更改文件模式/权限
    # T - 更改文件修改时间
    authorizer.add_user(USER, PASSWORD, SHARED_DIR, perm="elradfmwMT")
    
    # === 关键修改 ===
    # 为了解决 Windows 资源管理器中文乱码问题，
    # 我们需要强制使用 GBK 编码，而不是默认的 UTF-8。
    class GBK_FTPHandler(FTPHandler):
        # 覆盖默认编码
        encoding = 'gbk'
        
        def on_connect(self):
            print(f"[+] 新连接: {self.remote_ip}:{self.remote_port}")

    handler = GBK_FTPHandler
    handler.authorizer = authorizer
    
    # 配置被动模式端口范围
    handler.passive_ports = range(60000, 60100)
    
    # 绑定地址
    address = ("0.0.0.0", PORT)
    
    try:
        server = FTPServer(address, handler)
    except OSError as e:
        if "10013" in str(e) or "Permission denied" in str(e):
            print(f"错误: 无法绑定端口 {PORT}。可能需要管理员权限，或者端口已被占用。")
            print("尝试使用端口 2121...")
            PORT = 2121
            address = ("0.0.0.0", PORT)
            server = FTPServer(address, handler)
        else:
            raise e

    print("="*50)
    print(f"FTP 服务器已启动 (GBK 编码修复版)")
    print(f"共享目录: {SHARED_DIR}")
    print(f"地址: ftp://<你的服务器公网IP>:{PORT}")
    print(f"用户名: {USER}")
    print(f"密码: {PASSWORD}")
    print("="*50)
    print("请注意：")
    print("如果使用 Windows 资源管理器，请刷新或重新连接。")
    print("="*50)
    
    server.serve_forever()

if __name__ == "__main__":
    start_ftp()
