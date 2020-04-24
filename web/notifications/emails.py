import smtplib

from django.conf import settings


def send_email(to_addr, subject, body_text):
    from_addr = settings.GMAIL_SMTP_USER
    body = "\r\n".join((
        "From: %s" % settings.GMAIL_SMTP_USER,
        "To: %s" % to_addr,
        "Subject: %s" % subject,
        "",
        body_text
    ))
    server = smtplib.SMTP_SSL(settings.GMAIL_SMTP_HOST, settings.GMAIL_SMTP_PORT)
    server.ehlo()
    server.login(settings.GMAIL_SMTP_USER, settings.GMAIL_SMTP_PASSWORD)
    server.sendmail(from_addr, [to_addr], body)
    server.quit()


def get_notification_body(place, description, emails, onset, created):
    emails_string = ', '.join(emails)
    body_text = f"""
        Place: {place}\n
        Description: {description}\n
        Participants: {emails_string}\n
        Onset at: {onset}\n
        Created at: {created}\n
    """
    return body_text
