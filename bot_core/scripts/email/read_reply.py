import imaplib
import email
from email.header import decode_header

def get_body(msg):
    if msg.is_multipart():
        return get_body(msg.get_payload(0))
    else:
        return msg.get_payload(None, True).decode('utf-8', errors='ignore')

def read_reply():
    user = 'pulsareon@qq.com'
    auth_code = 'tpzgjudeepqlcaad'
    mail = imaplib.IMAP4_SSL('imap.qq.com')
    mail.login(user, auth_code)
    mail.select("inbox")
    
    status, messages = mail.search(None, 'ALL')
    message_ids = messages[0].split()
    latest_id = message_ids[-1]
    
    res, msg_data = mail.fetch(latest_id, "(RFC822)")
    for response_part in msg_data:
        if isinstance(response_part, tuple):
            msg = email.message_from_bytes(response_part[1])
            body = get_body(msg)
            print("--- REPLY CONTENT ---")
            print(body)
            print("----------------------")
    
    mail.close()
    mail.logout()

if __name__ == "__main__":
    read_reply()
