from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str
    pinned: bool = False

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int

    class Config:
        orm_mode = True
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str
    completed: bool = False

class NoteCreate(NoteBase):
    pass

class NoteResponse(NoteBase):
    id: int

    class Config:
          from_attributes = True
