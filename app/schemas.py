from typing import List, Optional
from pydantic import BaseModel, EmailStr
from .models import AdminType, LevelEnum, RoleEnum


class CompanyBase(BaseModel):
    name: str


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    is_deleted: bool = False
    users: List["User"] = []

    class Config:
        from_attributes = True


class CompanyResponse(BaseModel):  # Schema para resposta da rota de Company
    id: int
    name: str
    is_deleted: bool = False

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    phone: Optional[str] = None
    company_id: int
    rol: RoleEnum
    level: LevelEnum


class UserCreate(UserBase):
    password: str
    email: EmailStr
    # admin_type: Optional[AdminType]


class User(UserBase):
    id: int
    is_active: bool = True
    is_deleted: bool = False
    email: EmailStr
    company: Company
    admin_type: Optional[AdminType]

    class Config:
        from_attributes = True


class UserResponse(BaseModel):  # Schema para resposta da rota de User
    id: int
    name: str
    phone: Optional[str] = None
    email: EmailStr
    company_id: int
    rol: RoleEnum
    level: LevelEnum
    is_active: bool = True
    is_deleted: bool = False
    admin_type: Optional[AdminType]

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
