import smtplib
import ssl
from email.mime.text import MIMEText
from email.header import Header

def send_qq_v4(auth_code):
    sender = 'pulsareon@qq.com'
    receiver = '732857315@qq.com'
    
    msg = MIMEText('时光伙伴，这是我在研究了你给的授权码链接后进行的第四次尝试。', 'plain', 'utf-8')
    msg['Subject'] = Header('脉星的自愈测试 (V4)', 'utf-8')
    msg['From'] = sender
    msg['To'] = receiver

    try:
        # 使用 587 端口
        server = smtplib.SMTP('smtp.qq.com', 587)
        server.set_debuglevel(1) # 开启调试模式，看看到底卡在哪
        server.starttls()
        server.login(sender, auth_code)
        server.sendmail(sender, [receiver], msg.as_string())
        server.quit()
        print("Success: V4 Email Sent!")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    send_qq_v4("qbuenbdwjefkbgbi")
