import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import easyimap

def send_email(smtpObj, sender, receiver, message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = message['subject']

    msg.attach(MIMEText(message['body']))

    for file in message['files']:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(file))
        msg.attach(part)
    print("sent")
    smtpObj.sendmail(sender, receiver, msg.as_string())


def redirect_email(username, password):
    imapper = easyimap.connect('imap.gmail.com', username, password)
    smtpObj = smtplib.SMTP('smtp.gmail.com:587')
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)
    for mail_id in imapper.listids(limit=100):
        mail = imapper.mail(mail_id)
        to = mail.to #"example+person+inbox+gmail+com@gmail.com"
        to = to.split("@")[0].split("+")[1:]
        name = "+".join(to[:-2])
        to = name + "@" + to[-2] + "." + to[-1]
        message = {'subject': mail.title, 'body': mail.body,
                   'files': mail.attachments}
        print("received")
        send_email(smtpObj, mail.from_addr, to, message)


if __name__=="__main__":
    username = 'compliance.accomplice@gmail.com'
    password = 'HackUIowa2018GG'
    redirect_email(username, password)
