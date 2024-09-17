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


class AccountIsNotAuthorizedError(DomainError):
    def __init__(self):
        super().__init__(message="User is not authorized")


class AccountBadPermissionError(DomainError):
    def __init__(self):
        super().__init__(message="User has bad permission")


class TokenExpiredError(DomainError):
    def __init__(self):
        super().__init__(message="Token has expired")


class InvalidTokenPayloadError(DomainError):
    def __init__(self):
        super().__init__(message="Token is not trusted")


class CacheError(DomainError):
    def __init__(self, message: str):
        super().__init__(message)


class ActivationError(DomainError):
    def __init__(self, message: str):
        super().__init__(message=message)


class ValidationAPIError(DomainError):
    def __init__(self, message: str):
        super().__init__(message=message)
