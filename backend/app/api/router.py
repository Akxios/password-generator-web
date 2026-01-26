from fastapi import APIRouter

from backend.app.schemas.password import (
    PasswordCheckRequest,
    PasswordCheckResponse,
    PasswordGenerateRequest,
    PasswordGenerateResponse,
)
from backend.app.services.entropy import password_strength_report
from backend.app.services.generate import generate_cryptographic_password

router = APIRouter(prefix="/api")


@router.post(
    "/generate",
    response_model=PasswordGenerateResponse,
    summary="Генерация пароля",
    description="Генерирует криптографически стойкий пароль и считает энтропию",
)
async def api_password_generate(data: PasswordGenerateRequest):
    password = generate_cryptographic_password(
        length=data.length,
        use_lower=data.use_lower,
        use_upper=data.use_upper,
        use_digits=data.use_digits,
        use_special=data.use_special,
    )

    report = password_strength_report(password)
    report["password"] = password

    return report


@router.post(
    "/check",
    response_model=PasswordCheckResponse,
    summary="Проверка пароля",
    description="Считает энтропию пароля",
)
async def api_password_check(data: PasswordCheckRequest):
    password = data.password
    report = password_strength_report(password)
    report["password"] = password

    return report
