from pydantic import BaseModel, Field, model_validator
from fastapi import Form
from backend.src.schemas.password import PasswordGenerateRequest


class PasswordGenerateForm(PasswordGenerateRequest):
    @classmethod
    def from_form(cls, form_data: dict):
        """Преобразует данные из HTML Form в объект формы"""
        return cls(
            length=int(form_data.get("length", 12)),
            use_lower=bool(form_data.get("use_lower")),
            use_upper=bool(form_data.get("use_upper")),
            use_digits=bool(form_data.get("use_digits")),
            use_special=bool(form_data.get("use_special")),
        )
