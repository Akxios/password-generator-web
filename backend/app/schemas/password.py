from pydantic import BaseModel, Field, model_validator

from backend.config import (
    DEFAULT_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)


class PasswordGenerateRequest(BaseModel):
    length: int = Field(
        DEFAULT_PASSWORD_LENGTH, ge=MIN_PASSWORD_LENGTH, le=MAX_PASSWORD_LENGTH
    )
    use_lower: bool = Field(True, description="Использование маленьких букв")
    use_upper: bool = Field(True, description="Использование заглавных букв")
    use_digits: bool = Field(True, description="Использование цифр")
    use_special: bool = Field(True, description="Использование специальных символов")

    @model_validator(mode="after")
    def at_least_one_charset(self):
        if not any([self.use_lower, self.use_upper, self.use_digits, self.use_special]):
            raise ValueError("At least one character set must be enabled")
        return self


class PasswordCheckRequest(BaseModel):
    password: str = Field(..., min_length=4, max_length=128, description="Пароль")


class PasswordAnalysis(BaseModel):
    entropy: float = Field(..., description="Энтропия пароля в битах")
    length: int = Field(..., description="Длина пароля")
    unique_ratio: float = Field(..., description="Доля уникальных символов")
    repeat_ratio: float = Field(..., description="Доля повторяющихся паттернов")
    ascii_sequence: int = Field(
        ..., description="Максимальная длина ASCII-последовательности"
    )
    keyboard_sequence: int = Field(
        ..., description="Максимальная длина клавиатурной последовательности"
    )
    digits_only: bool = Field(..., description="Только цифры?")
    in_dictionary: bool = Field(
        ..., description="Пароль встречается в словаре популярных паролей?"
    )


class PasswordGenerateResponse(PasswordAnalysis):
    password: str = Field(..., description="Сгенерированный пароль")


class PasswordCheckResponse(PasswordAnalysis):
    pass
