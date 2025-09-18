import smtplib
import ssl
import uuid
from email.mime.text import MIMEText
from email.utils import formataddr


class SMTPClient:
    def __init__(self, from_addr, password, host='smtp.gmail.com', port=587):
        '''
        初始化
        :param from_addr: 发送者
        :param password: 密码
        :param host: 邮箱服务器
        :param port: 端口
        '''
        # 初始化
        self.from_addr = from_addr
        self.password = password
        self.host = host
        self.port = port
        self.server = None

    def connect(self):
        '''
        SMTP 服务连接
        :return:
        '''
        context = ssl.create_default_context()
        server = smtplib.SMTP_SSL(host=self.host, port=self.port, context=context, timeout=10)
        # server.set_debuglevel(1)
        server.login(self.from_addr, self.password)
        self.server = server
        print('已建立连接')
        return server

    def send(self, msg, to_addrs):
        '''
        邮件发送
        :param msg:
        :param to_addrs:
        :return:
        '''
        if not self.server:
            raise Exception('未建立连接')
        self.server.send_message(msg, from_addr=self.from_addr, to_addrs=to_addrs)
        print(f'发送成功')

    def close(self):
        '''
        断开连接
        :return:
        '''
        if self.server:
            self.server.quit()
            self.server = None
        print('连接已关闭')

    def update_host(self, host):
        '''
        更新 host
        :param host:
        :return:
        '''
        self.host = host

    def update_port(self, port):
        '''
        更新 port
        :param port:
        :return:
        '''
        self.port = port


def send_email():
    from_addr = '1836140285@qq.com'
    to_addr = "156175469@qq.com"
    password = "wdtmjddhkhbhcaif"
    port = 587
    host = "smtp.qq.com"

    uuid_str = str(uuid.uuid4())
    msg = MIMEText("正文内容", "plain", "utf-8")
    msg["Subject"] = f"测试邮件：{uuid_str}"
    msg["From"] = formataddr(("你的昵称", from_addr))
    msg["To"] = to_addr

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
        server.set_debuglevel(1)
        server.login(from_addr, password)
        server.send_message(msg, from_addr=from_addr, to_addrs=[to_addr])
        server.quit()


def run():
    # send_email()
    from_addr = '1836140285@qq.com'
    to_addr = "156175469@qq.com"
    password = "xmzoxpbvpzeeciga"
    port = 587
    host = "smtp.qq.com"

    uuid_str = str(uuid.uuid4())
    msg = MIMEText("正文内容", "plain", "utf-8")
    msg["Subject"] = f"测试邮件：{uuid_str}"
    msg["From"] = formataddr(("你的昵称", from_addr))
    msg["To"] = to_addr

    my_smtp = SMTPClient(from_addr, password, host, port)
    my_smtp.connect()
    my_smtp.send(msg, to_addrs=[to_addr])
    my_smtp.close()


if __name__ == '__main__':
    run()
