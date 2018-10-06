import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import easyimap
import time

#HI LIAM

#Parameters
##smtpObj: a smtp connection to the server
##sender: our username plus information about the original sender
##receiver: the email address the message will be sent to
##message: a dictionary with the subject, reply-to (original sender), body, and any attachments
def send_email(smtpObj, sender, receiver, message):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = message['subject']
    msg['reply-to'] = message['reply']
    msg.attach(MIMEText(message['body']))

    for file in message['files']:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(file, 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename(file))
        msg.attach(part)
    print("Sent to ", receiver)
    smtpObj.sendmail(sender, receiver, msg.as_string())

#The main method, takes our gmail username and password
def redirect_email(username, password):
    imapper = easyimap.connect('imap.gmail.com', username, password) #connect to receive
    smtpObj = smtplib.SMTP('smtp.gmail.com:587') #connect to send
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)
    for mail in imapper.unseen(limit=100): #only grabs unread messages
        to = mail.to #"example+person+inbox+gmail+com@gmail.com"
        to = to.split("@")[0].split("+")[1:]
        name = "+".join(to[:-2]) #Using negative indices to support arbitrary + in original email account
        to = name + "@" + to[-2] + "." + to[-1]
        message = {'reply': mail.from_addr, 'subject': mail.title,
                   'body': mail.body, 'files': mail.attachments}
        username = username.split("@")
        sender = "@".join(["+".join([username[0], mail.from_addr.replace("@", "+").replace(".", "+")]), username[1]]) #Injects sender's email address in plus fields of our email address
        print("Received from ", mail.from_addr)
        send_email(smtpObj, sender, to, message)



if __name__=="__main__":
    #Alex would store these as environment variables. I just use a throwaway gmail account.
    username = 'compliance.accomplice@gmail.com'
    password = 'HackUIowa2018GG'
    print("Started Compliance Accomplice email middleware system.")
    while(True):
        print("Checking for unread email...")
        redirect_email(username, password)
        time.sleep(10) #arbitrary, runs every 10 seconds
