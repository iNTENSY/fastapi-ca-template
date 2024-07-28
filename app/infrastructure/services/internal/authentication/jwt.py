import datetime as dt
import uuid

from jose import jwt, JWTError, ExpiredSignatureError
from jose.exceptions import JWTClaimsError

from app.application.interfaces.jwt import IJwtProcessor
from app.application.interfaces.timezone import IDateTimeProcessor
from app.domain.accounts.exceptions import InvalidTokenError, TokenExpiredError, InvalidTokenPayloadError
from app.domain.core.value_objects import EmailVO, UuidVO
from app.infrastructure.settings.jwt import JwtSettings


class JwtProcessor(IJwtProcessor):
    def __init__(
            self,
            settings: JwtSettings,
            dt_processor: IDateTimeProcessor
    ) -> None:
        self.__settings = settings
        self.__dt = dt_processor
        self.__current_datetime = self.__dt.get_current_time()

    def generate_token(self, uid: uuid.UUID, email: str) -> str:
        issued_at = self.__current_datetime
        expiration_time = issued_at + dt.timedelta(seconds=self.__settings.expires_in)
        payload = {
            "iat": issued_at,
            "exp": expiration_time,
            "sub": str(uid),
            "email": email,
        }
        encoded_jwt = jwt.encode(payload, key=self.__settings.secret, algorithm=self.__settings.algorithm)
        return encoded_jwt

    def parse(self, token: str) -> tuple[UuidVO, EmailVO]:
        try:
            payload = jwt.decode(token, key=self.__settings.secret, algorithms=self.__settings.algorithm)
            return UuidVO(payload["sub"]), EmailVO(payload["email"])
        except ExpiredSignatureError:
            raise TokenExpiredError
        except JWTClaimsError:
            raise InvalidTokenPayloadError
        except JWTError:
            raise InvalidTokenError

    def refresh_token(self, token: str) -> str:
        payload = self.parse(token)
        return self.generate_token(*payload)
