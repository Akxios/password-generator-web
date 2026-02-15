import math

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from app.schemas.password_form import PasswordGenerateForm
from app.services.entropy import password_strength_report
from app.services.generate import generate_cryptographic_password

templates = Jinja2Templates(directory="app/web/templates")
router = APIRouter()


@router.post(
    "/",
    response_class=HTMLResponse,
    summary="Генерация пароля на сайте",
)
async def generate_password(request: Request):
    form_data = await request.form()
    errors = []
    password = None
    report = {}
    form = None
    guesses_log = 0

    try:
        form = PasswordGenerateForm.from_form(form_data)

        password = generate_cryptographic_password(
            length=form.length,
            use_lower=form.use_lower,
            use_upper=form.use_upper,
            use_digits=form.use_digits,
            use_special=form.use_special,
        )

        report = password_strength_report(password)

        # <--- 3. Считаем логарифм здесь (Python это умеет, а Jinja нет)
        guesses = report.get("guesses", 0)
        if guesses > 0:
            guesses_log = math.log10(guesses)

    except (ValidationError, ValueError) as e:
        if hasattr(e, "errors"):
            errors = [
                f"{' → '.join(map(str, err['loc']))}: {err['msg']}"
                for err in e.errors()
            ]
        else:
            errors = [str(e)]

    form_values = (
        form.model_dump()
        if form
        else {
            "length": int(form_data.get("length", 12)),
            "use_lower": bool(form_data.get("use_lower")),
            "use_upper": bool(form_data.get("use_upper")),
            "use_digits": bool(form_data.get("use_digits")),
            "use_special": bool(form_data.get("use_special")),
        }
    )

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "errors": errors,
            "password": password,
            "guesses_log": guesses_log,  # <--- 4. Передаем готовое значение
            **report,
            **form_values,
        },
    )
