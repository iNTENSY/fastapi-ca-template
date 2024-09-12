import logging
import sys

from app.application.interfaces.logger import ILogger
from app.infrastructure.services.internal.logger.config import LoggerSettings


class LoggerImp(ILogger):
    def __init__(self, settings: LoggerSettings):
        self.__settings = settings
        self.__logger = logging.getLogger(settings.name)
        self.__logger.setLevel(settings.level)
        self.__initialize_handlers()

    def __initialize_handlers(self) -> None:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        file_handler = logging.FileHandler(filename=self.__settings.filename, encoding='utf-8')
        file_handler.setFormatter(logging.Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
        self.__logger.addHandler(stream_handler)
        self.__logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        self.__logger.debug(message)

    def info(self, message: str) -> None:
        self.__logger.info(message)

    def warning(self, message: str) -> None:
        self.__logger.warning(message)

    def error(self, message: str) -> None:
        self.__logger.error(message)

    def critical(self, message: str) -> None:
        self.__logger.critical(message)
