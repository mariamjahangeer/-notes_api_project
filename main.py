from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas
from database import engine, get_db

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# ➕ Create a new note (no response_model for now)
@app.post("/notes")
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(**note.dict())
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return {
        "id": db_note.id,
        "title": db_note.title,
        "content": db_note.content
    }


# 📥 Get all notes (returning manually)
@app.get("/notes")
def get_notes(db: Session = Depends(get_db)):
    notes = db.query(models.Note).all()
    return [
        {
            "id": note.id,
            "title": note.title,
            "content": note.content
        }
        for note in notes
    ]


# 🔍 Get note by ID
@app.get("/notes/{note_id}")
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content
    }


# 📝 Update note
@app.put("/notes/{note_id}")
def update_note(note_id: int, updated_note: schemas.NoteCreate, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    for key, value in updated_note.dict().items():
        setattr(note, key, value)

    db.commit()
    db.refresh(note)
    return {
        "id": note.id,
        "title": note.title,
        "content": note.content
    }


# ❌ Delete note
@app.delete("/notes/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"detail": "Note deleted successfully"}



