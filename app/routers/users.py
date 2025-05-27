from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..models import User
from ..database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request, "error": None})

@router.post("/signup", response_class=HTMLResponse)
def signup(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    role: str = Form("user"),
    db: Session = Depends(get_db)
):
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return templates.TemplateResponse("signup.html", {"request": request, "error": "Ім'я вже зайняте"})
    user = User(username=username, password=password, role=role)
    db.add(user)
    db.commit()
    # Після успішної реєстрації — перенаправляємо на сторінку входу
    return RedirectResponse("/login", status_code=302)

@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", response_class=HTMLResponse)
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == username).first()
    if not user or user.password != password:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Невірний логін або пароль"})
    # Тут можна встановити сесію або кукі, але мінімально — перенаправлення на головну
    return RedirectResponse("/", status_code=302)
