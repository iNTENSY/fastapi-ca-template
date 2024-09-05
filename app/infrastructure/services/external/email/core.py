import smtplib
from email.message import EmailMessage
from email.mime.text import MIMEText

from app.application.interfaces.email import IEmailService
from app.infrastructure.services.external.email.settings import EmailSettings


class EmailServiceImp(IEmailService):
    def __init__(self, conf: EmailSettings):
        self.__conf = conf

    def send_email(self, to: str, subject: str, body: str, message: EmailMessage = None):
        if message is None:
            message = self.__generate_message(to, subject, body)
        with smtplib.SMTP(self.__conf.host, self.__conf.port) as server:
            server.starttls()
            server.login(self.__conf.login, self.__conf.password)
            server.sendmail(
                from_addr=self.__conf.login,
                to_addrs=to,
                msg=message.as_string()
            )

    def __generate_message(self, to: str, subject: str, body: str) -> MIMEText:
        message = MIMEText(body, _charset='utf-8')
        message['From'] = self.__conf.login
        message['To'] = to
        message['Subject'] = subject
        return message
