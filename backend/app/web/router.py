from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from backend.app.services.generate import generate_cryptographic_password
from backend.app.services.entropy import password_strength_report
from backend.app.schemas.password_form import PasswordGenerateForm

templates = Jinja2Templates(directory="frontend/templates")
router = APIRouter()

@router.post("/",
    response_class=HTMLResponse,
    summary="Генерация пароля на сайте",
)
async def generate_password(request: Request):
    form_data = await request.form()
    errors = []
    password = None
    entropy = None
    form = None

    try:
        form = PasswordGenerateForm.from_form(form_data)

        password = generate_cryptographic_password(
            form.length,
            form.use_lower,
            form.use_upper,
            form.use_digits,
            form.use_special,
        )

        entropy = password_strength_report(password)["entropy"]

    except (ValidationError, ValueError) as e:
        # единообразно собираем ошибки
        if hasattr(e, "errors"):  # Pydantic
            errors = [f"{' → '.join(map(str, err['loc']))}: {err['msg']}" for err in e.errors()]
        else:  # ValueError
            errors = [str(e)]

    form_values = form.model_dump() if form else {
        "length": int(form_data.get("length", 12)),
        "use_lower": bool(form_data.get("use_lower")),
        "use_upper": bool(form_data.get("use_upper")),
        "use_digits": bool(form_data.get("use_digits")),
        "use_special": bool(form_data.get("use_special")),
    }

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "errors": errors,
            "password": password,
            "entropy": entropy,
            **form_values,
        }
    )
