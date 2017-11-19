import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

user='robert.owens.capstone@gmail.com'
password='adminadmin'

s=smtplib.SMTP(host='smtp.gmail.com', port=587)
s.starttls()
s.login(user,password)

msg = MIMEMultipart()

message='test'

msg['From']='rbowensv@gmail.com'

msg["To"]='rbowensv@gmail.com'

msg['Subject']='This is a TEST'

msg.attach(MIMEText(message, 'plain'))

s.send_message(msg)

del msg
