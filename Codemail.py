import smtplib
email_user='yourmail'
email_send='towho?'
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email_user,'password')
message='Hi there,sending this email from python'
server.sendmail(email_user,email_send,message)
server.quit()
