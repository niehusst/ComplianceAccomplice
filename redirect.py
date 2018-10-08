import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import os
import easyimap
import time
import random
from cloud import SentimentParse
from wordParser import WordParser

#HI LIAM

#Parameters
##smtpObj: a smtp connection to the server
##sender: our username plus information about the original sender
##receiver: the email address the message will be sent to
##message: a dictionary with the subject, reply-to (original sender), body, and any attachments
def send_email(smtpObj, sender, receiver, message, dir):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = message['subject']
    msg['reply-to'] = message['reply']
    msg.attach(MIMEText(message['body'], 'html'))
    if dir:
        files = os.listdir(dir)
        for file in files:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(dir + file, 'rb').read())
            encode_base64(part)
            part.add_header('Content-Disposition', 'attachment; filename="%s"'
                            % os.path.basename(file))
            msg.attach(part)
    if sender == username: #logo in reply
        part = MIMEBase('application', 'octet-stream') #attach logo
        part.set_payload(open("res/logo.png", 'rb').read())
        encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                        % os.path.basename("logo.png"))
        msg.attach(part) #logo attached
    print("Sent to ", receiver)
    smtpObj.sendmail(sender, receiver, msg.as_string())


def handle_attachments(atts):
    if len(atts) == 0:
        return False
    try:
        dir = "atts/{}/".format(random.randint(0, 999999999999))
        os.makedirs(dir)
    except:
        handle_attachments(atts)
    for a in atts: #store in folder
        f = open(dir + a[0], "wb")
        f.write(a[1])
        f.close()
    return dir

#returns info on mail to be accepted and forwarded
def get_message_data_forward(mail, username):
    to = mail.to.split("@")[0].split("+")[1:] #"example+person+inbox+gmail+com@gmail.com"
    name = "+".join(to[:-2]) #Using negative indices to support arbitrary + in original email account
    to = name + "@" + to[-2] + "." + to[-1]
    message = {'reply': mail.from_addr, 'subject': mail.title,
               'body': mail.body}
    username = username.split("@")
    sender = "@".join(["+".join([username[0], mail.from_addr.replace("@", "+").replace(".", "+")]), username[1]]) #Injects sender's email address in plus fields of our email address
    return to, message, sender

#returns info on mail to be rejected and relayed back to the sender
def get_message_data_reply(mail, username, issues):
    to = mail.from_addr
    body = "\n".join(issues)
    body += "____ORIGINAL MESSAGE____\n"
    body += mail.body
    file = open("reply.html")
    html = file.read().replace("\n","<br>")
    html = html.format("<br>".join(issues), "<br>".join(mail.body.split("\n")))
    message = {'reply': mail.to,
               'subject': "Compliance Accomplice detected issues with \"" + mail.title + "\"",
               'body': html}
    return to, message, username

#THIS IS WHERE THE MAGIC HAPPENS
def detect_issues(mail):
    issues = []
    wp = WordParser(mail.title)
    wp.search_profanity()
    issues += wp.get_response()
    wp = WordParser(mail.body)
    wp.search_profanity()
    issues += wp.get_response()
    sp = SentimentParse()
    issues += sp.analyze_text(mail.body)
    return issues



#The main method, takes our gmail username and password
def redirect_email(username, password):
    imapper = easyimap.connect('imap.gmail.com', username, password) #connect to receive
    smtpObj = smtplib.SMTP('smtp.gmail.com:587') #connect to send
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(username, password)
    for mail in imapper.unseen(limit=100): #only grabs unread messages
        print("Received from ", mail.from_addr)
        if "Re: Compliance Accomplice detected issues with" in mail.title:
            print("Forwarding Initial Message")
            #Send original message
            sender = mail.to
            to = mail.to.split("@")[0].split("+")[1:]
            name = "+".join(to[:-2]) #Using negative indices to support arbitrary + in original email account
            to = name + "@" + to[-2] + "." + to[-1]
            message = {"reply": sender,
                       "subject": mail.title.split("\"")[1],
                       "body": mail.body.split("Your orignal message")[1].strip("</p>\
                   </div>\
               </div>\
               </body>\
               </html>")}
            send_email(smtpObj, sender, to, message, False)
        else: #New message to process
            dir = handle_attachments(mail.attachments)
            issues = detect_issues(mail)
            if len(issues) == 0: #No issues detected
                print("No issues detected.")
                to, message, sender = get_message_data_forward(mail, username)
            else:
                print("Issues detected")
                to, message, sender = get_message_data_reply(mail, username, issues)
            send_email(smtpObj, sender, to, message, dir)



if __name__=="__main__":
    #For security, store these as environment variables. I just use a throwaway gmail account. If you seriously intend to use this software, you will need to make your own mail account for this to go through
    username = 'compliance.accomplice@gmail.com'
    password = '***********'
    print("Started Compliance Accomplice email middleware system.")
    while(True):
        print("Checking for unread email...")
        redirect_email(username, password)
        time.sleep(10) #arbitrary, runs every 10 seconds
        os.system("rm -r atts/*")
