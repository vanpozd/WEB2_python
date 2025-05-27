from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from ..models import Location
from ..database import get_db
from ..auth import get_current_user, require_admin

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def read_locations(request: Request, db: Session = Depends(get_db), user=Depends(get_current_user)):
    locations = db.query(Location).all()
    return templates.TemplateResponse("locations.html", {"request": request, "locations": locations, "user": user})

@router.get("/locations/create", response_class=HTMLResponse)
def create_location_form(request: Request, user=Depends(require_admin)):
    return templates.TemplateResponse("create_location.html", {"request": request, "user": user})

@router.post("/locations/create")
def create_location(name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db), user=Depends(require_admin)):
    location = Location(name=name, description=description)
    db.add(location)
    db.commit()
    return RedirectResponse("/", status_code=302)

@router.get("/locations/{loc_id}/edit", response_class=HTMLResponse)
def edit_location_form(loc_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_admin)):
    location = db.query(Location).filter(Location.id == loc_id).first()
    return templates.TemplateResponse("edit_location.html", {"request": request, "location": location, "user": user})

@router.post("/locations/{loc_id}/edit")
def edit_location(loc_id: int, name: str = Form(...), description: str = Form(...), db: Session = Depends(get_db), user=Depends(require_admin)):
    location = db.query(Location).filter(Location.id == loc_id).first()
    location.name = name
    location.description = description
    db.commit()
    return RedirectResponse("/", status_code=302)

@router.post("/locations/{loc_id}/delete")
def delete_location(loc_id: int, db: Session = Depends(get_db), user=Depends(require_admin)):
    location = db.query(Location).filter(Location.id == loc_id).first()
    db.delete(location)
    db.commit()
    return RedirectResponse("/", status_code=302)
