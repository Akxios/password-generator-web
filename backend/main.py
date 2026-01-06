from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from pathlib import Path

from backend.config import (
    DEFAULT_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    MAX_PASSWORD_LENGTH
)
from backend.src.web.router import router as web_router 
from backend.src.api.router import router as api_router

templates = Jinja2Templates(directory="frontend/templates")
app = FastAPI(title="Password Generator API", description="API для генерации и проверки пароля")

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://127.0.0.1:80001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(web_router)
app.include_router(api_router)


@app.get("/",
    response_class=HTMLResponse,
    summary="Главная страница",
    description="Возвращается главную страницу"    
)
def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
        },
    )
