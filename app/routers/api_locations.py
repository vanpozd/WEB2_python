from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..models import Location
from ..database import get_db

router = APIRouter()

@router.get("/locations")
def get_locations(db: Session = Depends(get_db)):
    return db.query(Location).all()
