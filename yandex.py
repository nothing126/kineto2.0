from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import config


def send_message(to, subj, txt):
    msg = MIMEMultipart()
    msg['From'] = config.MAIL
    msg['To'] = to
    msg['Subject'] = subj
    msg.attach(MIMEText(txt, 'plain'))

    # Используем SMTP_SSL и порт 465 для безопасного подключения
    server = smtplib.SMTP_SSL(config.SMTP_SERV, 465)

    # Приветствие сервера
    server.ehlo(config.MAIL)

    # Вход в учетную запись с помощью вашего адреса электронной почты и пароля
    server.login(config.SMTP_LOG, config.SMTP_PASS)

    # Отправка сообщения
    server.sendmail(config.MAIL, to, msg.as_string())

    # Завершение сессии SMTP
    server.quit()
