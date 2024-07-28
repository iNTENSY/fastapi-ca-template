from typing import Optional

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from starlette.requests import Request
from starlette import status


class OAuth2PasswordBearerWithCookie(OAuth2PasswordBearer):
    """
    That class looks for `"access_token"` into `cookies` (not headers).
    """

    async def __call__(self, request: Request) -> Optional[str]:
        authorization = request.cookies.get("access_token")
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/v1/auth/login")
