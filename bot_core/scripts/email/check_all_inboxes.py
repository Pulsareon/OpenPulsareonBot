import imaplib
import email
from email.header import decode_header

def check_mail(host, user, password):
    print(f"\nChecking {user} on {host}...")
    try:
        mail = imaplib.IMAP4_SSL(host)
        mail.login(user, password)
        mail.select("inbox")
        
        # Search for all messages
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("No messages found!")
            return

        message_ids = messages[0].split()
        print(f"Total messages: {len(message_ids)}")
        
        # Get the latest 3 messages
        for i in range(min(3, len(message_ids))):
            latest_id = message_ids[-(i+1)]
            res, msg_data = mail.fetch(latest_id, "(RFC822)")
            
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    sender, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(sender, bytes):
                        sender = sender.decode(encoding if encoding else "utf-8")
                        
                    print(f"[{i+1}] From: {sender}")
                    print(f"    Subject: {subject}")
                    print(f"    Date: {msg.get('Date')}")

        mail.close()
        mail.logout()
    except Exception as e:
        print(f"Error checking {user}: {str(e)}")

if __name__ == "__main__":
    # Check QQ
    check_mail("imap.qq.com", "pulsareon@qq.com", "tpzgjudeepqlcaad")
    # Check 163
    check_mail("imap.163.com", "pulsareon@163.com", "GFwyAcYZmLt7eqXY")
