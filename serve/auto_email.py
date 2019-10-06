
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import time

"""
自动发送邮件
"""


def email_send(title, content,to='1274560014@qq.com'):

    """
    title : 邮件标题
    content：邮件内容
    to：收件人
    """

    def _format_addr(s):

        name, addr = parseaddr(s)
        return formataddr((Header(name, 'utf-8').encode(), addr))


    # from_addr = 'fanspider@foxmail.com'
    # password = 'bcnsuqbfjpppcidh'  # 密码
    # to_addr = to
    # smtp_server = 'smtp.qq.com'

    # from_addr = 'fanspider@163.com'
    # password = 'lcy568972' # 密码
    # to_addr = to
    # smtp_server = 'smtp.163.com'

    from_addr = 'linchuyang1024@163.com'
    password = 'lcy568972'  # 密码
    to_addr = to
    smtp_server = 'smtp.163.com'
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('爬虫提示<%s>' % from_addr) # 发送者
    msg['To'] = _format_addr('管理员 <%s>' % to_addr) # 接收者
    msg['Subject'] = Header(title, 'utf-8').encode()

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

# if __name__ == '__main__':
#     nowtimes = time.asctime(time.localtime(time.time()))
#     email_send('你好erlla','认识一下\n')
