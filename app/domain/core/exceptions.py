class DomainError(Exception):
    """Base class for exceptions in this module."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class DomainValidationError(DomainError):
    """Exception for domain validation errors"""

    def __init__(self, message: str = "Validation Error") -> None:
        super().__init__(message=message)


class InternalServerError(DomainError):
    """An exception is used when an unexpected error occurs."""

    def __init__(self) -> None:
        super().__init__(message="Internal server error")


class IntegrityError(DomainError):
    def __init__(self) -> None:
        super().__init__(message="Your data conflicts with existing data")
