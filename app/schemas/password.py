from typing import List, Optional

from pydantic import BaseModel, Field, model_validator

from app.config import (
    DEFAULT_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
)


class PasswordGenerateRequest(BaseModel):
    length: int = Field(
        DEFAULT_PASSWORD_LENGTH, ge=MIN_PASSWORD_LENGTH, le=MAX_PASSWORD_LENGTH
    )
    use_lower: bool = Field(True)
    use_upper: bool = Field(True)
    use_digits: bool = Field(True)
    use_special: bool = Field(True)

    @model_validator(mode="after")
    def at_least_one_charset(self):
        if not any([self.use_lower, self.use_upper, self.use_digits, self.use_special]):
            raise ValueError("At least one character set must be enabled")
        return self


class PasswordCheckRequest(BaseModel):
    # Разрешаем проверять даже 1 символ
    password: str = Field(..., min_length=1, max_length=128)


class CrackTimes(BaseModel):
    online_throttling_100_per_hour: str = Field(
        ..., description="Онлайн (ограничение скорости)"
    )
    online_no_throttling_10_per_second: str = Field(
        ..., description="Онлайн (без ограничений)"
    )
    offline_slow_hashing_1e4_per_second: str = Field(
        ..., description="Офлайн (медленный хеш, bcrypt)"
    )
    offline_fast_hashing_1e10_per_second: str = Field(
        ..., description="Офлайн (быстрый хеш, MD5)"
    )


class PasswordAnalysis(BaseModel):
    score: int = Field(..., ge=0, le=4, description="Оценка сложности (0-4)")
    crack_times_display: CrackTimes = Field(
        ..., description="Время взлома в разных сценариях"
    )
    guesses: float = Field(..., description="Расчетное количество попыток")
    warning: Optional[str] = Field(None, description="Предупреждение")
    suggestions: List[str] = Field(default_factory=list, description="Советы")


class PasswordGenerateResponse(PasswordAnalysis):
    password: str = Field(..., description="Сгенерированный пароль")


class PasswordCheckResponse(PasswordAnalysis):
    pass
