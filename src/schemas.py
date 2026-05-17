from datetime import date
from pydantic import BaseModel, EmailStr


class ContactModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date
    additional_data: str | None = None


class ContactResponse(ContactModel):
    id: int

    class Config:
        from_attributes = True