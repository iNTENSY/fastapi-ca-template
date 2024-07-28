from app.domain.core.exceptions import DomainError


class InvalidTokenError(DomainError):
    def __init__(self):
        super().__init__(message="Invalid token")


class AccountNotFoundError(DomainError):
    def __init__(self):
        super().__init__(message="User not found")


class InvalidAccountDataError(DomainError):
    def __init__(self):
        super().__init__(message="Invalid user data")


class UserIsNotAuthorizedError(DomainError):
    def __init__(self):
        super().__init__(message="User is not authorized")


class UserBadPermissionError(DomainError):
    def __init__(self):
        super().__init__(message="User has bad permission")


class TokenExpiredError(DomainError):
    def __init__(self):
        super().__init__(message="Token has expired")


class InvalidTokenPayloadError(DomainError):
    def __init__(self):
        super().__init__(message="Token is not trusted")
