import imaplib
import email

def check_inbox(auth_code):
    try:
        mail = imaplib.IMAP4_SSL('imap.163.com')
        mail.login('pulsareon@163.com', auth_code)
        mail.select('inbox')
        
        # 搜索所有未读邮件
        status, messages = mail.search(None, 'UNSEEN')
        print(f"Status: {status}, New messages: {len(messages[0].split())}")
        
        # 搜索关于退信的关键词
        status, bounce_msgs = mail.search(None, 'SUBJECT "退信"')
        print(f"Bounce reports found: {len(bounce_msgs[0].split())}")
        
        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    check_inbox("GFwyAcYZmLt7eqXY")
