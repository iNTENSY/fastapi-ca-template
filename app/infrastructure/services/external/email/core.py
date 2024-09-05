from email.message import EmailMessage
from email.mime.text import MIMEText

from app.application.interfaces.email import IEmailService
from app.infrastructure.services.external.email.settings import EmailSettings
from app.infrastructure.services.external.email.tasks import send_verification_code


class EmailServiceImp(IEmailService):
    def __init__(self, conf: EmailSettings):
        self.__conf = conf

    def send_email(self, message: EmailMessage) -> None:
        send_verification_code.delay(
            conf=vars(self.__conf),
            to=message['to'],
            message=message.as_string()
        )

    def generate_simple_message(self, to: str, subject: str, body: str) -> MIMEText:
        message = MIMEText(body, _charset='utf-8')
        message['From'] = self.__conf.login
        message['To'] = to
        message['Subject'] = subject
        return message
