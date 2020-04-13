import imapclient
import pprint
import pyzmail
import smtplib
import configparser 
import sys
from email.message import EmailMessage
from email.parser import Parser as EmailParser
import imaplib
imaplib._MAXLINE = 10000000 #To display full subject line

# Fetch email and password from config file
cp = configparser.ConfigParser()
cp.read('credentials.cfg')
email = pswd = None
for each_section in cp.sections():
    for k,v in cp.items(each_section):
        if k == "email":
            email = v
        if k == "password":
            pswd = v
if not email or not pswd:
    sys.exit("Username or password not found please check your config file")
else:
    print("Email and password retrieved from the config file")

# Setup smtp
smtpObj = smtplib.SMTP('smtp.gmail.com',port=587)
smtpResponse = smtpObj.ehlo()
if smtpResponse[0] == 250:
        print("SMTP connection successful")
else:
    sys.exit("Exiting...Please check connection settings")

smtpTLSresponse = smtpObj.starttls()
if smtpTLSresponse[0] == 220:
    print("SMTP now in TLS mode")
else:
    sys.exit("Exiting...Please check TLS settings")

login_status = smtpObj.login(email, pswd)
if login_status[0] == 235:
    print("Logged in Succesfully")
else:
    sys.exit("Unable to login please check your credentials")

#compose email
msg = EmailMessage()
msg.set_content('Hello Human hope you are doing good')
msg['Subject'] = "Automated email"
msg['From'] = email
msg['To'] = 'newfortesting@gmail.com'

#Send email    
# sent_status = smtpObj.send_message(msg)
# print("Email send status: {}".format(sent_status))

smtpObj.quit()

#imap setup for retrieving emails
imapObj = imapclient.IMAPClient('imap.gmail.com', ssl=True)
imapObj.login(email, pswd)
# pprint.pprint(imapObj.list_folders())
imapObj.select_folder('INBOX', readonly=True) #Change readonly to False for deleting
UIDS = imapObj.search(['ALL'])
#UIDS = imapObj.search(['OR','FROM', 'newfortesting@gmail.com', 'SINCE', dt.date(2020,4,12)])

# pprint.pprint(UIDS)
rawMessages = imapObj.fetch(UIDS[-10:], ['BODY[]'])
# pprint.pprint(rawMessages)

for k,v in rawMessages.items():
    message = pyzmail.PyzMessage.factory(rawMessages[k][b'BODY[]'])
    print("Email subject: {}".format(message.get_subject()))
    # if message.text_part:
        # print(message.text_part.get_payload().decode(message.text_part.charset))