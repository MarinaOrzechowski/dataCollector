import email
import smtplib
from email.mime.text import MIMEText


def send_email(email, happiness, age, avg_happiness, is_happier, total_participants, happiest_age):
    from_email = "mishkice@gmail.com"
    from_password = "Orzechowski9225"
    to_email = email

    subject = "Happiness data"
    message = "Hello, <br>Thank you for participating in the survey! <br> <strong>%s</strong> people sent us their responses. The average level of happiness is <strong>%s</strong>. Your level of happiness is <strong>%s</strong>. You are <strong>%s</strong> than an average person. <br>Survey showed that <strong>%s</strong> is the happiest age!<br><br><br> Regards,<br> Happiness Data Collector" % (
        total_participants, avg_happiness, happiness, is_happier, happiest_age)

    msg = MIMEText(message, 'html')
    msg['Subject'] = subject
    msg['To'] = to_email
    msg['From'] = from_email

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(from_email, from_password)
    gmail.send_message(msg)
