__author__ = 'JYC'

import os, smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.header import Header
from email import encoders
from mimetypes import guess_type

class Sender:
    def __init__(self, mail_id, pw):
        self.mail_id = mail_id
        self.pw = pw
        self.smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        self.smtpserver.ehlo()
        self.smtpserver.starttls()
        self.smtpserver.ehlo()
        self.smtpserver.login(mail_id, pw)

    def __del__(self):
         self.smtpserver.close()


    def send_gmail(self, to, subject, text, html, attach):
        msg = MIMEMultipart()
        msg['From'] = self.mail_id
        msg['To'] = to
        msg['Subject'] = Header(subject, 'utf-8')
        mimetext = MIMEText(text, 'plain', 'utf-8')
        msg.attach(mimetext)

        mimetype, encoding = guess_type(attach)
        mimetype = mimetype.split('/', 1)
        fp = open(attach, "rb")

        part = MIMEBase(mimetype[0], mimetype[1])
        part.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(part)

        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attach))
        msg.attach(part)
        self.smtpserver.sendmail(self.mail_id, to, msg.as_string())

if __name__=="__main__":
    sender = Sender('', '')
    

