from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import globalconfig as cfg

def sendemailreport(message):
    fromaddr = cfg.smtp['email']
    toaddr = cfg.smtp['email']
#connect(cfg.mysql['host'], cfg.mysql['user'], cfg.mysql['password'])
    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Reporting Rig Status"

    body = message

    msg.attach(MIMEText(body, 'plain'))

    filename = cfg.logfilename
    attachment = open(filename, "rb")

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(part)

    server = smtplib.SMTP(cfg.smtp['host'], cfg.smtp['port'])
    server.starttls()
    server.login(fromaddr, cfg.smtp['pass'])
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Email Sent!")
