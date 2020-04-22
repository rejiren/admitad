import smtplib

gmail_user = 'admitad.test.task@gmail.com'
gmail_password = '^8yh_09JK'


def send_email():#host, subject, to_addr, from_addr, body_text):
    host = "mySMTP.server.com"
    subject = "Test email"
    to_addr = "sfgsdfgdfsgdfsg@2go-mail.com"
    from_addr = gmail_user
    body_text = "Pupiru!!!!!"

    BODY = "\r\n".join((
        "From: %s" % from_addr,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    ))
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(gmail_user, gmail_password)

    server.sendmail(from_addr, [to_addr], BODY)
    server.quit()
