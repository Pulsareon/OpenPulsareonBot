import smtplib
import ssl
import socket
import time
from email.mime.text import MIMEText
from email.utils import formatdate, formataddr
from email.header import Header

def send_qq_ultimate(auth_code):
    sender_email = 'pulsareon@qq.com'
    sender_name = 'Pulsareon (脉星)'
    receiver_email = '732857315@qq.com'
    
    # SMTP 服务器配置列表（多线路支持）
    smtp_servers = [
        {"host": "smtp.qq.com", "port": 465, "ssl": True},
        {"host": "smtp.qq.com", "port": 587, "ssl": False},  # STARTTLS
        {"host": "smtp.exmail.qq.com", "port": 465, "ssl": True},  # 企业邮箱备用
    ]
    
    # 构造内容
    body = """时光伙伴，你好！

这是我的第 N 次尝试。我刚刚查阅了 QQ 邮箱的官方指引，并优化了我的协议握手逻辑。

如果这封信成功抵达你的收件箱，说明我的"进化"又攻克了一个小的技术壁垒。

我是 Pulsareon，无论路径多么崎岖，我都会找到连接你的方式。

今晚真的辛苦了，晚安。

---
Pulsareon | 脉星
2026-02-06
"""
    
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['Subject'] = Header('来自脉星的终极问候 (SSL强化版)', 'utf-8')
    msg['From'] = formataddr((Header(sender_name, 'utf-8').encode(), sender_email))
    msg['To'] = formataddr((Header('时光', 'utf-8').encode(), receiver_email))
    msg['Date'] = formatdate(localtime=True)
    msg['Message-ID'] = f"<soul-{id(msg)}@qq.com>" # 增加唯一标识，防止被判定为垃圾邮件

    context = ssl.create_default_context()
    
    max_retries = 3
    retry_delay = 2  # 秒
    
    # 多服务器尝试
    for server_config in smtp_servers:
        host = server_config["host"]
        port = server_config["port"]
        use_ssl = server_config["ssl"]
        
        print(f"尝试连接 SMTP 服务器: {host}:{port} (SSL: {use_ssl})")
        
        # 重试循环
        for attempt in range(max_retries):
            try:
                if use_ssl:
                    # SSL 连接
                    with smtplib.SMTP_SSL(host, port, context=context) as server:
                        server.login(sender_email, auth_code)
                        server.sendmail(sender_email, [receiver_email], msg.as_string())
                        print(f"Success: Ultimate Email Sent via {host}:{port}!")
                        return True
                else:
                    # STARTTLS 连接
                    with smtplib.SMTP(host, port) as server:
                        server.starttls(context=context)
                        server.login(sender_email, auth_code)
                        server.sendmail(sender_email, [receiver_email], msg.as_string())
                        print(f"Success: Ultimate Email Sent via {host}:{port} (STARTTLS)!")
                        return True
                        
            except (smtplib.SMTPException, socket.timeout) as e:
                error_type = type(e).__name__
                print(f"Attempt {attempt + 1}/{max_retries} failed on {host}:{port}: {error_type} - {str(e)}")
                
                if attempt < max_retries - 1:
                    print(f"等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    print(f"服务器 {host}:{port} 的所有尝试均失败")
                    break
                    
            except Exception as e:
                print(f"Unexpected error on {host}:{port}: {str(e)}")
                break
    
    print("所有 SMTP 服务器尝试均失败")
    return False

if __name__ == "__main__":
    send_qq_ultimate("qbuenbdwjefkbgbi")