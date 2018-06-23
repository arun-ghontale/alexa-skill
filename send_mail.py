import smtplib
import email
print(dir(email))
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
 
fromaddr = "arun.g.ghontale@gmail.com"
toaddr = "ghontale.arun.agg@gmail.com"
 
msg = MIMEMultipart()
 
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = "Log stats attached to this file"
 
body = "Attached are the logs and the log stats which was requested"
 
msg.attach(MIMEText(body, 'plain'))
 
filename = "logs.txt"
attachment = open(filename, "rb")
part = MIMEBase('application', 'octet-stream')
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)

filename = "log_stats.txt"
attachment = open(filename, "rb")
part1 = MIMEBase('application', 'octet-stream')
part1.set_payload((attachment).read())
encoders.encode_base64(part1)
part1.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 msg.attach(part1)
 
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(fromaddr, 'arungg118211477')
text = msg.as_string()
server.sendmail(fromaddr, toaddr, text)
server.quit()