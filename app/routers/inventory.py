from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import requests

from .. import models, schemas
from ..database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new part
@router.post("/parts/", response_model=schemas.PartOut, status_code=status.HTTP_201_CREATED)
def create_part(part: schemas.PartCreate, db: Session = Depends(get_db)):
    db_part = models.Part(**part.dict())
    db.add(db_part)
    db.commit()
    db.refresh(db_part)
    return db_part

# Retrieve parts with optional skip/limit
@router.get("/parts/", response_model=List[schemas.PartOut])
def get_parts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Part).offset(skip).limit(limit).all()

# Retrieve a specific part by ID
@router.get("/parts/{part_id}", response_model=schemas.PartOut)
def get_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    return part

# Update a part
@router.put("/parts/{part_id}", response_model=schemas.PartOut)
def update_part(part_id: int, part_in: schemas.PartCreate, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    for field, value in part_in.dict().items():
        setattr(part, field, value)
    db.commit()
    db.refresh(part)
    return part

# Delete a part
@router.delete("/parts/{part_id}")
def delete_part(part_id: int, db: Session = Depends(get_db)):
    part = db.query(models.Part).filter(models.Part.id == part_id).first()
    if not part:
        raise HTTPException(status_code=404, detail="Part not found")
    db.delete(part)
    db.commit()
    return {"message": "Part deleted"}

# Get low-stock suggestions from LLM
@router.get("/low-stock", response_model=List[schemas.SuggestionResponse])
def get_low_stock_suggestions(db: Session = Depends(get_db)):
    low_parts = db.query(models.Part).filter(models.Part.qty <= 5).all()
    suggestions = []
    for part in low_parts:
        prompt = f"Part {part.part_number} has low stock of {part.qty}. Suggest reorder quantity and reason."
        try:
            response = requests.post(
                "http://127.0.0.1:8000/v1/completions",
                json={"model": "suggestion-model", "prompt": prompt},
                timeout=10,
            )
            if response.status_code == 200:
                suggestion = response.json().get("choices", [{}])[0].get("text", "Reorder now.")
            else:
                suggestion = "Error contacting LLM."
        except Exception:
            suggestion = "Error contacting LLM."
        suggestions.append(schemas.SuggestionResponse(part_number=part.part_number, suggestion=suggestion))
    return suggestions