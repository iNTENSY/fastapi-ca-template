from app.domain.accounts.exceptions import ValidationAPIError


class PasswordValidator:
    @staticmethod
    def validate(value: str) -> None:
        if len(value) < 8:
            raise ValidationAPIError("Пароль должен состоять минимум из 8 символов")

        if value.lower() == value:
            raise ValidationAPIError("Пароль должен содержать хотя бы один заглавный символ")
