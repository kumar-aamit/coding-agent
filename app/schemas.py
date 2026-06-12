from pydantic import BaseModel

class PartBase(BaseModel):
    part_number: str
    qty: int
    location: str

class PartCreate(PartBase):
    pass

class PartOut(PartBase):
    id: int

    class Config:
        orm_mode = True

class SuggestionResponse(BaseModel):
    part_number: str
    suggestion: str